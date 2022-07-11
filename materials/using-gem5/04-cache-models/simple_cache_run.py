# Copyright (c) 2021 The Regents of the University of California
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

import m5
import argparse
import importlib
from m5.objects import Root
from gem5.components.boards.test_board import TestBoard
from gem5.components.processors.linear_generator import LinearGenerator
from gem5.components.memory import SingleChannelDDR3_1600

parser = argparse.ArgumentParser(
    description="A traffic generator that can be used to test a gem5 "
    "memory component."
)

parser.add_argument(
    "generator_cores", type=int, help="The number of generator cores to use."
)

parser.add_argument(
    "cache_system",
    type=str,
    help="The cache class to import and instantiate.",
    choices=["Classic", "MESITwoLevel"],
)
parser.add_argument(
    "mem_args",
    nargs="*",
    help="The arguments needed to instantiate the memory class.",
)

def cache_factory(cache):
    if cache == 'Classic':
        from gem5.components.cachehierarchies\
            .classic.private_l1_private_l2_cache_hierarchy import (
            PrivateL1PrivateL2CacheHierarchy,
        )
        return PrivateL1PrivateL2CacheHierarchy(
            l1d_size="32KiB",
            l1i_size="32KiB",
            l2_size="256KiB",
        )
    elif cache == 'MESITwoLevel':
        from gem5.components.cachehierarchies\
            .ruby.mesi_two_level_cache_hierarchy import (
            MESITwoLevelCacheHierarchy,
        )
        return MESITwoLevelCacheHierarchy(
        l1i_size="32KiB",
        l1i_assoc="8",
        l1d_size="32KiB",
        l1d_assoc="8",
        l2_size="256KiB",
        l2_assoc="4",
        num_l2_banks=1,
    )
    else:
        raise ValueError(f"The cache class {cache} is not supported.")



args = parser.parse_args()
cache_hierarchy = cache_factory(args.cache_system)
memory = SingleChannelDDR3_1600(*args.mem_args)
generator = LinearGenerator(
            duration="250us",
            rate="40GB/s",
            num_cores=args.generator_cores,
            max_addr=memory.get_size(),
        )

motherboard = TestBoard(
    clk_freq="3GHz",
    processor=generator,  # We pass the traffic generator as the processor.
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
root = Root(full_system=False, system=motherboard)
m5.instantiate()
generator.start_traffic()
print("Beginning simulation!")
exit_event = m5.simulate()
print(
    "Exiting @ tick {} because {}.".format(m5.curTick(), exit_event.getCause())
)
