---
title: "Creating a `SimObject`"
author: ["Jason Lowe-Power", "Mahyar Samani"]
slides_code: EUq-MeBW7YJKlNOoqk5irdoBoEhpDDlojUDUSEXYWr50Iw?e=cgPEYA
livestream_code: OcXA1D4b1RA
example_code: /materials/developing-gem5-models/02-simobj
---

**NOTE:** This text is not necessarily up to date!

**TO DO:** Please update with `PARAMS(<SimObject>)`

**TO DO:** Update the parameters to not depend on the events

## Setting up your development environment

This is going to talk about getting started developing gem5.

### gem5-style guidelines

When modifying any open source project, it is important to follow the
project's style guidelines. Details on gem5 style can be found on the
gem5 [Coding Style page](http://www.gem5.org/documentation/general_docs/development/coding_style/).

To help you conform to the style guidelines, gem5 includes a script
which runs whenever you commit a changeset in git. This script should be
automatically added to your .git/config file by SCons the first time you
build gem5. Please do not ignore these warnings/errors. However, in the
rare case where you are trying to commit a file that doesn't conform to
the gem5 style guidelines (e.g., something from outside the gem5 source
tree) you can use the git option `--no-verify` to skip running the style
checker.

The key takeaways from the style guide are:

- Use 4 spaces, not tabs
- Sort the includes
- Use capitalized camel case for class names, camel case for member variables and functions, and snake case for local variables.
- Document your code

### git branches

Most people developing with gem5 use the branch feature of git to track
their changes. This makes it quite simple to commit your changes back to
gem5. Additionally, using branches can make it easier to update gem5
with new changes that other people make while keeping your own changes
separate. The [Git book](https://git-scm.com/book/en/v2) has a great
[chapter](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
describing the details of how to use branches.

## Creating a *very* simple `SimObject`

**Note**: gem5 has SimObject named `SimpleObject`. Implementing another
`SimpleObject` SimObject will result in confusing compiler issues.

Almost all objects in gem5 inherit from the base SimObject type.
SimObjects export the main interfaces to all objects in gem5. SimObjects
are wrapped `C++` objects that are accessible from the `Python`
configuration scripts.

SimObjects can have many parameters, which are set via the `Python`
configuration files. In addition to simple parameters like integers and
floating point numbers, they can also have other SimObjects as
parameters. This allows you to create complex system hierarchies, like
real machines.

In this chapter, we will walk through creating a simple "HelloWorld"
SimObject. The goal is to introduce you to how SimObjects are created
and the required boilerplate code for all SimObjects. We will also
create a simple `Python` configuration script which instantiates our
SimObject.

In the next few chapters, we will take this simple SimObject and expand
on it to include [debugging support](../debugging), [dynamic
events](../events), and [parameters](../parameters).

> **Using git branches**
>
> It is common to use a new git branch for each new feature you add to
> gem5.
>
> The first step when adding a new feature or modifying something in
> gem5, is to create a new branch to store your changes. Details on git
> branches can be found in the Git book.
>
> ```sh
> git checkout -b hello-simobject
> ```

### Step 1: Create a Python class for your new SimObject

Each SimObject has a Python class which is associated with it. This
Python class describes the parameters of your SimObject that can be
controlled from the Python configuration files. For our simple
SimObject, we are just going to start out with no parameters. Thus, we
simply need to declare a new class for our SimObject and set it's name
and the C++ header that will define the C++ class for the SimObject.

We can create a file, `HelloObject.py`, in `src/learning_gem5/part2`.
If you have cloned the gem5 repository you'll have the files mentioned
in this tutorial completed under `src/learning_gem5/part2` and
`configs/learning_gem5/part2`. You can delete these or move them
elsewhere to follow this tutorial.

```python
from m5.params import *
from m5.SimObject import SimObject

class HelloObject(SimObject):
    type = 'HelloObject'
    cxx_header = "learning_gem5/part2/hello_object.hh"
```

It is not required that the `type` be the same as the name of the class,
but it is convention. The `type` is the C++ class that you are wrapping
with this Python SimObject. Only in special circumstances should the
`type` and the class name be different.

The `cxx_header` is the file that contains the declaration of the class
used as the `type` parameter. Again, the convention is to use the name
of the SimObject with all lowercase and underscores, but this is only
convention. You can specify any header file here.

### Step 2: Implement your SimObject in C++

Next, we need to create `hello_object.hh` and `hello_object.cc` in
`src/learning_gem5/part2/` directory which will implement the `HelloObject`.

We'll start with the header file for our `C++` object. By convention,
gem5 wraps all header files in `#ifndef/#endif` with the name of the
file and the directory its in so there are no circular includes.

The only thing we need to do in the file is to declare our class. Since
`HelloObject` is a SimObject, it must inherit from the C++ SimObject
class. Most of the time, your SimObject's parent will be a subclass of
SimObject, not SimObject itself.

The SimObject class specifies many virtual functions. However, none of
these functions are pure virtual, so in the simplest case, there is no
need to implement any functions except for the constructor.

The constructor for all SimObjects assumes it will take a parameter
object. This parameter object is automatically created by the build
system and is based on the `Python` class for the SimObject, like the
one we created above. The name for this parameter type is generated
automatically from the name of your object. For our "HelloObject" the
parameter type's name is "HelloObjectParams".

The code required for our simple header file is listed below.

```cpp
#ifndef __LEARNING_GEM5_HELLO_OBJECT_HH__
#define __LEARNING_GEM5_HELLO_OBJECT_HH__

#include "params/HelloObject.hh"
#include "sim/sim_object.hh"

class HelloObject : public SimObject
{
  public:
    HelloObject(const HelloObjectParams &p);
};

#endif // __LEARNING_GEM5_HELLO_OBJECT_HH__
```

Next, we need to implement *two* functions in the `.cc` file, not just
one. The first function, is the constructor for the `HelloObject`. Here
we simply pass the parameter object to the SimObject parent and print
"Hello world!"

Normally, you would **never** use `std::cout` in gem5. Instead, you
should use debug flags. In the [next chapter](../debugging), we
will modify this to use debug flags instead. However, for now, we'll
simply use `std::cout` because it is simple.

```cpp
#include "learning_gem5/part2/hello_object.hh"

#include <iostream>

HelloObject::HelloObject(const HelloObjectParams &params) :
    SimObject(params)
{
    std::cout << "Hello World! From a SimObject!" << std::endl;
}
```

**Note**: If the constructor of your SimObject follows the following
signature,

```cpp
Foo(const FooParams &)
```

then a `FooParams::create()` method will be automatically defined. The purpose
of the `create()` method is to call the SimObject constructor and return an
instance of the SimObject. Most SimObject will follow this pattern; however,
if your SimObject does not follow this pattern,
[the gem5 SimObject documetation](http://doxygen.gem5.org/release/current/classSimObject.html#details)
provides more information about manually implementing the `create()` method.


### Step 3: Register the SimObject and C++ file

In order for the `C++` file to be compiled and the `Python` file to be
parsed we need to tell the build system about these files. gem5 uses
SCons as the build system, so you simply have to create a SConscript
file in the directory with the code for the SimObject. If there is
already a SConscript file for that directory, simply add the following
declarations to that file.

This file is simply a normal `Python` file, so you can write any
`Python` code you want in this file. Some of the scripting can become
quite complicated. gem5 leverages this to automatically create code for
SimObjects and to compile the domain-specific languages like SLICC and
the ISA language.

In the SConscript file, there are a number of functions automatically
defined after you import them. See the section on that...

To get your new SimObject to compile, you simply need to create a new
file with the name "SConscript" in the `src/learning_gem5/part2` directory. In
this file, you have to declare the SimObject and the `.cc` file. Below
is the required code.

```python
Import('*')

SimObject('HelloObject.py')
Source('hello_object.cc')
```

### Step 4: (Re)-build gem5

To compile and link your new files you simply need to recompile gem5.
The below example assumes you are using the x86 ISA, but nothing in our
object requires an ISA so, this will work with any of gem5's ISAs.

```
scons build/X86/gem5.opt
```

### Step 5: Create the config scripts to use your new SimObject

Now that you have implemented a SimObject, and it has been compiled into
gem5, you need to create or modify a `Python` config file `run_hello.py` in
`configs/learning_gem5/part2` to instantiate your object. Since your object
is very simple a system object is not required! CPUs are not needed, or
caches, or anything, except a `Root` object. All gem5 instances require a
`Root` object.

Walking through creating a *very* simple configuration script, first,
import m5 and all of the objects you have compiled.

```python
import m5
from m5.objects import *
```

Next, you have to instantiate the `Root` object, as required by all gem5
instances.

```python
root = Root(full_system = False)
```

Now, you can instantiate the `HelloObject` you created. All you need to
do is call the `Python` "constructor". Later, we will look at how to
specify parameters via the `Python` constructor. In addition to creating
an instantiation of your object, you need to make sure that it is a
child of the root object. Only SimObjects that are children of the
`Root` object are instantiated in `C++`.

```python
root.hello = HelloObject()
```

Finally, you need to call `instantiate` on the `m5` module and actually
run the simulation!

```python
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))
```

Remember to rebuild gem5 after modifying files in the src/ directory. The
command line to run the config file is in the output below after
'command line:'. The output should look something like the following:

Note: If the code for the future section "Adding parameters to SimObjects
and more events", (goodbye_object) is in your `src/learning_gem5/part2`
directory, run_hello.py will cause an error. If you delete those files or
move them outside of the gem5 directory `run_hello.py` should give the output
below.

```termout
    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled May  4 2016 11:37:41
    gem5 started May  4 2016 11:44:28
    gem5 executing on mustardseed.cs.wisc.edu, pid 22480
    command line: build/X86/gem5.opt configs/learning_gem5/part2/run_hello.py

    Global frequency set at 1000000000000 ticks per second
    Hello World! From a SimObject!
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
    Exiting @ tick 18446744073709551615 because simulate() limit reached
```

Congrats! You have written your first SimObject. In the next chapters,
we will extend this SimObject and explore what you can do with
SimObjects.

## Debugging in gem5

Above, we covered how to
create a very simple SimObject. In this chapter, we will replace the
simple print to `stdout` with gem5's debugging support.

gem5 provides support for `printf`-style tracing/debugging of your code
via *debug flags*. These flags allow every component to have many
debug-print statements, without all of them enabled at the same time.
When running gem5, you can specify which debug flags to enable from the
command line.

### Using debug flags

For instance, when running the first simple.py script from
simple-config-chapter, if you enable the `DRAM` debug flag, you get the
following output. Note that this generates *a lot* of output to the
console (about 7 MB).

```sh
    build/X86/gem5.opt --debug-flags=DRAM configs/learning_gem5/part1/simple.py | head -n 50
```

```termout
    gem5 Simulator System.  http://gem5.org
    DRAM device capacity (gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  3 2017 16:03:38
    gem5 started Jan  3 2017 16:09:53
    gem5 executing on chinook, pid 19223
    command line: build/X86/gem5.opt --debug-flags=DRAM configs/learning_gem5/part1/simple.py

    Global frequency set at 1000000000000 ticks per second
          0: system.mem_ctrl: Memory capacity 536870912 (536870912) bytes
          0: system.mem_ctrl: Row buffer size 8192 bytes with 128 columns per row buffer
          0: system.remote_gdb.listener: listening for remote gdb #0 on port 7000
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
          0: system.mem_ctrl: recvTimingReq: request ReadReq addr 400 size 8
          0: system.mem_ctrl: Read queue limit 32, current size 0, entries needed 1
          0: system.mem_ctrl: Address: 400 Rank 0 Bank 0 Row 0
          0: system.mem_ctrl: Read queue limit 32, current size 0, entries needed 1
          0: system.mem_ctrl: Adding to read queue
          0: system.mem_ctrl: Request scheduled immediately
          0: system.mem_ctrl: Single request, going to a free rank
          0: system.mem_ctrl: Timing access to addr 400, rank/bank/row 0 0 0
          0: system.mem_ctrl: Activate at tick 0
          0: system.mem_ctrl: Activate bank 0, rank 0 at tick 0, now got 1 active
          0: system.mem_ctrl: Access to 400, ready at 46250 bus busy until 46250.
      46250: system.mem_ctrl: processRespondEvent(): Some req has reached its readyTime
      46250: system.mem_ctrl: number of read entries for rank 0 is 0
      46250: system.mem_ctrl: Responding to Address 400..   46250: system.mem_ctrl: Done
      77000: system.mem_ctrl: recvTimingReq: request ReadReq addr 400 size 8
      77000: system.mem_ctrl: Read queue limit 32, current size 0, entries needed 1
      77000: system.mem_ctrl: Address: 400 Rank 0 Bank 0 Row 0
      77000: system.mem_ctrl: Read queue limit 32, current size 0, entries needed 1
      77000: system.mem_ctrl: Adding to read queue
      77000: system.mem_ctrl: Request scheduled immediately
      77000: system.mem_ctrl: Single request, going to a free rank
      77000: system.mem_ctrl: Timing access to addr 400, rank/bank/row 0 0 0
      77000: system.mem_ctrl: Access to 400, ready at 101750 bus busy until 101750.
     101750: system.mem_ctrl: processRespondEvent(): Some req has reached its readyTime
     101750: system.mem_ctrl: number of read entries for rank 0 is 0
     101750: system.mem_ctrl: Responding to Address 400..  101750: system.mem_ctrl: Done
     132000: system.mem_ctrl: recvTimingReq: request ReadReq addr 400 size 8
     132000: system.mem_ctrl: Read queue limit 32, current size 0, entries needed 1
     132000: system.mem_ctrl: Address: 400 Rank 0 Bank 0 Row 0
     132000: system.mem_ctrl: Read queue limit 32, current size 0, entries needed 1
     132000: system.mem_ctrl: Adding to read queue
     132000: system.mem_ctrl: Request scheduled immediately
     132000: system.mem_ctrl: Single request, going to a free rank
     132000: system.mem_ctrl: Timing access to addr 400, rank/bank/row 0 0 0
     132000: system.mem_ctrl: Access to 400, ready at 156750 bus busy until 156750.
     156750: system.mem_ctrl: processRespondEvent(): Some req has reached its readyTime
     156750: system.mem_ctrl: number of read entries for rank 0 is 0
```

Or, you may want to debug based on the exact instruction the CPU is
executing. For this, the `Exec` debug flag may be useful. This debug
flags shows details of how each instruction is executed by the simulated
CPU.

```sh
    build/X86/gem5.opt --debug-flags=Exec configs/learning_gem5/part1/simple.py | head -n 50
```

```termout
    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  3 2017 16:03:38
    gem5 started Jan  3 2017 16:11:47
    gem5 executing on chinook, pid 19234
    command line: build/X86/gem5.opt --debug-flags=Exec configs/learning_gem5/part1/simple.py

    Global frequency set at 1000000000000 ticks per second
          0: system.remote_gdb.listener: listening for remote gdb #0 on port 7000
    warn: ClockedObject: More than one power state change request encountered within the same simulation tick
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
      77000: system.cpu T0 : @_start    : xor   rbp, rbp
      77000: system.cpu T0 : @_start.0  :   XOR_R_R : xor   rbp, rbp, rbp : IntAlu :  D=0x0000000000000000
     132000: system.cpu T0 : @_start+3    : mov r9, rdx
     132000: system.cpu T0 : @_start+3.0  :   MOV_R_R : mov   r9, r9, rdx : IntAlu :  D=0x0000000000000000
     187000: system.cpu T0 : @_start+6    : pop rsi
     187000: system.cpu T0 : @_start+6.0  :   POP_R : ld   t1, SS:[rsp] : MemRead :  D=0x0000000000000001 A=0x7fffffffee30
     250000: system.cpu T0 : @_start+6.1  :   POP_R : addi   rsp, rsp, 0x8 : IntAlu :  D=0x00007fffffffee38
     250000: system.cpu T0 : @_start+6.2  :   POP_R : mov   rsi, rsi, t1 : IntAlu :  D=0x0000000000000001
     360000: system.cpu T0 : @_start+7    : mov rdx, rsp
     360000: system.cpu T0 : @_start+7.0  :   MOV_R_R : mov   rdx, rdx, rsp : IntAlu :  D=0x00007fffffffee38
     415000: system.cpu T0 : @_start+10    : and    rax, 0xfffffffffffffff0
     415000: system.cpu T0 : @_start+10.0  :   AND_R_I : limm   t1, 0xfffffffffffffff0 : IntAlu :  D=0xfffffffffffffff0
     415000: system.cpu T0 : @_start+10.1  :   AND_R_I : and   rsp, rsp, t1 : IntAlu :  D=0x0000000000000000
     470000: system.cpu T0 : @_start+14    : push   rax
     470000: system.cpu T0 : @_start+14.0  :   PUSH_R : st   rax, SS:[rsp + 0xfffffffffffffff8] : MemWrite :  D=0x0000000000000000 A=0x7fffffffee28
     491000: system.cpu T0 : @_start+14.1  :   PUSH_R : subi   rsp, rsp, 0x8 : IntAlu :  D=0x00007fffffffee28
     546000: system.cpu T0 : @_start+15    : push   rsp
     546000: system.cpu T0 : @_start+15.0  :   PUSH_R : st   rsp, SS:[rsp + 0xfffffffffffffff8] : MemWrite :  D=0x00007fffffffee28 A=0x7fffffffee20
     567000: system.cpu T0 : @_start+15.1  :   PUSH_R : subi   rsp, rsp, 0x8 : IntAlu :  D=0x00007fffffffee20
     622000: system.cpu T0 : @_start+16    : mov    r15, 0x40a060
     622000: system.cpu T0 : @_start+16.0  :   MOV_R_I : limm   r8, 0x40a060 : IntAlu :  D=0x000000000040a060
     732000: system.cpu T0 : @_start+23    : mov    rdi, 0x409ff0
     732000: system.cpu T0 : @_start+23.0  :   MOV_R_I : limm   rcx, 0x409ff0 : IntAlu :  D=0x0000000000409ff0
     842000: system.cpu T0 : @_start+30    : mov    rdi, 0x400274
     842000: system.cpu T0 : @_start+30.0  :   MOV_R_I : limm   rdi, 0x400274 : IntAlu :  D=0x0000000000400274
     952000: system.cpu T0 : @_start+37    : call   0x9846
     952000: system.cpu T0 : @_start+37.0  :   CALL_NEAR_I : limm   t1, 0x9846 : IntAlu :  D=0x0000000000009846
     952000: system.cpu T0 : @_start+37.1  :   CALL_NEAR_I : rdip   t7, %ctrl153,  : IntAlu :  D=0x00000000004001ba
     952000: system.cpu T0 : @_start+37.2  :   CALL_NEAR_I : st   t7, SS:[rsp + 0xfffffffffffffff8] : MemWrite :  D=0x00000000004001ba A=0x7fffffffee18
     973000: system.cpu T0 : @_start+37.3  :   CALL_NEAR_I : subi   rsp, rsp, 0x8 : IntAlu :  D=0x00007fffffffee18
     973000: system.cpu T0 : @_start+37.4  :   CALL_NEAR_I : wrip   , t7, t1 : IntAlu :
    1042000: system.cpu T0 : @__libc_start_main    : push   r15
    1042000: system.cpu T0 : @__libc_start_main.0  :   PUSH_R : st   r15, SS:[rsp + 0xfffffffffffffff8] : MemWrite :  D=0x0000000000000000 A=0x7fffffffee10
    1063000: system.cpu T0 : @__libc_start_main.1  :   PUSH_R : subi   rsp, rsp, 0x8 : IntAlu :  D=0x00007fffffffee10
    1118000: system.cpu T0 : @__libc_start_main+2    : movsxd   rax, rsi
    1118000: system.cpu T0 : @__libc_start_main+2.0  :   MOVSXD_R_R : sexti   rax, rsi, 0x1f : IntAlu :  D=0x0000000000000001
    1173000: system.cpu T0 : @__libc_start_main+5    : mov  r15, r9
    1173000: system.cpu T0 : @__libc_start_main+5.0  :   MOV_R_R : mov   r15, r15, r9 : IntAlu :  D=0x0000000000000000
    1228000: system.cpu T0 : @__libc_start_main+8    : push r14
```

In fact, the `Exec` flag is actually an agglomeration of multiple debug
flags. You can see this, and all of the available debug flags, by
running gem5 with the `--debug-help` parameter.

```sh
    build/X86/gem5.opt --debug-help
```

```termout
    Base Flags:
        Activity: None
        AddrRanges: None
        Annotate: State machine annotation debugging
        AnnotateQ: State machine annotation queue debugging
        AnnotateVerbose: Dump all state machine annotation details
        BaseXBar: None
        Branch: None
        Bridge: None
        CCRegs: None
        CMOS: Accesses to CMOS devices
        Cache: None
        CacheComp: None
        CachePort: None
        CacheRepl: None
        CacheTags: None
        CacheVerbose: None
        Checker: None
        Checkpoint: None
        ClockDomain: None
    ...
    Compound Flags:
        All: Controls all debug flags. It should not be used within C++ code.
            All Base Flags
        AnnotateAll: All Annotation flags
            Annotate, AnnotateQ, AnnotateVerbose
        CacheAll: None
            Cache, CacheComp, CachePort, CacheRepl, CacheVerbose, HWPrefetch
        DiskImageAll: None
            DiskImageRead, DiskImageWrite
    ...
    XBar: None
        BaseXBar, CoherentXBar, NoncoherentXBar, SnoopFilter
```

### Adding a new debug flag

In the [previous chapters](../helloobject), we used a simple
`std::cout` to print from our SimObject. While it is possible to use the
normal C/C++ I/O in gem5, it is highly discouraged. So, we are now going
to replace this and use gem5's debugging facilities instead.

When creating a new debug flag, we first have to declare it in a
SConscript file. Add the following to the SConscript file in the
directory with your hello object code (src/learning\_gem5/).

```python
DebugFlag('HelloExample')
```

This declares a debug flag of "HelloExample". Now, we can use this in debug
statements in our SimObject.

By declaring the flag in the SConscript file, a debug header is
automatically generated that allows us to use the debug flag. The header
file is in the `debug` directory and has the same name (and
capitalization) as what we declare in the SConscript file. Therefore, we
need to include the automatically generated header file in any files
where we plan to use the debug flag.

In the `hello_object.cc` file, we need to include the header file.

```cpp
#include "debug/HelloExample.hh"
```

Now that we have included the necessary header file, let's replace the
`std::cout` call with a debug statement like so.

```cpp
DPRINTF(HelloExample, "Created the hello object\n");
```

`DPRINTF` is a C++ macro. The first parameter is a *debug flag* that has
been declared in a SConscript file. We can use the flag `Hello` since we
declared it in the `src/learning_gem5/SConscript` file. The rest of the
arguments are variable and can be anything you would pass to a `printf`
statement.

Now, if you recompile gem5 and run it with the "Hello" debug flag, you
get the following result.

```sh
    build/X86/gem5.opt --debug-flags=Hello configs/learning_gem5/part2/run_hello.py
```

```termout
    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  4 2017 09:40:10
    gem5 started Jan  4 2017 09:41:01
    gem5 executing on chinook, pid 29078
    command line: build/X86/gem5.opt --debug-flags=Hello configs/learning_gem5/part2/run_hello.py

    Global frequency set at 1000000000000 ticks per second
          0: hello: Created the hello object
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
    Exiting @ tick 18446744073709551615 because simulate() limit reached
```

You can find the updated SConcript file
[here](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part2/SConscript)
and the updated hello object code
[here](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part2/hello_object.cc).

### Debug output

For each dynamic `DPRINTF` execution, three things are printed to
`stdout`. First, the current tick when the `DPRINTF` is executed.
Second, the *name of the SimObject* that called `DPRINTF`. This name is
usually the Python variable name from the Python config file. However,
the name is whatever the SimObject `name()` function returns. Finally,
you see whatever format string you passed to the `DPRINTF` function.

You can control where the debug output goes with the `--debug-file`
parameter. By default, all of the debugging output is printed to
`stdout`. However, you can redirect the output to any file. The file is
stored relative to the main gem5 output directory, not the current
working directory.

### Using functions other than DPRINTF

`DPRINTF` is the most commonly used debugging function in gem5. However,
gem5 provides a number of other functions that are useful in specific
circumstances.

> These functions are like the previous functions `:cppDDUMP`,
> `:cppDPRINTF`, and `:cppDPRINTFR` except they do not take a flag as a
> parameter. Therefore, these statements will *always* print whenever
> debugging is enabled.

All of these functions are only enabled if you compile gem5 in "opt" or
"debug" mode. All other modes use empty placeholder macros for the above
functions. Therefore, if you want to use debug flags, you must use
either "gem5.opt" or "gem5.debug".

## Adding parameters to SimObjects and more events

One of the most powerful parts of gem5's Python interface is the ability
to pass parameters from Python to the C++ objects in gem5. In this
chapter, we will explore some of the kinds of parameters for SimObjects
and how to use them building off of the simple `HelloObject` from the
[previous chapters](http://www.gem5.org/documentation/learning_gem5/part2/helloobject/).

### Simple parameters

First, we will add parameters for the latency and number of times to
fire the event in the `HelloObject`. To add a parameter, modify the
`HelloObject` class in the SimObject Python file
(`src/learning_gem5/part2/HelloObject.py`). Parameters are set by adding new
statements to the Python class that include a `Param` type.

For instance, the following code has a parameter `time_to_wait` which is
a "Latency" parameter and `number_of_fires` which is an integer
parameter.

```python
class HelloObject(SimObject):
    type = 'HelloObject'
    cxx_header = "learning_gem5/part2/hello_object.hh"

    time_to_wait = Param.Latency("Time before firing the event")
    number_of_fires = Param.Int(1, "Number of times to fire the event before "
                                   "goodbye")
```

`Param.<TypeName>` declares a parameter of type `TypeName`. Common types
are `Int` for integers, `Float` for floats, etc. These types act like
regular Python classes.

Each parameter declaration takes one or two parameters. When given two
parameters (like `number_of_fires` above), the first parameter is the
*default value* for the parameter. In this case, if you instantiate a
`HelloObject` in your Python config file without specifying any value
for number\_of\_fires, it will take the default value of 1.

The second parameter to the parameter declaration is a short description
of the parameter. This must be a Python string. If you only specify a
single parameter to the parameter declaration, it is the description (as
for `time_to_wait`).

gem5 also supports many complex parameter types that are not just
builtin types. For instance, `time_to_wait` is a `Latency`. `Latency`
takes a value as a time value as a string and converts it into simulator
**ticks**. For instance, with a default tick rate of 1 picosecond
(10\^12 ticks per second or 1 THz), `"1ns"` is automatically converted
to 1000. There are other convenience parameters like `Percent`,
`Cycles`, `MemorySize` and many more.

Once you have declared these parameters in the SimObject file, you need
to copy their values to your C++ class in its constructor. The following
code shows the changes to the `HelloObject` constructor.

```cpp
HelloObject::HelloObject(const HelloObjectParams &params) :
    SimObject(params),
    event(*this),
    myName(params.name),
    latency(params.time_to_wait),
    timesLeft(params.number_of_fires)
{
    DPRINTF(Hello, "Created the hello object with the name %s\n", myName);
}
```

Here, we use the parameter's values for the default values of latency
and timesLeft. Additionally, we store the `name` from the parameter
object to use it later in the member variable `myName`. Each `params`
instantiation has a name which comes from the Python config file when it
is instantiated.

However, assigning the name here is just an example of using the params
object. For all SimObjects, there is a `name()` function that always
returns the name. Thus, there is never a need to store the name like
above.

To the HelloObject class declaration, add a member variable for the
name.

```cpp
class HelloObject : public SimObject
{
  private:
    void processEvent();

    EventWrapper event;

    const std::string myName;

    const Tick latency;

    int timesLeft;

  public:
    HelloObject(HelloObjectParams *p);

    void startup();
};
```

When we run gem5 with the above, we get the following error:

```termout
    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  4 2017 14:46:36
    gem5 started Jan  4 2017 14:46:52
    gem5 executing on chinook, pid 3422
    command line: build/X86/gem5.opt --debug-flags=Hello configs/learning_gem5/part2/run_hello.py

    Global frequency set at 1000000000000 ticks per second
    fatal: hello.time_to_wait without default or user set value
```

This is because the `time_to_wait` parameter does not have a default
value. Therefore, we need to update the Python config file
(`run_hello.py`) to specify this value.

```python
root.hello = HelloObject(time_to_wait = '2us')
```

Or, we can specify `time_to_wait` as a member variable. Either option is
exactly the same because the C++ objects are not created until
`m5.instantiate()` is called.

```python
root.hello = HelloObject()
root.hello.time_to_wait = '2us'
```

The output of this simple script is the following when running the the
`Hello` debug flag.

```termout
    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  4 2017 14:46:36
    gem5 started Jan  4 2017 14:50:08
    gem5 executing on chinook, pid 3455
    command line: build/X86/gem5.opt --debug-flags=Hello configs/learning_gem5/part2/run_hello.py

    Global frequency set at 1000000000000 ticks per second
          0: hello: Created the hello object with the name hello
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
    2000000: hello: Hello world! Processing the event! 0 left
    2000000: hello: Done firing!
    Exiting @ tick 18446744073709551615 because simulate() limit reached
```

You can also modify the config script to fire the event multiple times.

### Other SimObjects as parameters

You can also specify other SimObjects as parameters. To demonstrate
this, we are going to create a new SimObject, `GoodbyeObject`. This
object is going to have a simple function that says "Goodbye" to another
SimObject. To make it a little more interesting, the `GoodbyeObject` is
going to have a buffer to write the message, and a limited bandwidth to
write the message.

First, declare the SimObject in the SConscript file:

```python
Import('*')

SimObject('HelloObject.py')
Source('hello_object.cc')
Source('goodbye_object.cc')

DebugFlag('Hello')
```

The new SConscript file can be downloaded
[here](/_pages/static/scripts/part2/parameters/SConscript).

Next, you need to declare the new SimObject in a SimObject Python file.
Since the `GoodbyeObject` is highly related to the `HelloObject`, we
will use the same file. You can add the following code to
`HelloObject.py`.

This object has two parameters, both with default values. The first
parameter is the size of a buffer and is a `MemorySize` parameter.
Second is the `write_bandwidth` which specifies the speed to fill the
buffer. Once the buffer is full, the simulation will exit.

```python
class GoodbyeObject(SimObject):
    type = 'GoodbyeObject'
    cxx_header = "learning_gem5/part2/goodbye_object.hh"

    buffer_size = Param.MemorySize('1kB',
                                   "Size of buffer to fill with goodbye")
    write_bandwidth = Param.MemoryBandwidth('100MB/s', "Bandwidth to fill "
                                            "the buffer")
```

The updated `HelloObject.py` file can be downloaded
[here](/_pages/static/scripts/part2/parameters/HelloObject.py).

Now, we need to implement the `GoodbyeObject`.

```cpp
#ifndef __LEARNING_GEM5_GOODBYE_OBJECT_HH__
#define __LEARNING_GEM5_GOODBYE_OBJECT_HH__

#include <string>

#include "params/GoodbyeObject.hh"
#include "sim/sim_object.hh"

class GoodbyeObject : public SimObject
{
  private:
    void processEvent();

    /**
     * Fills the buffer for one iteration. If the buffer isn't full, this
     * function will enqueue another event to continue filling.
     */
    void fillBuffer();

    EventWrapper<GoodbyeObject, &GoodbyeObject::processEvent> event;

    /// The bytes processed per tick
    float bandwidth;

    /// The size of the buffer we are going to fill
    int bufferSize;

    /// The buffer we are putting our message in
    char *buffer;

    /// The message to put into the buffer.
    std::string message;

    /// The amount of the buffer we've used so far.
    int bufferUsed;

  public:
    GoodbyeObject(GoodbyeObjectParams *p);
    ~GoodbyeObject();

    /**
     * Called by an outside object. Starts off the events to fill the buffer
     * with a goodbye message.
     *
     * @param name the name of the object we are saying goodbye to.
     */
    void sayGoodbye(std::string name);
};

#endif // __LEARNING_GEM5_GOODBYE_OBJECT_HH__
```

```cpp
#include "learning_gem5/part2/goodbye_object.hh"

#include "debug/Hello.hh"
#include "sim/sim_exit.hh"

GoodbyeObject::GoodbyeObject(const GoodbyeObjectParams &params) :
    SimObject(params), event(*this), bandwidth(params.write_bandwidth),
    bufferSize(params.buffer_size), buffer(nullptr), bufferUsed(0)
{
    buffer = new char[bufferSize];
    DPRINTF(Hello, "Created the goodbye object\n");
}

GoodbyeObject::~GoodbyeObject()
{
    delete[] buffer;
}

void
GoodbyeObject::processEvent()
{
    DPRINTF(Hello, "Processing the event!\n");
    fillBuffer();
}

void
GoodbyeObject::sayGoodbye(std::string other_name)
{
    DPRINTF(Hello, "Saying goodbye to %s\n", other_name);

    message = "Goodbye " + other_name + "!! ";

    fillBuffer();
}

void
GoodbyeObject::fillBuffer()
{
    // There better be a message
    assert(message.length() > 0);

    // Copy from the message to the buffer per byte.
    int bytes_copied = 0;
    for (auto it = message.begin();
         it < message.end() && bufferUsed < bufferSize - 1;
         it++, bufferUsed++, bytes_copied++) {
        // Copy the character into the buffer
        buffer[bufferUsed] = *it;
    }

    if (bufferUsed < bufferSize - 1) {
        // Wait for the next copy for as long as it would have taken
        DPRINTF(Hello, "Scheduling another fillBuffer in %d ticks\n",
                bandwidth * bytes_copied);
        schedule(event, curTick() + bandwidth * bytes_copied);
    } else {
        DPRINTF(Hello, "Goodbye done copying!\n");
        // Be sure to take into account the time for the last bytes
        exitSimLoop(buffer, 0, curTick() + bandwidth * bytes_copied);
    }
}

GoodbyeObject*
GoodbyeObjectParams::create()
{
    return new GoodbyeObject(this);
}
```

The header file can be downloaded
[here](/_pages/static/scripts/part2/parameters/goodbye_object.hh) and the
implementation can be downloaded
[here](/_pages/static/scripts/part2/parameters/goodbye_object.cc).

The interface to this `GoodbyeObject` is simple a function `sayGoodbye`
which takes a string as a parameter. When this function is called, the
simulator builds the message and saves it in a member variable. Then, we
begin filling the buffer.

To model the limited bandwidth, each time we write the message to the
buffer, we pause for the latency it takes to write the message. We use a
simple event to model this pause.

Since we used a `MemoryBandwidth` parameter in the SimObject
declaration, the `bandwidth` variable is automatically converted into
ticks per byte, so calculating the latency is simply the bandwidth times
the bytes we want to write the buffer.

Finally, when the buffer is full, we call the function `exitSimLoop`,
which will exit the simulation. This function takes three parameters,
the first is the message to return to the Python config script
(`exit_event.getCause()`), the second is the exit code, and the third is
when to exit.

#### Adding the GoodbyeObject as a parameter to the HelloObject

First, we will also add a `GoodbyeObject` as a parameter to the
`HelloObject`. To do this, you simply specify the SimObject class name
as the `TypeName` of the `Param`. You can have a default, or not, just
like a normal parameter.

```python
class HelloObject(SimObject):
    type = 'HelloObject'
    cxx_header = "learning_gem5/part2/hello_object.hh"

    time_to_wait = Param.Latency("Time before firing the event")
    number_of_fires = Param.Int(1, "Number of times to fire the event before "
                                   "goodbye")

    goodbye_object = Param.GoodbyeObject("A goodbye object")
```

The updated `HelloObject.py` file can be downloaded
[here](/_pages/static/scripts/part2/parameters/HelloObject.py).

Second, we will add a reference to a `GoodbyeObject` to the
`HelloObject` class.
Don't forget to include goodbye_object.hh at the top of the hello_object.hh file!

```cpp
#include <string>

#include "learning_gem5/part2/goodbye_object.hh"
#include "params/HelloObject.hh"
#include "sim/sim_object.hh"

class HelloObject : public SimObject
{
  private:
    void processEvent();

    EventWrapper event;

    /// Pointer to the corresponding GoodbyeObject. Set via Python
    GoodbyeObject* goodbye;

    /// The name of this object in the Python config file
    const std::string myName;

    /// Latency between calling the event (in ticks)
    const Tick latency;

    /// Number of times left to fire the event before goodbye
    int timesLeft;

  public:
    HelloObject(HelloObjectParams *p);

    void startup();
};
```

Then, we need to update the constructor and the process event function
of the `HelloObject`. We also add a check in the constructor to make
sure the `goodbye` pointer is valid. It is possible to pass a null
pointer as a SimObject via the parameters by using the `NULL` special
Python SimObject. We should *panic* when this happens since it is not a
case this object has been coded to accept.

```cpp
#include "learning_gem5/part2/hello_object.hh"

#include "base/misc.hh"
#include "debug/Hello.hh"

HelloObject::HelloObject(HelloObjectParams &params) :
    SimObject(params),
    event(*this),
    goodbye(params.goodbye_object),
    myName(params.name),
    latency(params.time_to_wait),
    timesLeft(params.number_of_fires)
{
    DPRINTF(Hello, "Created the hello object with the name %s\n", myName);
    panic_if(!goodbye, "HelloObject must have a non-null GoodbyeObject");
}
```

Once we have processed the number of event specified by the parameter,
we should call the `sayGoodbye` function in the `GoodbyeObject`.

```cpp
void
HelloObject::processEvent()
{
    timesLeft--;
    DPRINTF(Hello, "Hello world! Processing the event! %d left\n", timesLeft);

    if (timesLeft <= 0) {
        DPRINTF(Hello, "Done firing!\n");
        goodbye.sayGoodbye(myName);
    } else {
        schedule(event, curTick() + latency);
    }
}
```

You can find the updated header file
[here](/_pages/static/scripts/part2/parameters/hello_object.hh) and the
implementation file
[here](/_pages/static/scripts/part2/parameters/hello_object.cc).

#### Updating the config script

Lastly, we need to add the `GoodbyeObject` to the config script. Create
a new config script, `hello_goodbye.py` and instantiate both the hello
and the goodbye objects. For instance, one possible script is the
following.

```python
import m5
from m5.objects import *

root = Root(full_system = False)

root.hello = HelloObject(time_to_wait = '2us', number_of_fires = 5)
root.hello.goodbye_object = GoodbyeObject(buffer_size='100B')

m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
```

You can download this script
[here](/_pages/static/scripts/part2/parameters/hello_goodbye.py).

Running this script generates the following output.

```termout
    gem5 Simulator System.  http://gem5.org
    gem5 is copyrighted software; use the --copyright option for details.

    gem5 compiled Jan  4 2017 15:17:14
    gem5 started Jan  4 2017 15:18:41
    gem5 executing on chinook, pid 3838
    command line: build/X86/gem5.opt --debug-flags=Hello configs/learning_gem5/part2/hello_goodbye.py

    Global frequency set at 1000000000000 ticks per second
          0: hello.goodbye_object: Created the goodbye object
          0: hello: Created the hello object
    Beginning simulation!
    info: Entering event queue @ 0.  Starting simulation...
    2000000: hello: Hello world! Processing the event! 4 left
    4000000: hello: Hello world! Processing the event! 3 left
    6000000: hello: Hello world! Processing the event! 2 left
    8000000: hello: Hello world! Processing the event! 1 left
    10000000: hello: Hello world! Processing the event! 0 left
    10000000: hello: Done firing!
    10000000: hello.goodbye_object: Saying goodbye to hello
    10000000: hello.goodbye_object: Scheduling another fillBuffer in 152592 ticks
    10152592: hello.goodbye_object: Processing the event!
    10152592: hello.goodbye_object: Scheduling another fillBuffer in 152592 ticks
    10305184: hello.goodbye_object: Processing the event!
    10305184: hello.goodbye_object: Scheduling another fillBuffer in 152592 ticks
    10457776: hello.goodbye_object: Processing the event!
    10457776: hello.goodbye_object: Scheduling another fillBuffer in 152592 ticks
    10610368: hello.goodbye_object: Processing the event!
    10610368: hello.goodbye_object: Scheduling another fillBuffer in 152592 ticks
    10762960: hello.goodbye_object: Processing the event!
    10762960: hello.goodbye_object: Scheduling another fillBuffer in 152592 ticks
    10915552: hello.goodbye_object: Processing the event!
    10915552: hello.goodbye_object: Goodbye done copying!
    Exiting @ tick 10944163 because Goodbye hello!! Goodbye hello!! Goodbye hello!! Goodbye hello!! Goodbye hello!! Goodbye hello!! Goo
```

You can modify the parameters to these two SimObjects and see how the
overall execution time (Exiting @ tick **10944163**) changes. To run
these tests, you may want to remove the debug flag so there is less
output to the terminal.

In the next chapters, we will create a more complex and more useful
SimObject, culminating with a simple blocking uniprocessor cache
implementation.
