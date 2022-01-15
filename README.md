This repository has been designed for use in gem5 tutorials.
It is built with the assumption users will utilize [Codespaces](https://github.com/features/codespaces) to learn gem5.

The repository contains the following directories:

* [docker](docker) :
The source code for the Docker image used by [.devcontainer/Dockerfile](.devcontainer/Dockerfile) to create the Codespace Docker container.
* [gem5](gem5) :
v21.2 of gem5.
* [gem5-resources](gem5-resources):
gem5-resources which may be used with v21.2 of gem5.

**Note:** [docker](docker) and [gem5](gem5) are submodules though the [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json) file specifies a `git module update --init --recursive` command is called when the Codespace Docker container is created.

The container, used by Codespaces, is build from [.devcontainer/Dockerfile](.devcontainer/Dockerfile).
It

* Contains all gem5 dependencies (inc. optional dependencies).
* Prebuilt gem5 binaries:
    - `/usr/local/bin/gem5-x86`
    - `/usr/local/bin/gem5-arm`
    - `/usr/local/bin/gem5-riscv`
* A RISCV64 and an AARCH64 GNU cross-compiler:
    * RISCV64 GNU cross-compiler found in `/opt/cross-compiler/riscv64-linux/`.
    * AARCH64 GNU cross-compiler found in `/opt/cross-compiler/aarch64-linux/`.

## Beginners example

The following can be used to run a basic gem5 simulation straight away:

```
gem5-arm gem5/configs/example/gem5_library/arm-hello.py`
```

This will execute a "Hello world!" program inside a simulated ARM system.
