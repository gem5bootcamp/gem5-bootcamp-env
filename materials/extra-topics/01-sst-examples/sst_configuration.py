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

import sst
import sys
import os

from sst import UnitAlgebra

cache_link_latency = "1ps"

bbl = "riscv-boot-exit-nodisk"
cpu_clock_rate = "3GHz"
# gem5 will send requests to physical addresses of range [0x80000000, inf) to memory
# currently, we do not subtract 0x80000000 from the request's address to get the "real" address
# so, the mem_size would always be 2GiB larger than the desired memory size
memory_size_gem5 = "4GiB"
memory_size_sst = "6GiB"
addr_range_end = UnitAlgebra(memory_size_sst).getRoundedValue()

l1_params = {
    "access_latency_cycles" : "1",
    "cache_frequency" : cpu_clock_rate,
    "replacement_policy" : "lru",
    "coherence_protocol" : "MESI",
    "associativity" : "4",
    "cache_line_size" : "64",
    "cache_size" : "4 KiB",
    "L1" : "1",
}

cpu_params = {
    "frequency": cpu_clock_rate,
    "cmd": " ../../configs/example/sst/riscv_fs.py --cpu-clock-rate {} --memory-size {}".format(cpu_clock_rate, memory_size_gem5),
    "debug_flags": ""
}

gem5_node = sst.Component("gem5_node", "gem5.gem5Component")
gem5_node.addParams(cpu_params)

cache_bus = sst.Component("cache_bus", "memHierarchy.Bus")
cache_bus.addParams( { "bus_frequency" : cpu_clock_rate } )

system_port = gem5_node.setSubComponent("system_port", "gem5.gem5Bridge", 0) # for initialization
system_port.addParams({ "response_receiver_name": "system.system_outgoing_bridge"}) # tell the SubComponent the name of the corresponding SimObject

cache_port = gem5_node.setSubComponent("cache_port", "gem5.gem5Bridge", 0) # SST -> gem5
cache_port.addParams({ "response_receiver_name": "system.memory_outgoing_bridge"})

# L1 cache
l1_cache = sst.Component("l1_cache", "memHierarchy.Cache")
l1_cache.addParams(l1_params)

# Memory
memctrl = sst.Component("memory", "memHierarchy.MemController")
memctrl.addParams({
    "debug" : "0",
    "clock" : "1GHz",
    "request_width" : "64",
    "addr_range_end" : addr_range_end, # should be changed accordingly to memory_size_sst
})
memory = memctrl.setSubComponent("backend", "memHierarchy.simpleMem")
memory.addParams({
    "access_time" : "30ns",
    "mem_size" : memory_size_sst
})

# Connections
# cpu <-> L1
cpu_cache_link = sst.Link("cpu_l1_cache_link")
cpu_cache_link.connect(
    (cache_port, "port", cache_link_latency),
    (cache_bus, "high_network_0", cache_link_latency)
)
system_cache_link = sst.Link("system_cache_link")
system_cache_link.connect(
    (system_port, "port", cache_link_latency),
    (cache_bus, "high_network_1", cache_link_latency)
)
cache_bus_cache_link = sst.Link("cache_bus_cache_link")
cache_bus_cache_link.connect(
    (cache_bus, "low_network_0", cache_link_latency),
    (l1_cache, "high_network_0", cache_link_latency)
)
# L1 <-> mem
cache_mem_link = sst.Link("l1_cache_mem_link")
cache_mem_link.connect(
    (l1_cache, "low_network_0", cache_link_latency),
    (memctrl, "direct_link", cache_link_latency)
)

# enable Statistics
stat_params = { "rate" : "0ns" }
sst.setStatisticLoadLevel(5)
sst.setStatisticOutput("sst.statOutputTXT", {"filepath" : "./sst-stats.txt"})
sst.enableAllStatisticsForComponentName("l1_cache", stat_params)
sst.enableAllStatisticsForComponentName("memory", stat_params)
