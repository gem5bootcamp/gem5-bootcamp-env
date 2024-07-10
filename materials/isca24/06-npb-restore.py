"""
Example of how to take restore from a checkpoint taken after booting linux.
Most useful for when you have to use a timing CPU to boot, not with KVM.
Let's use KVM so it's fast, though.
Note: Checkpointing with switchable processor is not well supported

This script changes the CPU type to O3 as an example of what can change
(Note: It's not a great example... but it's an example)

Run with `gem5-mesi 06-npb-restore.py`

When running SP instead of IS, it takes about 5 minutes with timing CPU and
15 minutes with O3
"""

from gem5.coherence_protocol import CoherenceProtocol
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_switchable_processor import (
    SimpleSwitchableProcessor,
)
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource, CheckpointResource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires
import m5

# This simulation requires using KVM with gem5 compiled for X86 simulation
# and with MESI_Two_Level cache coherence protocol.
requires(
    isa_required=ISA.X86,
    coherence_protocol_required=CoherenceProtocol.MESI_TWO_LEVEL,
    kvm_required=True,
)

from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)

caches = PrivateL1SharedL2CacheHierarchy(
    l1d_size="32KiB",
    l1d_assoc=8,
    l1i_size="32KiB",
    l1i_assoc=8,
    l2_size="256KiB",
    l2_assoc=16,
)

# Main memory
memory = SingleChannelDDR4_2400(size="3GiB")

# This is a switchable CPU. We first boot Ubuntu using KVM, then the guest
# will exit the simulation by calling "m5 exit" (see the `command` variable
# below, which contains the command to be run in the guest after booting).
# Upon exiting from the simulation, the Exit Event handler will switch the
# CPU type (see the ExitEvent.EXIT line below, which contains a map to
# a function to be called when an exit event happens).
processor = SimpleSwitchableProcessor(
    starting_core_type=CPUTypes.KVM,
    switch_core_type=,
    isa=ISA.X86,
    num_cores=1,
)

# Here we tell the KVM CPU (the starting CPU) not to use perf.
for proc in processor.start:
    proc.core.usePerf = False

# Here we setup the board. The X86Board allows for Full-System X86 simulations.
board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=caches,
)

board.set_kernel_disk_workload(
    kernel=obtain_resource("x86-linux-kernel-5.4.0-105-generic"),
    disk_image=obtain_resource("x86-ubuntu-24.04-npb-img"),
    kernel_args=[
            "earlyprintk=ttyS0",
            "console=ttyS0",
            "lpj=7999923",
            "root=/dev/sda2"
        ],
    readfile_contents=f"echo 12345 | sudo -S /home/gem5/NPB3.4-OMP/bin/is.S.x; sleep 5; m5 exit;",
)

def on_work_begin():
    print("Work begin. Switching to detailed CPU")
    m5.stats.reset()
    processor.switch()
    yield False

def on_work_end():
    print("Work end")
    yield True

simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.WORKBEGIN: on_work_begin(),
        ExitEvent.WORKEND: on_work_end(),
    },
)

simulator.run()
