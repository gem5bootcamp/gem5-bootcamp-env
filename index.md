---
layout: index
title: Learning gem5 Bootcamp 2024
---

Welcome to the gem5 Bootcamp!

[Register for the 2024 gem5 Bootcamp](https://na.eventscloud.com/ereg/index.php?eventid=799532&){: .btn .btn-lg .btn-primary}

As the premier destination for computer architecture enthusiasts and researchers, our bootcamp offers an immersive experience into the world of architectural simulation and modeling.
Whether you're a student eager to learn, a professional looking to sharpen your skills, or a researcher seeking to push the boundaries of technology, the gem5 Bootcamp is your gateway to mastering the gem5 simulator.

Join us to explore the intricate workings of modern computer systems, engage with experts in the field, and collaborate with peers from around the globe.
With hands-on sessions, in-depth tutorials, and challenging projects, you'll gain practical knowledge and experience that will propel your understanding and innovation in computer architecture.

Dive into the dynamic world of simulation with the gem5 Bootcamp, and emerge equipped to tackle the computational challenges of tomorrow.

We also held a [gem5 Bootcamp in 2022](https://gem5bootcamp.github.io/gem5-bootcamp-env/) which you can check out for more information.
Videos from that bootcamp are available [on YouTube](https://www.youtube.com/watch?v=orASbQ02pDw&list=PL_hVbFs_loVSaSDPr1RJXP5RRFWjBMqq3).

## Tentative schedule for 2024

The bootcamp will be held from July 29th to August 2nd, 2024.
The bootcamp will run from 9am-4pm each day in the [UC Davis Conference Center](https://conferencecenter.ucdavis.edu/).

The full five day registration runs Monday-Friday.
The three day registration runs Tuesday-Thursday.

**Note: The links on this website are under construction and will be updated as the bootcamp approaches.**

- **Day 1: Computer architecture and computer architectures simulation 101**
  - **Morning:**
    - Introduction to computer architecture simulation
    - Introduction to gem5
    - Running gem5
    - gem5's input and output
    - Python language reminder
  - **Afternoon:**
    - Exercises with gem5
    - Discussions on research plans and preview the rest of the bootcamp
- **Day 2: gem5 basics**
  - **Morning: Configuring and running gem5 with pre-built resources**
    - gem5 Standard Library
      - Using stdlib components
      - Extending stdlib components
      - Using the `Simulator` object
      - Customizing exit operations
    - gem5 Resources
      - Using pre-built resources from <resources.gem5.org>
      - Kinds of resources: disk images, kernels, binaries, workloads, suites
      - Creating your own resources
        - Using local resources
        - Extending disk images (more on FS mode later)
    - gem5 basics
      - Building gem5, dependencies, SCons
      - Understanding gem5's build options
      - Available gem5 models
        - CPU models
        - Memory models
        - Cache models
        - Device and other models
  - **Afternoon: Using gem5 for computer system evaluation**
    - Deep dive on inputs to gem5
      - Traffic generators
      - Building binaries for gem5 and cross compiling
      - Marking regions of interest and the `gem5-bridge` (`m5`) library
    - Full system simulation
      - Required pieces
      - Creating disk images
      - `gem5-bridge` application
      - Bundling FS resources together into `Workload`s
    - Accelerating simulation
      - Fast-fowarding
      - KVM-based CPU
      - Checkpointing
      - Sampling
- **Day 3: Advanced gem5 uses and beginning gem5 development**
  - **Morning: Advanced gem5 uses**
    - gem5's GPU model
      - Introduction to the GPU model
      - Requirements for running the GPU model
      - GPU resources
      - Limitations of the GPU model
  - **Afternoon: Getting started with gem5 development**
    - Getting started with gem5 development and setting up a development environment
    - Creating your own `SimObject`s
      - Understand how a request travels through the system
      - Implement a SimObject
      - Learn how to model real-world hardware timing
      - Learn how to add SimStats and how it maps to real-world hardware
      - Debug a gem5 SimObject
- **Day 4: Advanced gem5 development**
  - **Morning: gem5's memory system**
    - Learn how to extend a packet with a new MemCmd
    - Learn how to use Garnet (How to create different network topologies with specific characteristics; using the Garnet synthetic traffic; and understanding the output statistics)
    - Create and extend cache coherence protocols (create a classic coherence protocol; design a Ruby coherence protocol)
- **Afternoon: gem5's execution model and adding new instructions**
  - Understand the details of the ISA sub-system
  - Extend gem5 to simulate an unsupported instruction
  - Understand the differences between modeling a user-mode and supervisor mode instruction
  - Understand gem5 debug traces for a particular execution
- **Day 5: Integrations with other simulators and contributing to gem5**
  - **Morning: Integrations with other simulators**
    - gem5's integration with other simulators
      - SystemC in gem5 & gem5 in SystemC
      - DRAMSys
      - DRAMSim
      - gem5 + [SST](https://sst-simulator.org/)
  - **Afternoon: Contributing to gem5**
    - Overview of gem5 governance model
    - Contributing to gem5
      - Understand the gem5 contribution process
      - Learn how to write a gem5 patch
      - Learn how to review a gem5 patch
      - Using git with gem5
    - gem5 testing
