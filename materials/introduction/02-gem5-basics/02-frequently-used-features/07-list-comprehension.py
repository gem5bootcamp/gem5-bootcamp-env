from pprint import pprint
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA

if __name__ == "__m5_main__":
    print("List Comprehension")

    print("Example 1")
    x = [k for k in range(10)]  # typical list comprehension
    print(f"x = {x}")
    print()

    print("Example 2")
    processors = [
        SimpleProcessor(cpu_type=cpu, isa=ISA.X86, num_cores=1)
        for cpu in [CPUTypes.ATOMIC, CPUTypes.TIMING, CPUTypes.O3]
    ]
    print("- Processor list:")
    pprint(processors)
    print("- Type of each processor:")
    for index, proc in enumerate(processors):
        # print(vars(proc)) # will list all object variables of an object
        cpu_type = proc.cores[0]._cpu_type
        print(f"Processor {index}: {cpu_type}")
    print()

    print(
        "Example 3"
    )  # we can use a similar syntax for constructing a dictionary or a set
    multi_core_processors = {
        cores: SimpleProcessor(cpu_type=CPUTypes.TIMING, isa=ISA.X86, num_cores=cores)
        for cores in [1, 2, 4]
    }
    print("- Processor list:")
    pprint(multi_core_processors)
    print("- The cores of each multi-core processor:")
    for key, val in multi_core_processors.items():
        num_cores = key
        proc = val
        print(f"Processor with {num_cores} cores: {proc.cores}")
    print()
