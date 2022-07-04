# Documentation: https://docs.python.org/3/library/argparse.html

from gem5.isas import ISA
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.processors.simple_processor import SimpleProcessor

from pprint import pprint
import argparse

if __name__ == "__m5_main__":
    # Constructing the argument parser
    parser = argparse.ArgumentParser(description="System Configuration")
    parser.add_argument(
        "cpu_type", type=str, help="CPU type, options are atomic, timing"
    )
    parser.add_argument("mem_size", type=str, help="Memory size, e.g. 32MiB")
    parser.add_argument("--num_cores", type=int, help="Number of cores", default="1")
    # Creating the argument parser object
    args = parser.parse_args()
    # Parsing the argument
    inputted_cpu_type = args.cpu_type
    inputted_mem_size = args.mem_size
    inputted_num_cores = args.num_cores

    assigned_cpu_type = None
    if inputted_cpu_type == "atomic":
        assigned_cpu_type = CPUTypes.ATOMIC
    elif inputted_cpu_type == "timing":
        assigned_cpu_type = CPUTypes.TIMING

    # Setting up the system
    cache_hierarchy = NoCache()
    memory = SingleChannelDDR3_1600(size=inputted_mem_size)
    processor = SimpleProcessor(
        cpu_type=assigned_cpu_type, isa=ISA.X86, num_cores=inputted_num_cores
    )
    board = SimpleBoard(
        clk_freq="3GHz",
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy,
    )

    print("***** Processor")
    pprint(vars(processor))
