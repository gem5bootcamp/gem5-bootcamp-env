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

#include "bootcamp/simple-mem-object/simple_mem_object.hh"

#include "base/trace.hh"
#include "debug/SimpleMemObject.hh"

namespace gem5
{

SimpleMemObject::SimpleMemObject(const Params& params):
    SimObject(params),
    instPort(name() + ".inst_port", this),
    dataPort(name() + ".data_port", this),
    memPort(name() + ".mem_port", this),
    blocked(false)
{}

// TODO: Implement this function.
Port&
SimpleMemObject::getPort(const std::string& if_name, PortID idx)
{
    if (if_name == "inst_port") {
        return instPort;
    } else if (if_name == "data_port") {
        return dataPort;
    } else if (if_name == "mem_port") {
        return memPort;
    } else {
        return SimObject::getPort(if_name, idx);
    }
}

// TODO: Implement this function.
void
SimpleMemObject::CPUSidePort::recvFunctional(PacketPtr pkt)
{
    owner->handleFunctional(pkt);
}

// TODO: Implement this function.
AddrRangeList
SimpleMemObject::CPUSidePort::getAddrRanges() const
{
    return owner->getAddrRanges();
}

void
SimpleMemObject::handleFunctional(PacketPtr pkt)
{
    memPort.sendFunctional(pkt);
}

AddrRangeList
SimpleMemObject::getAddrRanges() const
{
    DPRINTF(SimpleMemObject, "%s: Sending new ranges.\n", __func__);
    return memPort.getAddrRanges();
}

// TODO: Implement this function.
void
SimpleMemObject::MemSidePort::recvRangeChange()
{
    owner->sendRangeChange();
}

void
SimpleMemObject::sendRangeChange()
{
    // sendRangeChange already implemented by ResponsePort.
    instPort.sendRangeChange();
    dataPort.sendRangeChange();
}


// TODO: Implement this function.
bool
SimpleMemObject::CPUSidePort::recvTimingReq(PacketPtr pkt)
{
    if (!owner->handleRequest(pkt)) {
        needRetry = true;
        return false;
    } else {
        return true;
    }

}

// TODO: Implement this function.
bool
SimpleMemObject::handleRequest(PacketPtr pkt)
{
    if (blocked || memPort.blocked() ||
        instPort.blocked() || dataPort.blocked()) {
        return false;
    }

    DPRINTF(SimpleMemObject, "%s: Received a request for addr %#x.\n",
                                            __func__, pkt->getAddr());
    blocked = true;
    memPort.sendPacket(pkt);
    return true;
}

// TODO: Implement this function.
void
SimpleMemObject::MemSidePort::sendPacket(PacketPtr pkt)
{
    panic_if(blockedPacket != nullptr, "Should not try to send if blocked!.");
    if (!sendTimingReq(pkt)) {
        blockedPacket = pkt;
    }
}

// TODO: Implement this function.
void
SimpleMemObject::MemSidePort::recvReqRetry()
{
    assert(blockedPacket != nullptr);
    DPRINTF(SimpleMemObject, "%s: Received a request retry.\n", __func__);

    PacketPtr pkt = blockedPacket;
    blockedPacket = nullptr;
    sendPacket(pkt);
}

// TODO: Implement this function.
bool
SimpleMemObject::MemSidePort::recvTimingResp(PacketPtr pkt)
{
    return owner->handleResponse(pkt);
}


// TODO: Implement this function.
bool
SimpleMemObject::handleResponse(PacketPtr pkt)
{
    assert(blocked);
    DPRINTF(SimpleMemObject, "%s: Received a response for addr %#x.\n",
                                            __func__, pkt->getAddr());

    blocked = false;

    if (pkt->req->isInstFetch()) {
        instPort.sendPacket(pkt);
    } else {
        dataPort.sendPacket(pkt);
    }

    instPort.trySendRetry();
    dataPort.trySendRetry();

    return true;
}

void
SimpleMemObject::CPUSidePort::sendPacket(PacketPtr pkt)
{
    panic_if(blockedPacket != nullptr, "Should never try to send if blocked!");

    if (!sendTimingResp(pkt)) {
        blockedPacket = pkt;
    }
}

void
SimpleMemObject::CPUSidePort::recvRespRetry()
{
    assert(blockedPacket != nullptr);

    PacketPtr pkt = blockedPacket;
    blockedPacket = nullptr;

    sendPacket(pkt);
}

// TODO: Implement this function.
void
SimpleMemObject::CPUSidePort::trySendRetry()
{
    if (needRetry && blockedPacket == nullptr) {
        needRetry = false;
        DPRINTF(SimpleMemObject, "%s: Sending a retry request.\n", __func__);
        sendRetryReq();
    }
}

} // namespace gem5
