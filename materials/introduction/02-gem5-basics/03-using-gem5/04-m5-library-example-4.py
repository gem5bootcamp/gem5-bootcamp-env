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

"""
This gem5 configuration script creates a simple board to run an X86
"hello world" binary.

This is setup is the close to the simplest setup possible using the gem5
library. It does not contain any kind of caching, IO, or any non-essential
components.

Usage
-----

```
gem5-x86 03-m5-library-example-3.py
```
"""

import argparse

import m5
from m5.objects import AtomicSimpleCPU, Root

from gem5.isas import ISA
from gem5.utils.requires import requires
from gem5.resources.resource import Resource
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.simulate.simulator import Simulator
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)

if __name__ == "__m5_main__":

    # parsing arguments
    parser = argparse.ArgumentParser(description="System Configuration")
    parser.add_argument(
        "cpu_type", type=str, help="CPU type, options are atomic, timing"
    )
    parser.add_argument("l1d_size", type=str, help="Size of L1 data cache, e.g. 16kB")
    parser.add_argument("--clk_freq", type=str, help="Clock Frequency", default="1GHz")

    args = parser.parse_args()

    cpu_type = None
    if args.cpu_type == "atomic":
        cpu_type = CPUTypes.ATOMIC
    elif args.cpu_type == "timing":
        cpu_type = CPUTypes.TIMING
    else:
        raise Error("Unsupported CPU type. Must be atomic or timing")

    # Using gem5 standard library (i.e. import gem5) to build the system
    requires(isa_required=ISA.X86)
    # Here we setup the parameters of the l1 and l2 caches.
    cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
        l1d_size=args.l1d_size,
        l1i_size="16kB",
        l2_size="256kB",
    )
    memory = SingleChannelDDR3_1600(size="32MB")
    processor = SimpleProcessor(cpu_type=cpu_type, isa=ISA.X86, num_cores=1)
    board = SimpleBoard(
        clk_freq=args.clk_freq,
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy,
    )
    board.set_se_binary_workload(Resource("x86-hello64-static"))

    # Using the m5 library to drive the simulation
    root = Root(full_system=False, system=board)
    m5.instantiate()
    exit_event = m5.simulate()  # simulate the first 10 million ticks
    print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}.")
    print()
