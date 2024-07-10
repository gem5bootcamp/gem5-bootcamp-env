"""
This will start Linux boot on X86DemoBoard and run for 20 billion cycles.
Used as a very simple example.

run with `gem5-mesi 01-basic.py`
"""

from gem5.prebuilt.demo.x86_demo_board import X86DemoBoard
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
