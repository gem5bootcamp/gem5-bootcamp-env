"""
A small multisim example

Run with `gem5 -m gem5.utils.multisim 07-multisim.py`
or with `gem5 07-multisim.py -l` to list the ids of the simulators.
or with `gem5 07-multisim.py riscv-npb-is-size-s-run` to run one simulation

Running all situations on 8 cores takes about 4 minutes since there are 9
workloads
Running just IS takes about 1 minute
Most workloads finish within 2 minutes.
"""

from gem5.prebuilt.riscvmatched.riscvmatched_board import RISCVMatchedBoard
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

from gem5.utils.multisim import add_simulator

board = RISCVMatchedBoard()

for workload in obtain_resource("riscv-getting-started-benchmark-suite"):
    board.set_workload(workload)
    simulator = Simulator(board=board, id=workload.get_id())

    add_simulator(simulator)
