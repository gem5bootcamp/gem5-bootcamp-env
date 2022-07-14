# Copyright (c) 2021 The Regents of the University of California.
# All Rights Reserved
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

from m5.objects import GarnetNetwork, GarnetExtLink, GarnetIntLink, GarnetRouter, GarnetNetworkInterface


class GarnetPt2Pt(GarnetNetwork):
    """A point-to-point network using garnet.
    """

    def __init__(self, ruby_system):
        super().__init__()


        self.ruby_system = ruby_system

    def connectControllers(self, controllers):
        # Create one router/switch per controller in the system
        self.routers = [
            GarnetRouter(router_id = i) for i in range(len(controllers))
        ]
        self.ext_links = [GarnetExtLink(link_id=i, ext_node=c,
                                        int_node=self.routers[i],
                                        latency = 8)
                          for i, c in enumerate(controllers)]

        self.netifs = [GarnetNetworkInterface(id=i) \
                    for (i,n) in enumerate(self.ext_links)]

        link_count = 0
        self.int_links = []
        for ri in (self.routers):
            for rj in (self.routers):
                if ri == rj: continue # Don't connect a router to itself!
                link_count += 1
                self.int_links.append(GarnetIntLink(link_id = link_count,
                                                    src_node = ri,
                                                    dst_node = rj,
                                                    latency = 8,
                                                    weight  = 1))
