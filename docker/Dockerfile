FROM gcr.io/gem5-test/ubuntu-20.04_all-dependencies:stable

# Obtain the build gem5 binaries.
COPY --from=gcr.io/gem5-test/gem5-builder:latest /gem5/build/X86/gem5.fast /usr/local/bin/gem5-x86
COPY --from=gcr.io/gem5-test/gem5-builder:latest /gem5/build/ARM/gem5.fast /usr/local/bin/gem5-arm
COPY --from=gcr.io/gem5-test/gem5-builder:latest /gem5/build/RISCV/gem5.fast /usr/local/bin/gem5-riscv

# Obtain the cross compilers
RUN mkdir /opt/cross-compiler

COPY --from=gcr.io/gem5-test/gnu-cross-compiler-aarch64:latest /opt/cross-compiler/aarch64-linux /opt/cross-compiler/aarch64-linux
ENV PATH="/opt/cross-compiler/aarch64-linux/bin:${PATH}"

COPY --from=gcr.io/gem5-test/gnu-cross-compiler-riscv64:latest /opt/cross-compiler/riscv64-linux /opt/cross-compiler/riscv64-linux
ENV PATH="/opt/cross-compiler/riscv64-linux/bin:${PATH}"

# Install the APT dependencies
RUN apt -y update && apt install -y gdb curl vim

# Install the Python library dependencies
RUN pip install black pandas matplotlib numpy seaborn
