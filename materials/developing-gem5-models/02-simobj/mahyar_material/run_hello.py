# TODO: License goes here.

import m5
from m5.objects import *

root = Root(full_system=False)

root.hello = HelloObject()

m5.instantiate()

print("Beginning Simulation")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
