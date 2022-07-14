gem5-x86 --outdir=traffGenRes/m5out_ddr3_RO materials/using-gem5/03-running/example3/traffGen_example.py DDR3_1600_8x8  random 100
gem5-x86 --outdir=traffGenRes/m5out_ddr4_RO materials/using-gem5/03-running/example3/traffGen_example.py DDR4_2400_16x4 random 100
gem5-x86 --outdir=traffGenRes/m5out_nvm_RO  materials/using-gem5/03-running/example3/traffGen_example.py NVM_2400_1x64  random 100


gem5-x86 --outdir=traffGenRes/m5out_ddr3_R50 materials/using-gem5/03-running/example3/traffGen_example.py DDR3_1600_8x8  random 50
gem5-x86 --outdir=traffGenRes/m5out_ddr4_R50 materials/using-gem5/03-running/example3/traffGen_example.py DDR4_2400_16x4 random 50
gem5-x86 --outdir=traffGenRes/m5out_nvm_R50  materials/using-gem5/03-running/example3/traffGen_example.py NVM_2400_1x64  random 50


gem5-x86 --outdir=traffGenRes/m5out_ddr3_WO materials/using-gem5/03-running/example3/traffGen_example.py DDR3_1600_8x8  random 0
gem5-x86 --outdir=traffGenRes/m5out_ddr4_WO materials/using-gem5/03-running/example3/traffGen_example.py DDR4_2400_16x4 random 0
gem5-x86 --outdir=traffGenRes/m5out_nvm_WO  materials/using-gem5/03-running/example3/traffGen_example.py NVM_2400_1x64  random 0
