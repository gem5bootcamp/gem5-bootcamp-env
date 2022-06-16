---
title: Developing cache coherence protocols in Ruby
author: "Jason Lowe-Power"
---

## Ruby cache coherence model and SLICC language

Ruby comes from the [multifacet GEMS project](http://research.cs.wisc.edu/gems/).
Ruby provides a detailed cache memory and cache coherence models as well as a detailed network model (Garnet).

Ruby is flexible. It can model many different kinds of coherence
implementations, including broadcast, directory, token, region-based
coherence, and is simple to extend to new coherence models.

Ruby is a mostly drop-in replacement for the classic memory system.
There are interfaces between the classic gem5 MemObjects and Ruby, but
for the most part, the classic caches and Ruby are not compatible.

In this part of the book, we will first go through creating an example
protocol from the protocol description to debugging and running the
protocol.

Before diving into a protocol, we will first talk about some of the
architecture of Ruby. The most important structure in Ruby is the
controller, or state machine. Controllers are implemented by writing a
SLICC state machine file.

SLICC is a domain-specific language (Specification Language including
Cache Coherence) for specifying coherence protocols. SLICC files end in
".sm" because they are *state machine* files. Each file describes
states, transitions from a begin to an end state on some event, and
actions to take during the transition.

Each coherence protocol is made up of multiple SLICC state machine
files. These files are compiled with the SLICC compiler which is written
in Python and part of the gem5 source. The SLICC compiler takes the
state machine files and output a set of C++ files that are compiled with
all of gem5's other files. These files include the SimObject declaration
file as well as implementation files for SimObjects and other C++
objects.

Currently, gem5 supports compiling only a single coherence protocol at a
time. For instance, you can compile MI\_example into gem5 (the default,
poor performance, protocol), or you can use MESI\_Two\_Level. But, to
use MESI\_Two\_Level, you have to recompile gem5 so the SLICC compiler
can generate the correct files for the protocol. We discuss this further
in the compilation section \<MSI-building-section\>

Now, let's dive into implementing our first coherence protocol!

## More on the relation between SLICC and C++ files in Ruby

- Structures that are used in the SLICC files
- How to navigate the code
- `RubySystem` object
- Overall structure of the Ruby "black box" design
- How the network fits into this

## MSI example cache protocol

Before we implement a cache coherence protocol, it is important to have
a solid understanding of cache coherence. This section leans heavily on
the great book *A Primer on Memory Consistency and Cache Coherence* by
Daniel J. Sorin, Mark D. Hill, and David A. Wood which was published as
part of the Synthesis Lectures on Computer Architecture in 2011
([DOI:10.2200/S00346ED1V01Y201104CAC016](https://doi.org/10.2200/S00346ED1V01Y201104CAC016)).
If you are unfamiliar with cache coherence, I strongly advise reading that book before continuing.

In this chapter, we will be implementing an MSI protocol.
(An MSI protocol has three stable states, modified with read-write permission, shared with read-only permission, and invalid with no permissions.)
We will implement this as a three-hop directory protocol (i.e., caches can send data directly to other caches without going through the directory).
Details for the protocol can be found in Section 8.2 of *A Primer on Memory Consistency and Cache Coherence* (pages 141-149).
It will be helpful to print out Section 8.2 to reference as you are implementing the protocol.

You can download an exceprt of Sorin et al. that contains Section 8.2 [here](/_pages/static/external/Sorin_et-al_Excerpt_8.2.pdf).

## First steps to writing a protocol

Let's start by creating a new directory for our protocol at src/learning\_gem5/MSI\_protocol.
In this directory, like in all gem5 source directories, we need to create a file for SCons to know what to compile.
However, this time, instead of creating a `SConscript` file, we are
going to create a `SConsopts` file. (The `SConsopts` files are processed
before the `SConscript` files and we need to run the SLICC compiler
before SCons executes.)

We need to create a `SConsopts` file with the following:

```python
Import('*')

main.Append(ALL_PROTOCOLS=['MSI'])

main.Append(PROTOCOL_DIRS=[Dir('.')])
```

We do two things in this file. First, we register the name of our
protocol (`'MSI'`). Since we have named our protocol MSI, SCons will
assume that there is a file named `MSI.slicc` which specifies all of the
state machine files and auxiliary files. We will create that file after
writing all of our state machine files. Second, the `SConsopts` files
tells the SCons to look in the current directory for files to pass to
the SLICC compiler.

### Writing a state machine file

The next step, and most of the effort in writing a protocol, is to
create the state machine files. State machine files generally follow the
outline:

Parameters
:   These are the parameters for the SimObject that will be generated
    from the SLICC code.

Declaring required structures and functions
:   This section declares the states, events, and many other required
    structures for the state machine.

In port code blocks
:   Contain code that looks at incoming messages from the (`in_port`)
    message buffers and determines what events to trigger.

Actions
:   These are simple one-effect code blocks (e.g., send a message) that
    are executed when going through a transition.

Transitions
:   Specify actions to execute given a starting state and an event and
    the final state. This is the meat of the state machine definition.

Over the next few sections we will go over how to write each of these components of the protocol.
