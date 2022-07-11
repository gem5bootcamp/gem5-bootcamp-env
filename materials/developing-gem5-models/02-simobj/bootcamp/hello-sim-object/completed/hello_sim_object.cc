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

#include "bootcamp/hello-sim-object/hello_sim_object.hh"

#include "base/trace.hh"
#include "debug/HelloExampleFlag.hh"
#include "sim/sim_exit.hh"

namespace gem5
{

HelloSimObject::HelloSimObject(const Params &params):
    SimObject(params),
    event([this]{ processEvent(); }, name() + ".event"),
    latency(params.time_to_wait),
    timesLeft(params.number_of_greets)
{
    DPRINTF(HelloExampleFlag, "%s: Hello World! From a "
                    "SimObject (constructor).\n", __func__);
}

void
HelloSimObject::startup()
{
    DPRINTF(HelloExampleFlag, "%s: HelloWorld! From a "
                    "SimObject (startup).\n", __func__);

    assert(!event.scheduled());

    schedule(event, curTick() + latency);
}

void
HelloSimObject::processEvent()
{
    if (timesLeft > 0) {
        timesLeft--;
        DPRINTF(HelloExampleFlag, "%s: Hello World! Processing an event. "
                                "%d greets left.\n", __func__, timesLeft);
    }

    if (timesLeft == 0) {
        DPRINTF(HelloExampleFlag, "%s: Done greeting.\n", __func__);
        exitSimLoopNow("No greets left.", 0);
    }

    if ((timesLeft > 0) && (!event.scheduled())) {
        schedule(event, curTick() + latency);
    }
}

} // namespace gem5
