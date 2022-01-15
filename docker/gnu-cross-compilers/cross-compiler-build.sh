#! /bin/bash
set -e
trap 'previous_command=$this_command; this_command=$BASH_COMMAND' DEBUG
trap 'echo FAILED COMMAND: $previous_command' EXIT

#-------------------------------------------------------------------------------------------
# This script will download packages for, configure, build and install a GCC cross-compiler.
# Customize the variables (INSTALL_PATH, TARGET, etc.) to your liking before running.
# If you get an error and need to resume the script from some point in the middle,
# just delete/comment the preceding lines before running it again.
#
# See: http://preshing.com/20141119/how-to-build-a-gcc-cross-compiler
#-------------------------------------------------------------------------------------------

TARGET=$1
LINUX_ARCH=$2
INSTALL_PATH=/opt/cross-compiler/${TARGET}
CONFIGURATION_OPTIONS="--disable-multilib" # --disable-threads --disable-shared
PARALLEL_MAKE=-j`nproc`
BINUTILS_VERSION=binutils-2.35
GCC_VERSION=gcc-10.2.0
LINUX_KERNEL_VERSION=linux-5.8
GLIBC_VERSION=glibc-2.32
MPFR_VERSION=mpfr-4.1.0
GMP_VERSION=gmp-6.2.0
MPC_VERSION=mpc-1.0.2
ISL_VERSION=isl-0.18
CLOOG_VERSION=cloog-0.18.1
export PATH=$INSTALL_PATH/bin:$PATH

mkdir -p ${INSTALL_PATH}

# Download packages
export http_proxy=$HTTP_PROXY https_proxy=$HTTP_PROXY ftp_proxy=$HTTP_PROXY
wget -nc https://ftp.gnu.org/gnu/binutils/$BINUTILS_VERSION.tar.gz
wget -nc https://ftp.gnu.org/gnu/gcc/$GCC_VERSION/$GCC_VERSION.tar.gz
wget -nc https://www.kernel.org/pub/linux/kernel/v5.x/$LINUX_KERNEL_VERSION.tar.xz
wget -nc https://ftp.gnu.org/gnu/glibc/$GLIBC_VERSION.tar.xz

# Extract everything
for f in *.tar*; do tar xfk $f; done

# Binutils
mkdir -p build-binutils
cd build-binutils
../$BINUTILS_VERSION/configure --prefix=$INSTALL_PATH --target=$TARGET $CONFIGURATION_OPTIONS
make $PARALLEL_MAKE
make install
cd ..

# Linux Kernel Headers
cd $LINUX_KERNEL_VERSION
make ARCH=$LINUX_ARCH INSTALL_HDR_PATH=$INSTALL_PATH/$TARGET headers_install
cd ..

# Obtain the GCC Prerequisites
cd $GCC_VERSION
./contrib/download_prerequisites
cd ..

# C/C++ Compilers
mkdir -p build-gcc
cd build-gcc
../$GCC_VERSION/configure --prefix=$INSTALL_PATH --target=$TARGET --enable-languages=c,c++ --disable-libsanitizer $CONFIGURATION_OPTIONS $NEWLIB_OPTION
make $PARALLEL_MAKE all-gcc
make install-gcc
cd ..

# Standard C Library Headers and Startup Files
mkdir -p build-glibc
cd build-glibc
../$GLIBC_VERSION/configure --prefix=$INSTALL_PATH/$TARGET --build=$MACHTYPE --host=$TARGET --target=$TARGET --with-headers=$INSTALL_PATH/$TARGET/include $CONFIGURATION_OPTIONS libc_cv_forced_unwind=yes
make install-bootstrap-headers=yes install-headers
make $PARALLEL_MAKE csu/subdir_lib
install csu/crt1.o csu/crti.o csu/crtn.o $INSTALL_PATH/$TARGET/lib
$TARGET-gcc -nostdlib -nostartfiles -shared -x c /dev/null -o $INSTALL_PATH/$TARGET/lib/libc.so
touch $INSTALL_PATH/$TARGET/include/gnu/stubs.h
cd ..

# Compiler Support Library
cd build-gcc
make $PARALLEL_MAKE all-target-libgcc
make install-target-libgcc
cd ..

# Standard C Library & the rest of Glibc
cd build-glibc
make $PARALLEL_MAKE
make install
cd ..


# Standard C++ Library & the rest of GCC
cd build-gcc
make $PARALLEL_MAKE all
make install
cd ..

# Cleanup
rm -rf ${BINUTILS_VERSION}*
rm -rf ${GCC_VERSION}*
rm -rf ${LINUX_KERNEL_VERSION}*
rm -rf ${GLIBC_VERSION}*
rm -rf build-*

trap - EXIT
echo 'Success!'
