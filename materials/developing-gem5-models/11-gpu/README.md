# To compile square
cd /workspaces/gem5-bootcamp-env/gem5-resources/src/gpu/square
docker run --rm --volume /var/lib/docker/codespacemount/workspace/:/workspaces -w `pwd` gcr.io/gem5-test/gcn-gpu:v22-0 make

# To compiler gem5 (GCN3) GPU model
cd /workspaces/gem5-bootcamp-env/gem5/
docker run --rm --volume /var/lib/docker/codespacemount/workspace/:/workspaces -w `pwd` gcr.io/gem5-test/gcn-gpu:v22-0 scons build/GCN3_X86/gem5.opt -j17

# To run square in gem5 (static register allocator)
cd /workspaces/gem5-bootcamp-env/
docker run --rm --volume /var/lib/docker/codespacemount/workspace/:/workspaces -w `pwd` gcr.io/gem5-test/gcn-gpu:v22-0 gem5/build/GCN3_X86/gem5.opt -d m5out-static gem5/configs/example/apu_se.py --reg-alloc-policy=simple -n 3 -c gem5-resources/src/gpu/square/bin/square

# To run square in gem5 (dynamic register allocator)
docker run --rm --volume /var/lib/docker/codespacemount/workspace/:/workspaces -w `pwd` gcr.io/gem5-test/gcn-gpu:v22-0 gem5/build/GCN3_X86/gem5.opt -d m5out-dynamic gem5/configs/example/apu_se.py --reg-alloc-policy=dynamic -n 3 -c gem5-resources/src/gpu/square/bin/square

# to compile m5ops
cd /workspaces/gem5-bootcamp-env/gem5/util/m5
docker run --rm --volume /var/lib/docker/codespacemount/workspace/:/workspaces -w `pwd` gcr.io/gem5-test/gcn-gpu:v22-0 scons build/x86/out/m5

# to compile BC
cd /workspaces/gem5-bootcamp-env/gem5-resources/src/gpu/pannotia/bc
docker run --rm --volume /var/lib/docker/codespacemount/workspace/:/workspaces -w `pwd` gcr.io/gem5-test/gcn-gpu:v22-0 bash -c "export GEM5_PATH=/workspaces/gem5-bootcamp-env/gem5 ; make gem5-fusion"

# to run BC
wget http://dist.gem5.org/dist/develop/datasets/pannotia/bc/1k_128k.gr
docker run --rm --volume /var/lib/docker/codespacemount/workspace/:/workspaces -w `pwd` gcr.io/gem5-test/gcn-gpu:v22-0 gem5/build/GCN3_X86/gem5.opt -d m5out-bc gem5/configs/example/apu_se.py --reg-alloc-policy=dynamic -n 3 --mem-size=16GB --benchmark-root=gem5-resources/src/gpu/pannotia/bc/bin -c bc.gem5 --options="1k_128k.gr"