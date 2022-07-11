from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import CustomResource
from gem5.simulate.simulator import Simulator

# Updated version of the hello-world script from the stdlib tutorial

# let's use a very small cache, to see the impact on modeling of memory accesses
cache_hierarchy = PrivateL1CacheHierarchy(l1d_size="1KiB", l1i_size="1KiB")
memory = SingleChannelDDR3_1600("1GiB")

# By default, use AtomicSimpleCPU
processor = SimpleProcessor(cpu_type=CPUTypes.ATOMIC, num_cores=1)

# Uncomment one of the following lines to use TimingSimpleCPU, or O3CPU
#processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, num_cores=1)
#processor = SimpleProcessor(cpu_type=CPUTypes.O3, num_cores=1)


#Add them to the board.
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# Set the workload to IntMM.
# This is a modified version of IntMM (benchmark from llvm tests).
# The matrix size is modfied to reduce the simulation time.
binary = CustomResource("materials/using-gem5/05-cpu-models/IntMM/IntMM")
board.set_se_binary_workload(binary)

# Setup the Simulator and run the simulation.
simulator = Simulator(board=board)
simulator.run()
