/*
 * Copyright (c) 2017 Jason Lowe-Power
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

#include "tutorial/my_hello_object.hh"

#include "base/logging.hh"
#include "base/trace.hh"
#include "debug/MyHelloExample.hh"

namespace gem5
{

MyHelloObject::MyHelloObject(const Params &params) :
    SimObject(params),
    // Initialize the event

    // Initialize the goodbye object

    // Grab something from params

    // Grab the latency parameter

    // Grab the timesLeft parameter
{
    // It's a good idea to have debugging!
    DPRINTF(MyHelloExample, "Created the hello object named %s\n", myName);

    // Make sure to check that the user provides what you expect them to
}

void
MyHelloObject::startup()
{
    // Before simulation starts, we need to schedule the event

}

void
MyHelloObject::processEvent()
{
    // Count the number of times left

    // if the timesLeft is over, then print "Done firing!"
    // Otherwise, schedule this event to happen with a certain latency
}

} // namespace gem5
