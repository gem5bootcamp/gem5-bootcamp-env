from m5.objects import *
import m5
import argparse
from m5.objects.DRAMInterface import *
from m5.objects.NVMInterface import *

# sample cmd: build/NULL/gem5.opt --outdir=m5out1 traffGen_example.py DDR3_1600_8x8 linear 100

args = argparse.ArgumentParser()

args.add_argument(
    "mem_dev_type",
    type = str,
    help = "type of memory device, ex: DDR3, NVM, etc."
)

args.add_argument(
    "traffic_mode",
    type = str,
    help = "pattern of generated addresses, linear or random."
)

args.add_argument(
    "rd_prct",
    type=int,
    help="Read Percentage, the rest will be writes, ex: 70",
)

options = args.parse_args()

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "4GHz"
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = 'timing'

system.generator = PyTrafficGen()

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = eval(options.mem_dev_type)(range=AddrRange('8GB'))
system.mem_ctrl.dram.device_size = '1GB'

system.mem_ranges = [AddrRange('8GB')]

system.generator.port = system.mem_ctrl.port

def createRandomTraffic(tgen):
    yield tgen.createRandom(1000000000,                    # duration
                            0,                                   # min_addr
                            AddrRange('1GB').end, # max_adr
                            64,                                  # block_size
                            1000,                  # min_period
                            1000,                  # max_period
                            options.rd_prct,                     # rd_perc
                            0)                                   # data_limit
    yield tgen.createExit(0)

def createLinearTraffic(tgen):
    yield tgen.createLinear(1000000000,                    # duration
                            0,                                   # min_addr
                            AddrRange('1GB').end, # max_adr
                            64,                                  # block_size
                            1000,                  # min_period
                            1000,                  # max_period
                            options.rd_prct,                     # rd_perc
                            0)                                   # data_limit
    yield tgen.createExit(0)


root = Root(full_system=False, system=system)

m5.instantiate()

if options.traffic_mode == 'linear':
    system.generator.start(createLinearTraffic(system.generator))
elif options.traffic_mode == 'random':
    system.generator.start(createRandomTraffic(system.generator))
else:
    print('Wrong traffic type! Exiting!')
    exit()

exit_event = m5.simulate()
