#!/bin/bash

# Update the submodules
git submodule update --init --recursive

# Create the stubs
gem5-arm gem5_stubgen.py
gem5-x86 gem5_stubgen.py
gem5-riscv gem5_stubgen.py

mv out typings
