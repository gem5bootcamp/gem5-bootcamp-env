# importing a python library
import math

print(math.log2(128))

# import part of a library
from math import log2

print(log2(256))

# import a local file as a module
from CustomClasses import MyClass

# import gem5's m5 library
# Module structure:
#   src/python/m5
import m5
import m5.objects

# import gem5's standard library
# Module structure:
#   src/python/gem5
import gem5
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
