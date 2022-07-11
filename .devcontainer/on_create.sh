#!/bin/bash

# Update the submodules
git submodule update --init --recursive

# Create the stubs
gem5-arm gem5_stubgen.py
gem5-x86 gem5_stubgen.py
gem5-riscv gem5_stubgen.py

mv out typings

# Setups the gem5 source directory
cd gem5

## We cleanup git's 'blame' feature by ignoring certain commits (typically
## commits that have reformatted files)
git config --global blame.ignoreRevsFile .git-blame-ignore-revs

## `git pull` should rebase by default
git config --global pull.rebase true
