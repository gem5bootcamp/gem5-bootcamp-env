# Helping Material to Learn Adding Instructions in gem5

This directory provides helping material to add/test a couple of RISC-V Packed SIMD instructions in gem5. The slides associated with this module are available [here](https://ucdavis365-my.sharepoint.com/:p:/g/personal/jlowepower_ucdavis_edu/EeRIKzkdUJBDlaa9AmzERusBp28hxMfkyIOp-_2H5L9AqQ?e=fkoNbT).

Following is the description of folders/files in this directory:

- `add16_test.py` and `sra16_test.py` are two simple gem5 standard library scripts which create a very basic RISC-V system and test the newly added instruction using `Atomic` CPU model.
- `tests` directory contains the pre-compiled RISC-V test binaries (`add16_test` and `sra16_test`) for the newly added instructions (the source is available as well, but the toolchain to compile these tests is not available in the gem5 bootcamp env).
- `finished-material` contains a git patch that can be applied to gem5 source to add implementation of few RISC-V Packed SIMD instructions (the one we are covering in this session). To apply the patch, move it to gem5 source directory and run:
```sh
git checkout -b riscv-new-insts
git am 0001-arch-riscv-Add-some-RISC-V-packed-SIMD-instructions.patch
```
- `finished-material` also contains sample execution traces which contain the newly added instructions.