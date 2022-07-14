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

#include "bootcamp/simple-cache-object/simple_cache_object.hh"

#include "base/compiler.hh"
#include "base/random.hh"
#include "debug/SimpleCacheObject.hh"
#include "sim/system.hh"

namespace gem5
{

SimpleCacheObject::SimpleCacheObject(const Params& params) :
    ClockedObject(params),
    latency(params.latency),
    blockSize(params.system->cacheLineSize()),
    capacity(params.size / blockSize),
    memPort(params.name + ".mem_side", this),
    blocked(false), outstandingPacket(nullptr), waitingPortId(-1), stats(this)
{
    for (int i = 0; i < params.port_cpu_side_connection_count; ++i) {
        cpuPorts.emplace_back(name() + csprintf(".cpu_side[%d]", i), i, this);
    }
}

// TODO: Implement this function.
Port &
SimpleCacheObject::getPort(const std::string &if_name, PortID idx)
{

}

void
SimpleCacheObject::CPUSidePort::sendPacket(PacketPtr pkt)
{
    panic_if(blockedPacket != nullptr, "Should never try to send if blocked!");

    DPRINTF(SimpleCacheObject, "Sending %s to CPU\n", pkt->print());
    if (!sendTimingResp(pkt)) {
        DPRINTF(SimpleCacheObject, "failed!\n");
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
        DPRINTF(SimpleCacheObject, "Sending retry req.\n");
        sendRetryReq();
    }
}

void
SimpleCacheObject::CPUSidePort::recvFunctional(PacketPtr pkt)
{
    return owner->handleFunctional(pkt);
}

bool
SimpleCacheObject::CPUSidePort::recvTimingReq(PacketPtr pkt)
{
    if (!owner->handleRequest(pkt, id)) {
        needRetry = true;
        return false;
    } else {
        return true;
    }
}

void
SimpleCacheObject::CPUSidePort::recvRespRetry()
{
    assert(blockedPacket != nullptr);

    PacketPtr pkt = blockedPacket;
    blockedPacket = nullptr;

    DPRINTF(SimpleCacheObject, "Retrying response pkt %s\n", pkt->print());

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

// TODO: Implement this function.
bool
SimpleCacheObject::handleRequest(PacketPtr pkt, int port_id)
{

}

// TODO: Implement this function.
bool
SimpleCacheObject::handleResponse(PacketPtr pkt)
{

}

// TODO: Implement this function.
void
SimpleCacheObject::sendResponse(PacketPtr pkt)
{
    int port = waitingPortId;

    blocked = false;
    waitingPortId = -1;

    cpuPorts[port].sendPacket(pkt);
    for (auto& port : cpuPorts) {
        port.trySendRetry();
    }
}

void
SimpleCacheObject::handleFunctional(PacketPtr pkt)
{
    memPort.sendFunctional(pkt);
}

void
SimpleCacheObject::accessTiming(PacketPtr pkt)
{
    bool hit = accessFunctional(pkt);
    DPRINTF(SimpleCacheObject, "%s: Received a timing request for addr %#x.\n",
                                                    __func__, pkt->getAddr());
    if (hit) {
        DPRINTF(SimpleCacheObject, "%s: It is a hit.\n", __func__);
        pkt->makeResponse();
        sendResponse(pkt);
    } else {
        DPRINTF(SimpleCacheObject, "%s: It is a miss.\n", __func__);
        Addr addr = pkt->getAddr();
        Addr block_addr = pkt->getBlockAddr(blockSize);
        unsigned size = pkt->getSize();
        if (addr == block_addr && size == blockSize) {
            DPRINTF(SimpleCacheObject, "%s: The packet is of the cache block "
                                    "size and is to an aligned addr. Just "
                                    "forward the packet to mem.\n", __func__);
            memPort.sendPacket(pkt);
        } else {
            panic_if(addr - block_addr + size > blockSize,
                     "Cannot handle accesses that span multiple cache lines");
            DPRINTF(SimpleCacheObject, "%s: The packet is smaller than the "
                                    "cache block.\n", __func__);
            DPRINTF(SimpleCacheObject, "Upgrading packet to block size\n");

            assert(pkt->needsResponse());
            MemCmd cmd;
            if (pkt->isWrite() || pkt->isRead()) {
                cmd = MemCmd::ReadReq;
            } else {
                panic("Unknown packet type in upgrade size");
            }

            PacketPtr new_pkt = new Packet(pkt->req, cmd, blockSize);
            new_pkt->allocate();

            outstandingPacket = pkt;

            DPRINTF(SimpleCacheObject, "%s: Forward the upgraded packet "
                                    "to mem.\n", __func__);
            memPort.sendPacket(new_pkt);
        }
    }
}

bool
SimpleCacheObject::accessFunctional(PacketPtr pkt)
{
    Addr block_addr = pkt->getBlockAddr(blockSize);
    auto it = cacheStore.find(block_addr);
    if (it != cacheStore.end()) {
        if (pkt->isWrite()) {
            pkt->writeDataToBlock(it->second, blockSize);
        } else if (pkt->isRead()) {
            pkt->setDataFromBlock(it->second, blockSize);
        } else {
            panic("Unknown packet type!");
        }
        return true;
    }
    return false;
}

void
SimpleCacheObject::insert(PacketPtr pkt)
{
    if (cacheStore.size() >= capacity) {
        // Select random thing to evict. This is a little convoluted since we
        // are using a std::unordered_map. See http://bit.ly/2hrnLP2
        int bucket, bucket_size;
        do {
            bucket = random_mt.random(0, (int)cacheStore.bucket_count() - 1);
        } while ( (bucket_size = cacheStore.bucket_size(bucket)) == 0 );
        auto block = std::next(cacheStore.begin(bucket),
                               random_mt.random(0, bucket_size - 1));

        RequestPtr req = std::make_shared<Request>(
                                    block->first, blockSize, 0, 0);
        PacketPtr new_pkt = new Packet(req, MemCmd::WritebackDirty, blockSize);
        new_pkt->dataDynamic(block->second); // This will be deleted later

        DPRINTF(SimpleCacheObject, "Writing packet back %s\n", pkt->print());
        memPort.sendTimingReq(new_pkt);

        cacheStore.erase(block->first);
    }
    uint8_t *data = new uint8_t[blockSize];
    cacheStore[pkt->getAddr()] = data;

    pkt->writeDataToBlock(data, blockSize);
}

AddrRangeList
SimpleCacheObject::getAddrRanges() const
{
    DPRINTF(SimpleCacheObject, "Sending new ranges\n");
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
