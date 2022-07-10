from gem5.components.boards.simple_board import SimpleBoard

# from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import Resource
from gem5.resources.resource import CustomResource
from gem5.simulate.simulator import Simulator


# Obtain the components.
# cache_hierarchy = NoCache()
cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1d_size="32KiB", l1i_size="32KiB", l2_size="64KiB"
)
memory = SingleChannelDDR3_1600("1GiB")
processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, num_cores=1)

# Add them to the board.
board = SimpleBoard(
    clk_freq="3GHz", processor=processor, memory=memory, cache_hierarchy=cache_hierarchy
)

# Set the workload.
# binary = Resource("x86-hello64-static")
binary = CustomResource(
    "materials/using-gem5/02-stdlib/matrix-multiply/matrix-multiply"
)
board.set_se_binary_workload(binary)

# Setup the Simulator and run the simulation.
simulator = Simulator(board=board)
simulator.run()
