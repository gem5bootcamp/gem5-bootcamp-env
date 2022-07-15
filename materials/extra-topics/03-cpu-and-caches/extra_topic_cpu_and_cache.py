# Copyright (c) 2022 The Regents of the University of California.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This is a simple script to demonstrate cache replacement policies, prefetchers
and branch predictors in gem5 stdlib. We will use RISCV ISA for this example.
This script is taken from the course ECS201A, taught in the Winter quarter of
2022 at UC Davis.

Usage:
------
```
scons build/X86/gem5.opt -j<num_proc>
./build/X86/gem5.opt extra_topic_cpu_and_cache.py
```
"""
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes

from gem5.components.cachehierarchies.abstract_cache_hierarchy \
    import AbstractCacheHierarchy
from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy\
    import AbstractClassicCacheHierarchy
from gem5.components.cachehierarchies.abstract_two_level_cache_hierarchy \
    import AbstractTwoLevelCacheHierarchy
from gem5.components.cachehierarchies.classic.caches.l1dcache import L1DCache
from gem5.components.cachehierarchies.classic.caches.l1icache import L1ICache
from gem5.components.cachehierarchies.classic.caches.l2cache import L2Cache

from gem5.components.memory import SingleChannelDDR3_1600

from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.boards.simple_board import SimpleBoard
from gem5.simulate.simulator import Simulator
from gem5.resources.resource import CustomResource

from m5.objects import L2XBar, BaseXBar, SystemXBar, BadAddr, Port, NULL
from m5.objects import NULL, TaggedPrefetcher, BasePrefetcher, StridePrefetcher
from m5.objects import  LRURP, LFURP, RandomRP, TreePLRURP, WeightedLRURP
from m5.objects.BranchPredictor import *

from gem5.utils.override import overrides

class SmallL1(L1DCache):
    def __init__(self):
        super().__init__(size='16KiB',
                        tag_latency=1,
                        data_latency=1,
                        PrefetcherCls = NULL)

class MyL2Cache(L2Cache):
    def __init__(self):
        super().__init__(size='512KiB', PrefetcherCls = TaggedPrefetcher)

class My2LevelCacheHierarchy(
    AbstractClassicCacheHierarchy, AbstractTwoLevelCacheHierarchy
):
    """
    A cache setup where each core has a private L1 Data and Instruction Cache,
    and a private L2 cache.
    """

    @staticmethod
    def _get_default_membus() -> SystemXBar:
        """
        A method used to obtain the default memory bus of 64 bit in width for
        the PrivateL1PrivateL2 CacheHierarchy.

        :returns: The default memory bus for the PrivateL1PrivateL2
        CacheHierarchy.

        :rtype: SystemXBar
        """
        membus = SystemXBar(width=64)
        membus.badaddr_responder = BadAddr()
        membus.default = membus.badaddr_responder.pio
        return membus

    def __init__(
        self,
        l1_cache,
        l2_cache
    ) -> None:
        """
        :param membus: The memory bus. This parameter is optional parameter and
        will default to a 64 bit width SystemXBar is not specified.

        :type membus: BaseXBar
        """

        AbstractClassicCacheHierarchy.__init__(self=self)
        # dummy call...
        AbstractTwoLevelCacheHierarchy.__init__(
            self,
            l1i_size="32KiB",
            l1i_assoc=8,
            l1d_size="32KiB",
            l1d_assoc=8,
            l2_size="256KiB",
            l2_assoc=4,
        )

        self.l1dcache = l1_cache
        self.l2cache = l2_cache

        self.membus = SystemXBar(width=64)
        self.membus.badaddr_responder = BadAddr()
        self.membus.default = self.membus.badaddr_responder.pio
        # self.membus = membus

    @overrides(AbstractClassicCacheHierarchy)
    def get_mem_side_port(self) -> Port:
        return self.membus.mem_side_ports

    @overrides(AbstractClassicCacheHierarchy)
    def get_cpu_side_port(self) -> Port:
        return self.membus.cpu_side_ports

    @overrides(AbstractCacheHierarchy)
    def incorporate_cache(self, board: AbstractBoard) -> None:

        # Set up the system port for functional access from the simulator.
        board.connect_system_port(self.membus.cpu_side_ports)

        for cntr in board.get_memory().get_memory_controllers():
            cntr.port = self.membus.mem_side_ports

        self.l1icache = L1ICache(size=self._l1i_size)

        self.l2bus = L2XBar()
        self.l2cache.replacement_policy = RandomRP()

        cpu = board.get_processor().get_cores()[0]

        cpu.connect_icache(self.l1icache.cpu_side)
        cpu.connect_dcache(self.l1dcache.cpu_side)

        self.l1icache.mem_side = self.l2bus.cpu_side_ports
        self.l1dcache.mem_side = self.l2bus.cpu_side_ports

        self.l2bus.mem_side_ports = self.l2cache.cpu_side

        self.membus.cpu_side_ports = self.l2cache.mem_side

        cpu.connect_interrupt()

class MyO3Processor(SimpleProcessor):
    def __init__(self, width, rob_size, num_regs):
        """A simple to configure single core out-of-order processor.

        :param width: The pipeline width. Max value is 8.
        :param rob_size: The number of entries in the reorder buffer
        :param num_regs: The number of physical register for both integer and
            floating point register files.
        :param branch_predictor: One of the options in `branch_predictors`
        """
        super().__init__(cpu_type = CPUTypes.O3, num_cores=1)

        self.cores[0].core.fetchWidth = width
        self.cores[0].core.decodeWidth = width
        self.cores[0].core.renameWidth = width
        self.cores[0].core.issueWidth = width
        self.cores[0].core.wbWidth = width
        self.cores[0].core.commitWidth = width

        self.cores[0].core.numROBEntries = rob_size

        self.cores[0].core.numPhysIntRegs = num_regs
        self.cores[0].core.numPhysFloatRegs = num_regs

        self.cores[0].core.branchPred = BiModeBP()


class RiscvSEBoard(SimpleBoard):

    def __init__(self):
        """A simple RISC-V SE mode board.

        Has a small (512 MiB) DDR3 memory. This is small to support faster
        execution.
        Has a 2-level hierarchy.
        Can use any processor, but it is designed to be used with the simple
        O3 processor `MyO3Processor`.
        Runs at 3GHz.
        """

        memory = SingleChannelDDR3_1600(size="512MiB")

        super().__init__(
            clk_freq="3GHz",
            processor=MyO3Processor(8, 192, 256),
            memory=memory,
            cache_hierarchy=My2LevelCacheHierarchy(SmallL1(), MyL2Cache()),
        )

benchmark = CustomResource('mm-riscv-gem5')

def run_experiment():
    board = RiscvSEBoard()

    board.set_se_binary_workload(benchmark)
    board.processor.get_cores()[0].core.workload[0].cmd = [
            'mm-riscv-gem5',
            '25',
            1]

    simulator = Simulator(board=board, full_system=False)

    simulator.run()

if __name__ == "__m5_main__":
    run_experiment()
