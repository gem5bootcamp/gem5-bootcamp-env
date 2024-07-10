## Note on running GPU FS

You need not use docker to run simulations in GPU FS mode. We will be simulating AMD's latest GPU, MI300, in FS mode

#If you haven't built m5ops yet, then

```sh
cd /workspaces/gem5-bootcamp-env/gem5/util/m5
```
```sh
scons build/x86/out/m5
```

#To compile square for MI300

```sh
cd /workspaces/gem5-bootcamp-env/gem5-resources/src/gpu/square
```
```sh
cp /workspaces/gem5-bootcamp-env/materials/isca24/10-gpufs/Makefile ./
```
```sh
make
```

#To run square in FS mode

```sh
cd /workspaces/gem5-bootcamp-env
```
```sh
/usr/local/bin/gem5-vega gem5/configs/example/gpufs/mi200.py --kernel ./vmlinux-gpu-ml-isca --disk-image ./x86-ubuntu-gpu-ml-isca --app ./gem5-resources/src/gpu/square/bin/square --no-kvm-perf
```

#To create a checkpoint (assuming m5_checkpoint_addr() is already included in the application), we need to recompile square so that it creates a checkpoint

```sh
cp materials/isca24/10-gpufs/square-cpt/square.cpp gem5-resources/src/gpu/square/
```
```sh
cp materials/isca24/10-gpufs/mi300.py gem5/configs/example/gpufs/
```
```sh
cd gem5-resources/src/gpu/square
```
```sh
make clean && make
```

# To create checkpoint

```sh
cd /workspaces/gem5-bootcamp-env
```
```sh
/usr/local/bin/gem5-vega gem5/configs/example/gpufs/mi200.py --kernel ./vmlinux-gpu-ml-isca --disk-image ./x86-ubuntu-gpu-ml-isca --app ./gem5-resources/src/gpu/square/bin/square --no-kvm-perf --checkpoint-dir ./m5out
```

# To restore
```sh
/usr/local/bin/gem5-vega gem5/configs/example/gpufs/mi200.py --kernel ./vmlinux-gpu-ml-isca --disk-image ./x86-ubuntu-gpu-ml-isca --app ./gem5-resources/src/gpu/square/bin/square --no-kvm-perf --restore-dir ./m5out
```
