---
title: "Adding instructions to gem5"
author: Ayaz Akram
slides_code: EeRIKzkdUJBDlaa9AmzERusBp28hxMfkyIOp-_2H5L9AqQ?e=RoMFUD
livestream_code: Z5B02jkNpck
example_code: /materials/developing-gem5-models/06-cpu-instructions
---

This is a summary document for the gem5 bootcamp session on CPU models.
Topics covered in this tutorial include:

- Basics of an ISA (instruction set architecture)
- ISA and CPU independence in gem5
- Concepts related to an ISA implementation in gem5
- Journey of an instruction in gem5
- gem5 ISA parser
- Adding your own (RISC-V) instructions in gem5
- Testing your instructions in gem5

**Note:** This document is meant to complement the slides used in the bootcamp and will refer to the slides at certain places.

## Basics of an ISA

An ISA (instruction set architecture) is the interface between the hardware and the software parts of a computer system. Whenever, we refer to an ISA, we usually think about the following components that are part of an ISA:

- Instructions/operations
- Registers
- Memory model
- Exception/interrupt handling
- Addressing modes

## ISA and CPU independence in gem5

To be able to use any ISA with any CPU model in gem5, it tries to keep the two independent of each other.
gem5 relies on two generic interfaces to maintain this independence:

- Static instruction: CPU models access the ISA sub-system via static instruction objects.
- Execution context: ISA sub-system accesses the CPU model via execution context interface.

Following picture provides a detailed view of what gem5 components are ISA independent, what are ISA dependent, and what are in between.

![ISA dependent and independent components of gem5](/gem5-bootcamp-env/assets/img/ISAInd.png)

## Concepts related to an ISA implementation in gem5

### Static Instructions

As stated above, the static instruction acts as an interface between a CPU model and the ISA sub-system in gem5. Basically, a static instruction maps to a single binary instruction in the ISA and carries all the static information related to the simulated instruction it refers/maps to.
This information includes number of source and destination registers, the class of the instruction. A static instruction also points to following four virtual functions:

- execute: this function describes how the instruction executes (in other words, how the execution of the instruction can be simulated)
- initiateAcc: this function is used if the static instruction is a memory operation and is currently simulated using a CPU model which uses Timing memory accesses. `initiateAcc` is responsible for starting the memory access.
- completeAcc: `completeAcc` executes when the memory access completes and will perform any function which is needed at that point (e.g., writing back the read value in case of a load operation). Also, this is only used with Timing memory accesses.
- disassemble: This function is responsible for disassembling the instruction and is useful for debugging or generating execution traces.

### Dynamic Instructions

In contrast to static instructions, dynamic instructions carry dynamic information about the currently simulated instruction.
This information includes instruction's address, result, the thread that the instruction belongs to, and the physical register numbers that it is using.

### Execution Context

As stated above, the execution context provides an interface to the ISA sub-system to access the CPU state.
Execution context provides ways to read/write CPU registers (including PC), and the other parts of the memory.

### Thread Context

Thread context is the interface to all state of a thread for anything outside of the CPU.
Thread context is very similar to the execution context and also provides methods to read/write CPU registers.

## Journey of an instruction in gem5

This section goes through the journey of a couple of RISC-V instructions in gem5 when they are simulated using TimingSimple CPU. By following the instructions on slide 18, we can run a simple test program with gem5.
Next, the idea is to run the same program with `gdb` and to put some breakpoints in the gem5 source code (at the important functions that are defined in the ISA sub-system and are responsible for the decoding and the execution of instructions).
Instructions in slide 19, can be used to put breakpoints on relevant functions in a RISC-V Add and Lw (load word) instruction.By printing the backtrace of the previous function calls at the breakpoint we can observe which CPU functions are responsible for calling the ISA-subsystem functions.
As we will see in the next section, the functions where we put our breakpoints are not handwritten code, rather they are auto-generated via the gem5 ISA parser.

## gem5 ISA parser

gem5 uses a DSL (domain specific language) to specify the encoding and execution functions of instructions.
This DSL is understandable by a gem5 ISA parser, which might infer extra information from the ISA description file and finally generates the C++ code which is then compiled into the gem5 binary. Following picture provides a high-level instruction definition flow in gem5.

![High level flow of instruction definition in gem5](/gem5-bootcamp-env/assets/img/ISAParser.png)

Slides (slide 24 -- 88) provide a detailed explanation of gem5 ISA specification DSL. Following is a summary of the details in those slides.

ISA specification files contain different kind of sections. For example, decode section is one of those sections and is responsible for specifying how an instruction would be decoded.
The decode blocks look like a C switch statements block. The decode block can be nested and usually rely on multiple fields in the instruction to determine what instruction is under consideration. Below is an example of a decode block which is responsible for decoding a RISC-V Add instruction and the corresponding C++ code that is generated by the ISA parser.

![Decode block in gem5 ISA DSL](/gem5-bootcamp-env/assets/img/decode.png)

The other kind of sections in ISA specification files is declaration section which defines instruction formats and other supporting elements (e.g., instruction bitfield definitions) that are then used in the decode blocks.
The most important thing in the declaration section is the `format` block.
In the picture above, in the decode block each instruction definition invokes a function call which generates the C++ code for this instruction. The actual code that will be generated (or the function call that is invoked) is determined by the instruction format. 
Instruction format block looks like a python function that takes the arguments supplied by the instruction definition in the decode block and generates some pieces of code (which go in different places in the final C++ files). The output that is generated is following:

- header output: any code that goes into a header file that will be included in the other generated C++ files.
- decoder output: code that goes before the decode function.
- exec output: code that is responsible for defining how this instruction will be executed.
- decode block: this code goes into the decode function.

The format blocks essentially assign strings to some variables (which refer to the above output blocks). One can assign any string value. However, the ISA parser mostly makes use of template blocks and specialize them for the string assignments. The rationale behind using these template blocks is to reduce the amount of code by specializing the same template blocks for different instruction formats. Also, the ability to use one instruction format for multiple (similar in terms of their format) instructions reduces the amount of code needed for the ISA specification.

Moreover, the templates are usually specialized by passing an object of `InstObjParams` class to them. `InstObjParams` encapsulates the full set of parameters to be substituted into a template. It is also important to note that, a developer would specify or define some symbols that are used inside the templates, but the ISA parser would also define multiple other symbols that are then used inside the templates. ISA parser defines these symbols by inferring certain information about the instruction from other components like instruction formats.
Below are a few examples of template blocks and the corresponding C++ code that will be generated using them.

![ROp format used by R format instructions](/gem5-bootcamp-env/assets/img/ROpFormat.png)
*ROp format is used by RISC-V add instruction. Different templates are specialized using InstObjParams object to generate the output blocks.*

![Example of BasicDeclare template](/gem5-bootcamp-env/assets/img/BasicDeclare.png)
*BasicDeclare template is specialized to generate the output that goes in the header files. Above picture shows how the DSL template is converted into C++ code for an add instruction.*

![Example of BasicExecute template](/gem5-bootcamp-env/assets/img/ExecuteTemplate.png)
*BasicDeclare template is specialized to generate the output that defines how this instruction will be executed. Above picture shows how the DSL template is converted into C++ code for an add instruction.*

Other examples of template blocks can be seen in the slides referred above. For memory operations, the execution output is generated through three different templates:

- `fullExecTemplate` (e.g., LoadExecute) used with Atomic memory mode
- `initiateAccTemplate` (e.g., LoadInitiateAcc) used with Timing memory mode
- `completeAccTemplate` (e.g., LoadCompleteAcc) used with Timing memory mode

Slide 62 to 79 provide examples of these template blocks for a load word instruction.

A couple of other important components of gem5 ISA parser are `bitfield` and `instruction operand` definitions. A bitfield definition eventually generates a C++ preprocessor macro which will take out the relevant bits from the instruction machine code. Instruction operands are defined via special dictionary which maps operands to five element tuples. The tuple specifies information like the operand class, default operand type, bitfield name (how to specify a particular instance), instruction flags, and order of the operand in the disassembly.

## Adding new instructions in gem5

In this gem5 bootcamp session, we added support for a couple of [RISC-V Packed SIMD](https://github.com/riscv/riscv-p-spec/blob/master/P-ext-proposal.pdf) instructions in gem5.
RISC-V packed SIMD instruction extension defines a number of instructions that can be used for subword parallelism (i.e., operate on multiple parts of a general purpose register in parallel). Slide 90 -- 99 covers this part. A gem5 changeset with the changes required to support two new instructions in gem5 is provided in `materials/developing-gem5-models/06-cpu-instructions/finished-material`.

## Testing newly added instructions in gem5

Finally, after recompiling gem5 once your changes are added, to test the newly added instructions we can rely on two scripts (`add16_test.py` and `sra16_test.py`) provided in `materials/developing-gem5-models/06-cpu-instructions`. Slide 101 -- 111 cover this part of the session. The test binaries (along with their source) used by the previously mentioned scripts are provided in `materials/developing-gem5-models/tests`.
