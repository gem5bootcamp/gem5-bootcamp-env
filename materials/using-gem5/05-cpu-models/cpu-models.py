from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import CustomResource
from gem5.simulate.simulator import Simulator

# A simple script (similar to the hello-world script from the stdlib tutorial)
# to test with different CPU models
# We will run a simple application with AtomicSimpleCPU, TimingSimpleCPU, and
# O3CPU using two different cache sizes


