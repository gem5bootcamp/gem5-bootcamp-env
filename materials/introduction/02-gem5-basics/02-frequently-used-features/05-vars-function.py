from pprint import pprint
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA

if __name__ == "__m5_main__":
    print("***** Single-core Processor")
    processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, isa=ISA.X86, num_cores=1)
    print(processor)
    pprint(vars(processor))
    print()

    print("***** Multi-core Processor")
    multi_core_processor = SimpleProcessor(
        cpu_type=CPUTypes.TIMING, isa=ISA.X86, num_cores=4
    )
    print(multi_core_processor)
    pprint(vars(multi_core_processor))
    print()

    print(multi_core_processor._cpu_type)
