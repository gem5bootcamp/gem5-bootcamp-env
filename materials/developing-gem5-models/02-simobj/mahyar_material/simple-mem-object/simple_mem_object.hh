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

#ifndef __BOOTCAMP_SIMPLE_MEM_OBJECT_SIMPLE_MEM_OBJECT_HH__
#define __BOOTCAMP_SIMPLE_MEM_OBJECT_SIMPLE_MEM_OBJECT_HH__

namespace gem5
{

#include "mem/port.hh"
#include "params/SimpleMemObject.hh"
#include "sim/sim_object.hh"

class SimpleMemObject : public SimObject
{
  private:
    class CPUSidePort : public ResponsePort
    {
      private:
        SimpleMemObject* owner;

      public:
        CPUSidePort(const std::string& name, SimpleMemObject* owner):
            RequestPort(name, owner), owner(owner)
        {}
        AddrRangeList getAddrRanges() const override;

      protected:
        Tick recvAtomic(PacketPtr pkt) override { panic("recvAtomic unimpl.")}
        void recvFunctional(PacketPtr pkt) override;
        bool recvTimingReq(PacketPtr pkt) override;
        void recvRespRetry() override;
    }

    class MemSidePort : public RequestPort
    {
      private:
        SimpleMemObject* owner;
    }

  public:
    PARAMS(SimpleMemObject);
    SimpleMemObject(const Params& params);
}

} // namespace gem5

#endif // __BOOTCAMP_SIMPLE_MEM_OBJECT_SIMPLE_MEM_OBJECT_HH__