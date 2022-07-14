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
Hands-on Session 3: Checkpoints
-------------------------------------------
This is a completed renscript file.

This is a simple script to run the a binary program using the SimpleBoard.
We will use x86 ISA for this example. This script is partly taken from
configs/example/gem5_library/arm-hello.py

* Limitations *
---------------
1. We are only simulating workloads with one CPU core.
2. The binary cannot accept any arguments.

Usage:
------

```
scons build/X86/gem5.opt -j<num_proc>
./build/X86/gem5.opt base-system.py --binary <path/to/binary>
```
"""

# Importing the required python packages here

import os
import argparse

# We need to first determine which ISA that we want to use. Then we have to
# make sure that we are using the correct ISA while executing this script.

from gem5.isas import ISA
from gem5.utils.requires import requires

# We will use CustomResource to load the program in gem5.

from gem5.resources.resource import CustomResource

# We import various parameters of the machine.

from gem5.components.cachehierarchies.classic\
    .private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory import DualChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.processors.simple_processor import SimpleProcessor

# We will use the new simulator module to simulate this task.

from gem5.simulate.simulator import Simulator
from gem5.simulate.exit_event import ExitEvent

from m5.util import fatal

# We are using argparse to supply the path to the binary.

parser = argparse.ArgumentParser(
    description = "An example configuration script to run the matrix multiply \
            binary in gem5."
)

parser.add_argument(
    "--binary",
    "-b",
    type = str,
    required = True,
    help = "Input the path to the matrix multiply binary."
)

args = parser.parse_args()

# Ensure that the binary exists.

if not os.path.exists(os.path.join(os.getcwd(), args.binary)):
    fatal("The binary file does not exists!")

# This check ensures the gem5 binary is compiled to the X86 target. If not,
# an exception will be thrown.

requires(
    isa_required=ISA.X86
)

# We have PrivateL1PrivateL2CacheHierarchy

cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1d_size="16kB",
    l1i_size="16kB",
    l2_size="256kB",
)

# The memory has been correctly setup

memory = DualChannelDDR4_2400(size="2GB")

# We have a TIMING CPU. 

processor = SimpleProcessor(
    cpu_type = CPUTypes.TIMING,
    isa = ISA.X86,
    num_cores = 1
)

# The gem5 library's SimpleBoard can be used to run simple SE-mode simulations.
# Connecting all the different components to the board to complete the system.

board = SimpleBoard(
    clk_freq = "3GHz",
    processor = processor,
    memory = memory,
    cache_hierarchy = cache_hierarchy,
)

# Here we set the workload.

board.set_se_binary_workload(
    CustomResource(
        os.path.join(
            os.getcwd(),
            args.binary
        )
    )
)

# Lastly we instantiate the simulator module and simulate the program.

simulator = Simulator(board=board)
simulator.run()

# We acknowlwdge the user that the simulation has ended.

print(
    "Exiting @ tick {} because {}.".format(
        simulator.get_current_tick(),
        simulator.get_last_exit_event_cause(),
    )
)
