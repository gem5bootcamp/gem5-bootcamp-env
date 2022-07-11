/*
 * Copyright (c) 2021 The Regents of the University of California.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include "bootcamp/simple-cache/simple_cache.hh"

#include "base/compiler.hh"
#include "base/random.hh"
#include "debug/SimpleCache.hh"
#include "sim/system.hh"

namespace gem5
{

SimpleCacheObject::SimpleCacheObject(const Params& params) :
    ClockedObject(params),
    latency(params.latency),
    blockSize(params.system->cacheLineSize()),
    capacity(params.size / blockSize),
    memPort(params.name + ".mem_side", this),
    blocked(false), originalPacket(nullptr), waitingPortId(-1), stats(this)
{
    for (int i = 0; i < params.port_cpu_side_connection_count; ++i) {
        cpuPorts.emplace_back(name() + csprintf(".cpu_side[%d]", i), i, this);
    }
}

Port &
SimpleCacheObject::getPort(const std::string &if_name, PortID idx)
{
    if (if_name == "mem_side") {
        panic_if(idx != InvalidPortID,
                 "Mem side of simple cache not a vector port");
        return memPort;
    } else if (if_name == "cpu_side" && idx < cpuPorts.size()) {
        return cpuPorts[idx];
    } else {
        return ClockedObject::getPort(if_name, idx);
    }
}

void
SimpleCacheObject::CPUSidePort::sendPacket(PacketPtr pkt)
{
    panic_if(blockedPacket != nullptr, "Should never try to send if blocked!");

    DPRINTF(SimpleCache, "Sending %s to CPU\n", pkt->print());
    if (!sendTimingResp(pkt)) {
        DPRINTF(SimpleCache, "failed!\n");
        blockedPacket = pkt;
    }
}

AddrRangeList
SimpleCacheObject::CPUSidePort::getAddrRanges() const
{
    return owner->getAddrRanges();
}

void
SimpleCacheObject::CPUSidePort::trySendRetry()
{
    if (needRetry && blockedPacket == nullptr) {
        needRetry = false;
        DPRINTF(SimpleCache, "Sending retry req.\n");
        sendRetryReq();
    }
}

void
SimpleCacheObject::CPUSidePort::recvFunctional(PacketPtr pkt)
{
    return owner->handleFunctional(pkt);
}

// TODO: SimpleCache::CPUSidePort::recvTimingReq(PacketPtr pkt)

void
SimpleCacheObject::CPUSidePort::recvRespRetry()
{
    assert(blockedPacket != nullptr);

    PacketPtr pkt = blockedPacket;
    blockedPacket = nullptr;

    DPRINTF(SimpleCache, "Retrying response pkt %s\n", pkt->print());

    sendPacket(pkt);

    trySendRetry();
}

void
SimpleCacheObject::MemSidePort::sendPacket(PacketPtr pkt)
{
    panic_if(blockedPacket != nullptr, "Should never try to send if blocked!");

    if (!sendTimingReq(pkt)) {
        blockedPacket = pkt;
    }
}

bool
SimpleCacheObject::MemSidePort::recvTimingResp(PacketPtr pkt)
{
    return owner->handleResponse(pkt);
}

void
SimpleCacheObject::MemSidePort::recvReqRetry()
{
    assert(blockedPacket != nullptr);

    PacketPtr pkt = blockedPacket;
    blockedPacket = nullptr;

    sendPacket(pkt);
}

void
SimpleCacheObject::MemSidePort::recvRangeChange()
{
    owner->sendRangeChange();
}

// TODO: SimpleCache::handleRequest(PacketPtr pkt, int port_id)

// TODO: SimpleCache::handleResponse(PacketPtr pkt)

// TODO: SimpleCache::sendResponse(PacketPtr pkt)

void
SimpleCacheObject::handleFunctional(PacketPtr pkt)
{
    if (accessFunctional(pkt)) {
        pkt->makeResponse();
    } else {
        memPort.sendFunctional(pkt);
    }
}

// TODO: SimpleCacheObject::accessTiming(PacketPtr pkt)

// TODO: SimpleCacheObject::accessFunctional(PacketPtr pkt)

// TODO: SimpleCacheObject::insert(PacketPtr pkt)

AddrRangeList
SimpleCacheObject::getAddrRanges() const
{
    DPRINTF(SimpleCache, "Sending new ranges\n");
    return memPort.getAddrRanges();
}

void
SimpleCacheObject::sendRangeChange() const
{
    for (auto& port : cpuPorts) {
        port.sendRangeChange();
    }
}

SimpleCacheObject::SimpleCacheObjectStats::SimpleCacheObjectStats(
    statistics::Group* parent): statistics::Group(parent),
    ADD_STAT(hits, statistics::units::Count::get(), "Number of hits"),
    ADD_STAT(misses, statistics::units::Count::get(), "Number of misses"),
    ADD_STAT(missLatency, statistics::units::Tick::get(),
            "Ticks for misses to the cache"),
    ADD_STAT(hitRatio, statistics::units::Ratio::get(),
            "The ratio of hits to the total accesses to the cache",
            hits / (hits + misses))
{
    missLatency.init(16);
}

} // namespace gem5
