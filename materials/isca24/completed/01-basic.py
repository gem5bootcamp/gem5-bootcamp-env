"""
This will start Linux boot on X86DemoBoard and run for 20 billion cycles.
Used as a very simple example.

run with `gem5-mesi 01-basic.py`
"""

from gem5.prebuilt.demo.x86_demo_board import X86DemoBoard
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

board = X86DemoBoard()
board.set_workload(obtain_resource("x86-ubuntu-24.04-boot-no-systemd"))

simulator = Simulator(board=board)
simulator.run(20_000_000_000)
