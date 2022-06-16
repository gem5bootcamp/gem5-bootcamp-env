---
title: "Ruby cache part 3: Actions and transitions in state machines"
author: Jason Lowe-Power
---


## Action code blocks

The next section of the state machine file is the action blocks. The
action blocks are executed during a transition from one state to
another, and are called by the transition code blocks (which we will
discuss in the next section \<MSI-transitions-section\>). Actions are
*single action* blocks. Some examples are "send a message to the
directory" and "pop the head of the buffer". Each action should be small
and only perform a single action.

The first action we will implement is an action to send a GetS request
to the directory. We need to send a GetS request to the directory
whenever we want to read some data that is not in the Modified or Shared
states in our cache. As previously mentioned, there are three variables
that are automatically populated inside the action block (like the
`in_msg` in `peek` blocks). `address` is the address that was passed
into the `trigger` function, `cache_entry` is the cache entry passed
into the `trigger` function, and `tbe` is the TBE passed into the
`trigger` function.

```cpp
action(sendGetS, 'gS', desc="Send GetS to the directory") {
    enqueue(request_out, RequestMsg, 1) {
        out_msg.addr := address;
        out_msg.Type := CoherenceRequestType:GetS;
        out_msg.Destination.add(mapAddressToMachine(address,
                                MachineType:Directory));
        // See mem/protocol/RubySlicc_Exports.sm for possible sizes.
        out_msg.MessageSize := MessageSizeType:Control;
        // Set that the requestor is this machine so we get the response.
        out_msg.Requestor := machineID;
    }
}
```

When specifying the action block, there are two parameters: a
description and a "shorthand". These two parameters are used in the HTML
table generation. The shorthand shows up in the transition cell, so it
should be as short as possible. SLICC provides a special syntax to allow
for bold (''), superscript ('\^'), and spaces ('\_') in the shorthand to
help keep them short. Second, the description also shows up in the HTML
table when you click on a particular action. The description can be
longer and help explain what the action does.

Next, in this action we are going to send a message to the directory on
the `request_out` port as declared above the `in_port` blocks. The
`enqueue` function is similar to the `peek` function since it requires a
code block. `enqueue`, however, has the special variable `out_msg`. In
the `enqueue` block, you can modify the `out_msg` with the current data.

The `enqueue` block takes three parameters, the message buffer to send
the message, the type of the message, and a latency. This latency (1
cycle in the example above and throughout this cache controller) is the
*cache latency*. This is where you specify the latency of accessing the
cache, in this case for a miss. Below we will see that specifying the
latency for a hit is similar.

Inside the `enqueue` block is where the message data is populated. For
the address of the request, we can use the automatically populated
`address` variable. We are sending a GetS message, so we use that
message type. Next, we need to specify the destination of the message.
For this, we use the `mapAddressToMachine` function that takes the
address and the machine type we are sending to. This will look up in the
correct `MachineID` based on the address. We call `Destination.add`
because `Destination` is a `NetDest` object, or a bitmap of all
`MachineID`.

Finally, we need to specify the message size (from
`mem/protocol/RubySlicc_Exports.sm`) and set ourselves as the requestor.
By setting this `machineID` as the requestor, it will allow the
directory to respond to this cache or forward it to another cache to
respond to this request.

Similarly, we can create actions for sending other get and put requests.
Note that get requests represent requests for data and put requests
represent requests where we downgrading or evicting our copy of the
data.

```cpp
action(sendGetM, "gM", desc="Send GetM to the directory") {
    enqueue(request_out, RequestMsg, 1) {
        out_msg.addr := address;
        out_msg.Type := CoherenceRequestType:GetM;
        out_msg.Destination.add(mapAddressToMachine(address,
                                MachineType:Directory));
        out_msg.MessageSize := MessageSizeType:Control;
        out_msg.Requestor := machineID;
    }
}

action(sendPutS, "pS", desc="Send PutS to the directory") {
    enqueue(request_out, RequestMsg, 1) {
        out_msg.addr := address;
        out_msg.Type := CoherenceRequestType:PutS;
        out_msg.Destination.add(mapAddressToMachine(address,
                                MachineType:Directory));
        out_msg.MessageSize := MessageSizeType:Control;
        out_msg.Requestor := machineID;
    }
}

action(sendPutM, "pM", desc="Send putM+data to the directory") {
    enqueue(request_out, RequestMsg, 1) {
        out_msg.addr := address;
        out_msg.Type := CoherenceRequestType:PutM;
        out_msg.Destination.add(mapAddressToMachine(address,
                                MachineType:Directory));
        out_msg.DataBlk := cache_entry.DataBlk;
        out_msg.MessageSize := MessageSizeType:Data;
        out_msg.Requestor := machineID;
    }
}
```

Next, we need to specify an action to send data to another cache in the
case that we get a forwarded request from the directory for another
cache. In this case, we have to peek into the request queue to get other
data from the requesting message. This peek code block is exactly the
same as the ones in the `in_port`. When you nest an `enqueue` block in a
`peek` block both `in_msg` and `out_msg` variables are available. This
is needed so we know which other cache to send the data to.
Additionally, in this action we use the `cache_entry` variable to get
the data to send to the other cache.

```cpp
action(sendCacheDataToReq, "cdR", desc="Send cache data to requestor") {
    assert(is_valid(cache_entry));
    peek(forward_in, RequestMsg) {
        enqueue(response_out, ResponseMsg, 1) {
            out_msg.addr := address;
            out_msg.Type := CoherenceResponseType:Data;
            out_msg.Destination.add(in_msg.Requestor);
            out_msg.DataBlk := cache_entry.DataBlk;
            out_msg.MessageSize := MessageSizeType:Data;
            out_msg.Sender := machineID;
        }
    }
}
```

Next, we specify actions for sending data to the directory and sending
an invalidation ack to the original requestor on a forward request when
this cache does not have the data.

```cpp
action(sendCacheDataToDir, "cdD", desc="Send the cache data to the dir") {
    enqueue(response_out, ResponseMsg, 1) {
        out_msg.addr := address;
        out_msg.Type := CoherenceResponseType:Data;
        out_msg.Destination.add(mapAddressToMachine(address,
                                MachineType:Directory));
        out_msg.DataBlk := cache_entry.DataBlk;
        out_msg.MessageSize := MessageSizeType:Data;
        out_msg.Sender := machineID;
    }
}

action(sendInvAcktoReq, "iaR", desc="Send inv-ack to requestor") {
    peek(forward_in, RequestMsg) {
        enqueue(response_out, ResponseMsg, 1) {
            out_msg.addr := address;
            out_msg.Type := CoherenceResponseType:InvAck;
            out_msg.Destination.add(in_msg.Requestor);
            out_msg.DataBlk := cache_entry.DataBlk;
            out_msg.MessageSize := MessageSizeType:Control;
            out_msg.Sender := machineID;
        }
    }
}
```

Another required action is to decrement the number of acks we are
waiting for. This is used when we get a invalidation ack from another
cache to track the total number of acks. For this action, we assume that
there is a valid TBE and modify the implicit `tbe` variable in the
action block.

Additionally, we have another example of making debugging easier in
protocols: `APPEND_TRANSITION_COMMENT`. This function takes a string, or
something that can easily be converted to a string (e.g., `int`) as a
parameter. It modifies the *protocol trace* output, which we will
discuss in the [debugging section](../MSIdebugging). On each
protocol trace line that executes this action it will print the total
number of acks this cache is still waiting on. This is useful since the
number of remaining acks is part of the cache block state.

```cpp
action(decrAcks, "da", desc="Decrement the number of acks") {
    assert(is_valid(tbe));
    tbe.AcksOutstanding := tbe.AcksOutstanding - 1;
    APPEND_TRANSITION_COMMENT("Acks: ");
    APPEND_TRANSITION_COMMENT(tbe.AcksOutstanding);
}
```

We also need an action to store the acks when we receive a message from
the directory with an ack count. For this action, we peek into the
directory's response message to get the number of acks and store them in
the (required to be valid) TBE.

```cpp
action(storeAcks, "sa", desc="Store the needed acks to the TBE") {
    assert(is_valid(tbe));
    peek(response_in, ResponseMsg) {
        tbe.AcksOutstanding := in_msg.Acks + tbe.AcksOutstanding;
    }
    assert(tbe.AcksOutstanding > 0);
}
```

The next set of actions are to respond to CPU requests on hits and
misses. For these actions, we need to notify the sequencer (the
interface between Ruby and the rest of gem5) of the new data. In the
case of a store, we give the sequencer a pointer to the data block and
the sequencer updates the data in-place.

```cpp
action(loadHit, "Lh", desc="Load hit") {
    assert(is_valid(cache_entry));
    cacheMemory.setMRU(cache_entry);
    sequencer.readCallback(address, cache_entry.DataBlk, false);
}

action(externalLoadHit, "xLh", desc="External load hit (was a miss)") {
    assert(is_valid(cache_entry));
    peek(response_in, ResponseMsg) {
        cacheMemory.setMRU(cache_entry);
        // Forward the type of machine that responded to this request
        // E.g., another cache or the directory. This is used for tracking
        // statistics.
        sequencer.readCallback(address, cache_entry.DataBlk, true,
                               machineIDToMachineType(in_msg.Sender));
    }
}

action(storeHit, "Sh", desc="Store hit") {
    assert(is_valid(cache_entry));
    cacheMemory.setMRU(cache_entry);
    // The same as the read callback above.
    sequencer.writeCallback(address, cache_entry.DataBlk, false);
}

action(externalStoreHit, "xSh", desc="External store hit (was a miss)") {
    assert(is_valid(cache_entry));
    peek(response_in, ResponseMsg) {
        cacheMemory.setMRU(cache_entry);
        sequencer.writeCallback(address, cache_entry.DataBlk, true,
                               // Note: this could be the last ack.
                               machineIDToMachineType(in_msg.Sender));
    }
}

action(forwardEviction, "e", desc="sends eviction notification to CPU") {
    if (send_evictions) {
        sequencer.evictionCallback(address);
    }
}
```

In each of these actions, it is vital that we call `setMRU` on the cache
entry. The `setMRU` function is what allows the replacement policy to
know which blocks are most recently accessed. If you leave out the
`setMRU` call, the replacement policy will not operate correctly!

On loads and stores, we call the `read/writeCallback` function on the
`sequencer`. This notifies the sequencer of the new data or allows it to
write the data into the data block. These functions take four parameters
(the last parameter is optional): address, data block, a boolean for if
the original request was a miss, and finally, an optional `MachineType`.
The final optional parameter is used for tracking statistics on where
the data for the request was found. It allows you to track whether the
data comes from cache-to-cache transfers or from memory.

Finally, we also have an action to forward evictions to the CPU. This is
required for gem5's out-of-order models to squash speculative loads if
the cache block is evicted before the load is committed. We use the
parameter specified at the top of the state machine file to check if
this is needed or not.

Next, we have a set of cache management actions that allocate and free
cache entries and TBEs. To create a new cache entry, we must have space
in the `CacheMemory` object. Then, we can call the `allocate` function.
This allocate function doesn't actually allocate the host memory for the
cache entry since this controller specialized the `Entry` type, which is
why we need to pass a `new Entry` to the `allocate` function.

Additionally, in these actions we call `set_cache_entry`,
`unset_cache_entry`, and similar functions for the TBE. These set and
unset the implicit variables that were passed in via the `trigger`
function. For instance, when allocating a new cache block, we call
`set_cache_entry` and in all actions proceeding `allocateCacheBlock` the
`cache_entry` variable will be valid.

There is also an action that copies the data from the cache data block
to the TBE. This allows us to keep the data around even after removing
the cache block until we are sure that this cache no longer are
responsible for the data.

```cpp
action(allocateCacheBlock, "a", desc="Allocate a cache block") {
    assert(is_invalid(cache_entry));
    assert(cacheMemory.cacheAvail(address));
    set_cache_entry(cacheMemory.allocate(address, new Entry));
}

action(deallocateCacheBlock, "d", desc="Deallocate a cache block") {
    assert(is_valid(cache_entry));
    cacheMemory.deallocate(address);
    // clear the cache_entry variable (now it's invalid)
    unset_cache_entry();
}

action(writeDataToCache, "wd", desc="Write data to the cache") {
    peek(response_in, ResponseMsg) {
        assert(is_valid(cache_entry));
        cache_entry.DataBlk := in_msg.DataBlk;
    }
}

action(allocateTBE, "aT", desc="Allocate TBE") {
    assert(is_invalid(tbe));
    TBEs.allocate(address);
    // this updates the tbe variable for other actions
    set_tbe(TBEs[address]);
}

action(deallocateTBE, "dT", desc="Deallocate TBE") {
    assert(is_valid(tbe));
    TBEs.deallocate(address);
    // this makes the tbe variable invalid
    unset_tbe();
}

action(copyDataFromCacheToTBE, "Dct", desc="Copy data from cache to TBE") {
    assert(is_valid(cache_entry));
    assert(is_valid(tbe));
    tbe.DataBlk := cache_entry.DataBlk;
}
```

The next set of actions are for managing the message buffers. We need to
add actions to pop the head message off of the buffers after the message
has been satisfied. The `dequeue` function takes a single parameter, a
time for the dequeue to take place. Delaying the dequeue for a cycle
prevents the `in_port` logic from consuming another message from the
same message buffer in a single cycle.

```cpp
action(popMandatoryQueue, "pQ", desc="Pop the mandatory queue") {
    mandatory_in.dequeue(clockEdge());
}

action(popResponseQueue, "pR", desc="Pop the response queue") {
    response_in.dequeue(clockEdge());
}

action(popForwardQueue, "pF", desc="Pop the forward queue") {
    forward_in.dequeue(clockEdge());
}
```

Finally, the last action is a stall. Below, we are using a "z\_stall",
which is the simplest kind of stall in SLICC. By leaving the action
blank, it generates a "protocol stall" in the `in_port` logic which
stalls all messages from being processed in the current message buffer
and all lower priority message buffer. Protocols using "z\_stall" are
usually simpler, but lower performance since a stall on a high priority
buffer can stall many requests that may not need to be stalled.

```cpp
action(stall, "z", desc="Stall the incoming request") {
    // z_stall
}
```

There are two other ways to deal with messages that cannot currently be
processed that can improve the performance of protocols. (Note: We will
not be using these more complicated techniques in this simple example
protocol.) The first is `recycle`. The message buffers have a `recycle`
function that moves the request on the head of the queue to the tail.
This allows other requests in the buffer or requests in other buffers to
be processed immediately. `recycle` actions often improve the
performance of protocols significantly.

However, `recycle` is not very realistic when compared to real
implementations of cache coherence. For a more realistic
high-performance solution to stalling messages, Ruby provides the
`stall_and_wait` function on message buffers. This function takes the
head request and moves it into a separate structure tagged by an
address. The address is user-specified, but is usually the request's
address. Later, when the blocked request can be handled, there is
another function `wakeUpBuffers(address)` which will wake up all
requests stalled on `address` and `wakeUpAllBuffers()` that wakes up all
of the stalled requests. When a request is "woken up" it is placed back
into the message buffer to be subsequently processed.

## Transition code blocks

Finally, we've reached the final section of the state machine file! This
section contains the details for all of the transitions between states
and what actions to execute during the transition.

So far in this chapter we have written the state machine top to bottom
one section at a time. However, in most cache coherence implementations
you will find that you need to move around between sections. For
instance, when writing the transitions you will realize you forgot to
add an action, or you notice that you actually need another transient
state to implement the protocol. This is the normal way to write
protocols, but for simplicity this chapter goes through the file top to
bottom.

Transition blocks consist of two parts. First, the first line of a
transition block contains the begin state, event to transition on, and
end state (the end state may not be required, as we will discuss below).
Second, the transition block contains all of the actions to execute on
this transition. For instance, a simple transition in the MSI protocol
is transitioning out of Invalid on a Load.

```cpp
transition(I, Load, IS_D) {
    allocateCacheBlock;
    allocateTBE;
    sendGetS;
    popMandatoryQueue;
}
```

First, you specify the transition as the "parameters" to the
`transition` statement. In this case, if the initial state is `I` and
the event is `Load` then transition to `IS_D` (was invalid, going to
shared, waiting for data). This transition is straight out of Table 8.3
in Sorin et al.

Then, inside the `transition` code block, all of the actions that will
execute are listed in order. For this transition first we allocate the
cache block. Remember that in the `allocateCacheBlock` action the newly
allocated entry is set to the entry that will be used in the rest of the
actions. After allocating the cache block, we also allocate a TBE. This
could be used if we need to wait for acks from other caches. Next, we
send a GetS request to the directory, and finally we pop the head entry
off of the mandatory queue since we have fully handled it.

```cpp
transition(IS_D, {Load, Store, Replacement, Inv}) {
    stall;
}
```

In this transition, we use slightly different syntax. According to Table
8.3 from Sorin et al., we should stall if the cache is in IS\_D on
loads, stores, replacements, and invalidates. We can specify a single
transition statement for this by including multiple events in curly
brackets as above. Additionally, the final state isn't required. If the
final state isn't specified, then the transition is executed and the
state is not updated (i.e., the block stays in its beginning state). You
can read the above transition as "If the cache block is in state IS\_D
and there is a load, store, replacement, or invalidate stall the
protocol and do not transition out of the state." You can also use curly
brackets for beginning states, as shown in some of the transitions
below.

Below is the rest of the transitions needed to implement the L1 cache
from the MSI protocol.

```cpp
transition(IS_D, {DataDirNoAcks, DataOwner}, S) {
    writeDataToCache;
    deallocateTBE;
    externalLoadHit;
    popResponseQueue;
}

transition({IM_AD, IM_A}, {Load, Store, Replacement, FwdGetS, FwdGetM}) {
    stall;
}

transition({IM_AD, SM_AD}, {DataDirNoAcks, DataOwner}, M) {
    writeDataToCache;
    deallocateTBE;
    externalStoreHit;
    popResponseQueue;
}

transition(IM_AD, DataDirAcks, IM_A) {
    writeDataToCache;
    storeAcks;
    popResponseQueue;
}

transition({IM_AD, IM_A, SM_AD, SM_A}, InvAck) {
    decrAcks;
    popResponseQueue;
}

transition({IM_A, SM_A}, LastInvAck, M) {
    deallocateTBE;
    externalStoreHit;
    popResponseQueue;
}

transition({S, SM_AD, SM_A, M}, Load) {
    loadHit;
    popMandatoryQueue;
}

transition(S, Store, SM_AD) {
    allocateTBE;
    sendGetM;
    popMandatoryQueue;
}

transition(S, Replacement, SI_A) {
    sendPutS;
    forwardEviction;
}

transition(S, Inv, I) {
    sendInvAcktoReq;
    deallocateCacheBlock;
    forwardEviction;
    popForwardQueue;
}

transition({SM_AD, SM_A}, {Store, Replacement, FwdGetS, FwdGetM}) {
    stall;
}

transition(SM_AD, Inv, IM_AD) {
    sendInvAcktoReq;
    forwardEviction;
    popForwardQueue;
}

transition(SM_AD, DataDirAcks, SM_A) {
    writeDataToCache;
    storeAcks;
    popResponseQueue;
}

transition(M, Store) {
    storeHit;
    popMandatoryQueue;
}

transition(M, Replacement, MI_A) {
    sendPutM;
    forwardEviction;
}

transition(M, FwdGetS, S) {
    sendCacheDataToReq;
    sendCacheDataToDir;
    popForwardQueue;
}

transition(M, FwdGetM, I) {
    sendCacheDataToReq;
    deallocateCacheBlock;
    popForwardQueue;
}

transition({MI_A, SI_A, II_A}, {Load, Store, Replacement}) {
    stall;
}

transition(MI_A, FwdGetS, SI_A) {
    sendCacheDataToReq;
    sendCacheDataToDir;
    popForwardQueue;
}

transition(MI_A, FwdGetM, II_A) {
    sendCacheDataToReq;
    popForwardQueue;
}

transition({MI_A, SI_A, II_A}, PutAck, I) {
    deallocateCacheBlock;
    popForwardQueue;
}

transition(SI_A, Inv, II_A) {
    sendInvAcktoReq;
    popForwardQueue;
}
```

You can download the complete `MSI-cache.sm` file
[here](https://gem5.googlesource.com/public/gem5/+/refs/heads/stable/src/learning_gem5/part3/MSI-cache.sm).
