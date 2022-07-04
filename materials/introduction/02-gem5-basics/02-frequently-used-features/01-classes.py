from pprint import pprint
from gem5.components.processors.simple_processor import (
    SimpleProcessor,
    AbstractProcessor,
)
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from abc import abstractmethod


class SimpleProcessorWithID(SimpleProcessor):
    def __init__(self, processor_id, cpu_type, num_cores, isa=None):
        super().__init__(cpu_type, num_cores, isa)
        self._processor_id = processor_id


if __name__ == "__m5_main__":
    processor_1 = SimpleProcessor(cpu_type=CPUTypes.TIMING, isa=ISA.X86, num_cores=1)
    print("Processor_1")
    pprint(vars(processor_1))
    print()

    processor_2 = SimpleProcessorWithID(
        processor_id=1, cpu_type=CPUTypes.TIMING, isa=ISA.X86, num_cores=1
    )
    print("Processor_2")
    pprint(vars(processor_2))
    print()
