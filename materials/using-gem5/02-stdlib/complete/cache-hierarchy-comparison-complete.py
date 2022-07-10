from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import Resource
from gem5.resources.resource import CustomResource
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires
from gem5.isas import ISA

import argparse

requires(isa_required=ISA.X86)

parser = argparse.ArgumentParser(
    description="A script to check the difference between the "
    "PrivateL1PrivateL2CacheHierarchy and the "
    "PrivateL1CacheHierarchy"
)

parser.add_argument(
    "-s",
    "--shared-l2",
    action="store_true",
    help="If set the PrivateL1SharedL2CacheHierarchy will be used. Otherwise "
    "the PrivateL1CacheHierarchy will be used.",
)

parser.add_argument(
    "workload",
    type=str,
    choices=("x86-hello64-static", "matrix-multiply"),
    help="The gem5-resources workload to run.",
)

args = parser.parse_args()

# Set the cache hierarchy.
if args.shared_l2:
    print("With Shared L2 Cache")
    from private_l1_shared_l2_cache_hierarchy.private_l1_shared_l2_cache_complete import (
        PrivateL1SharedL2CacheHierarchy,
    )

    cache_hierarchy = PrivateL1SharedL2CacheHierarchy(
        l1d_size="32KiB", l1i_size="32KiB", l2_size="64KiB"
    )
else:
    print("Without Shared L2 Cache")
    from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import (
        PrivateL1CacheHierarchy,
    )

    cache_hierarchy = PrivateL1CacheHierarchy(l1d_size="32KiB", l1i_size="32KiB")

# Declare the rest of the components.
memory = SingleChannelDDR3_1600("1GiB")
processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, num_cores=1)

# Add them to the board.
board = SimpleBoard(
    clk_freq="3GHz", processor=processor, memory=memory, cache_hierarchy=cache_hierarchy
)

# Set the workload.
if args.workload == "x86-hello64-static":
    binary = Resource("x86-hello64-static")
elif args.workload == "matrix-multiply":
    binary = CustomResource(
        "materials/using-gem5/02-stdlib/matrix-multiply/matrix-multiply"
    )
else:
    assert False
board.set_se_binary_workload(binary)

# Setup the Simulator and run the simulation.
simulator = Simulator(board=board)
simulator.run()
