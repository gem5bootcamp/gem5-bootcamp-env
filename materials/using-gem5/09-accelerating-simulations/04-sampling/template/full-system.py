# Copyright (c) 2022 The Regents of the University of California
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
This script shows an example of booting an ARM based full system Ubuntu
disk image using the gem5's standard library. This simulation boots the disk
image using 2 TIMING CPU cores. The simulation ends when the startup is
completed successfully (i.e. when an `m5_exit instruction is reached on
successful boot).

Usage
-----

```
scons build/ARM/gem5.opt -j<NUM_CPUS>
./build/ARM/gem5.opt configs/example/gem5_library/arm-ubuntu-boot-exit.py
```

"""

from gem5.isas import ISA
from gem5.utils.requires import requires
from gem5.resources.resource import Resource
from gem5.simulate.simulator import Simulator
from gem5.components.boards.x86_board import X86Board
from gem5.components.memory import DualChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_switchable_processor import(
        SimpleSwitchableProcessor,
)

# This runs a check to ensure the gem5 binary is compiled for ARM.

requires(
    isa_required=ISA.X86,
)

from gem5.components.cachehierarchies.classic\
    .private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)


# Here we setup the parameters of the l1 and l2 caches.

cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1d_size="16kB",
    l1i_size="16kB",
    l2_size="256kB",
)

# Memory: Dual Channel DDR4 2400 DRAM device.

memory = DualChannelDDR4_2400(size = "2GB")

# Here we setup the processor. We use a simple TIMING processor. The config
# script was also tested with ATOMIC processor.

processor = SimpleSwitchableProcessor(
    starting_core_type=CPUTypes.ATOMIC,
    switch_core_type=CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=2,
)

# Here we setup the board. The X86Board allows for Full-System ARM simulations.

board = X86Board(
    clk_freq = "3GHz",
    processor = processor,
    memory = memory,
    cache_hierarchy = cache_hierarchy
)

# Here we set the Full System workload.

# The `set_kernel_disk_workload` function on the ArmBoard accepts an ARM
# kernel, a disk image, and, path to the bootloader.

board.set_kernel_disk_workload(

    # The x86 linux kernel will be automatically downloaded to the
    # `~/.cache/gem5` directory if not already present.
    # PARSEC benchamarks were tested with kernel version 4.19.83

    kernel=Resource("x86-linux-kernel-4.19.83"),

    # The x86-ubuntu-18.04 image will be automatically downloaded to the
    # `~/.cache/gem5` directory if not already present.

    disk_image=Resource("x86-ubuntu-18.04-img"),

    # We need to specify the readfile content

    readfile_contents = "m5 exit; echo \"hello world!\"; m5 exit;"
)

# We define the system with the aforementioned system defined.

simulator = Simulator(board = board)

# This X86Board is setup to boot Ubuntu-18.04. Upon successful boot, it will
# execute two instances `m5 exit`. Your task is to complete this code, where,
# after the first `m5 exit`, you need to switch the CPU.

# TIP: The following comments may help

# if simulator.get_last_exit_event_cause() != "m5_exit instruction encountered":
#     fatal("Unexpected EXIT Event Encountered!")

# Otherwise start the simulator module again with a different CPU.
# To switch the processor, use the method `switch`
#
# processor.switch()    -> switches the processor type.