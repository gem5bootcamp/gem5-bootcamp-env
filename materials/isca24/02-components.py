"""
This will build a classic caches based system to run a simple x86 SE workload.
IS takes about 40 seconds.

Run with `gem5 02-components.py`
"""

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400

from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA

from gem5.resources.resource import obtain_resource

from gem5.simulate.simulator import Simulator

