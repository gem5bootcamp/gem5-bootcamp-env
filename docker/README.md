This directory contains the sources for the gcr.io/gem5-test/gem5-tutorial-env Docker image which is used by [.devcontainer/Dockerfile](/.devcontainer/Dockerfile) to build the Docker container used by Codespaces.
The gcr.io/gem5-test/gem5-tutorial-env Docker image contains:

* All gem5 dependencies (inc. optional dependencies).
* Prebuilt gem5 binaries:
    * `/usr/local/bin/gem5-x86`
    * `/usr/local/bin/gem5-arm`
    * `/usr/local/bin/gem5-riscv`
* A RISCV64 and an AARCH64 GNU Cross-compiler:
    * RISCV64 GNU cross-compiler in `/opt/cross-compiler/riscv64-linux/`
    * AARCH64 GNU cross-compiler in `/opt/cross-compiler/aarch64-linux/`

## Building

gcr.io/gem5-test/gem5-tutorial-env can be built by executing:

```
make
```

This will build the image in accordance to the [Makefile].
It will pull the necessary Docker images and re-build them as required.
The image built will always contain the latest stable release of gem5 (both the source and compiled binaries).

The gcr.io/gem5-test/gem5-tutorial-env Docker image is built from the [Dockerfile](Dockerfile) file.
It depends on the following images, which are built if not available:

* gcr.io/gem5-test/gem5-builder :
This is built from [Dockerfile-builder](Dockerfile-builder).
It contains prebuilt gem5 binaries.
It is not used directly as it contains the gem5 sources (therefore large).
* gcr.io/gem5-test/gnu-cross-compiler-riscv64 :
This is built from [gnu-cross-compilers/Dockerfile-riscv64](gnu-cross-compilers/Dockerfile-riscv64).
It contains the RISCV64 GNU cross-compiler.
* gcr.io/gem5-test/gnu-cross-compiler-aarch64 :
This is built from [gnu-cross-compilers/Dockerfile-aarch64](gnu-cross-compilers/Dockerfile-aarch64).
It contains the AARCH64 GNU cross-compiler.


## Notes for gem5 developers

These images can be pushed with: `make push`.
Permission must be granted to push to the Google Cloud repository before doing so.
