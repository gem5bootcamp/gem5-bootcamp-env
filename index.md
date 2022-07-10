---
layout: index
title: Learning gem5 Bootcamp 2022
---

## Livestream and discussion

You can find links to all of the livestreamed videos on [YouTube](https://www.youtube.com/playlist?list=PL_hVbFs_loVSaSDPr1RJXP5RRFWjBMqq3).

Instead of using YouTube comments, we will be using [Slack](https://app.slack.com/client/T03JNC47S2E/C03PJRJ4RQ8) for our discussions.
You can use the following [invite link](https://join.slack.com/t/gem5-workspace/shared_invite/zt-1aal963w6-_cqn0u8QgBh3GeeSi2Ja7g) to enter the slack.
Once you have joined, type `/join-channel bootcamp-2022` in any text box (e.g., in a DM to yourself) to join the bootcamp channel.

## Tentative schedule

|Session| Topic | Objectives|
| :---  | :---  | :--- |
| Monday Morning | Welcome and Introduction | |
| | Building gem5 |- Learn about the gem5 dependencies <br> - Be introduced to SCons <br> - Understand the different gem5 binary types (opt, debug, fast)|
| | Python basics | - A recap of basic Python skills needed to use gem5 <br> - Object-oriented programming reminder <br> - Run a simple python script in gem5 |
| | Using gem5 basics | - Understand gem5 configuration scripts and its python interpreter <br> - Understand what the `m5` and `gem5` libraries are <br> - Get a general architecture outline of gem5 <br> - Obtain and understand the stats output <br> - Understand the `config.ini` file |
| | About simulation | - Learn about common gem5 terminology: "host", "guest", etc. <br> - Learn about the difference between Full-System and Syscall emulation mode |
| Monday Afternoon | The gem5 standard library | - Use the stdlib components to build a simulated system <br> - Use the stdlib `resource` class to automatically obtain gem5-resources to use in their experiment <br> - Create a gem5 resource custom resource <br> - Set workloads for a simulated system via the `set_workload` functions <br> - Create functions to run on specific exit events <br> - Create an stdlib component|
| | **Welcome dinner** | |
|Tuesday Morning | Using gem5 models | - Use different gem5 CPU models (Timing Simple, Atomic, O3, Minor, Trace, etc.) <br> - Use classic caches in a simulation <br> - Use Ruby caches in a simulation (understand the different coherence protocols, how to compile them and how to create a cache hierarchy via a simple network) |
| | Using gem5 to run things | - Use traffic generators to test memory systems <br> - Incorporate the m5 utility into workloads <br> - Learn to use cross-compilers for non-host ISA workloads <br> - Learn how to output and parse stats|
| Tuesday Afternoon| Full system simulation | - Create a disk image for FS simulations <br> - Create and add and modify gem5 resources <br> - Learn how to use the `m5 readfile` interface|
| | Accelerating Simulation | - Create checkpoints <br> - Load from checkpoints <br> - Fastforward a simulation <br> - Employ sampling techniques <br> - Learn about KVM |
| Wednesday Morning| Creating your own SimObjects| - Understand how a request travels through the system <br> - Implement a SimObject <br> - Learn how to model real-world hardware timing <br> - Learn how to add SimStats and how it maps to real-world hardware <br> - Debug a gem5 SimObject |
| Wednesday Afternoon| Adding your own instructions| - Understand the details of the ISA sub-system <br> - Extend gem5 to simulate an unsupported instruction <br> - Understand the differences between modeling a user-mode and supervisor mode instruction <br> - Understand gem5 debug traces for a particular execution |
| Thursday Morning | Advanced topics in memory systems | - Learn how to extend a packet with a new MemCmd <br> - Learn how to use Garnet (How to create different network topologies with specific characteristics; using the Garnet synthetic traffic; and understanding the output statistics) <br> -  Create and extend cache coherence protocols (create a classic coherence protocol; design a Ruby coherence protocol)|
| Thursday Afternoon | The gem5 GPU Model | [TBD] |
| | **Group Social Event** | |
| Friday Morning | Writing tests and contributing to gem5 | - Write a GTest to test a piece of CPP code <br> - Write a PyUnit test to test a python function <br> - Use testlib to test a gem5 simulation condition <br> - Run Testlib/PyUnit/GUnit tests for gem5 <br> - Understand gem5's quick/Kokoro, long/Nightly, very-long/Weekly test structure <br> - Understand gem5's code-formatting guidelines <br> - Use git to add code to the repo <br> - Review patches on Gerrit <br> - Respond to feedback on Gerrit |
| Friday Afternoon | gem5 extensions and other simulators | - Incorporate SST into a simulation <br> - Incorporate DRAMSim into a simulation <br> - Use SystemC in gem5 and gem5 in SystemC |
| | Wrapping things up | |
