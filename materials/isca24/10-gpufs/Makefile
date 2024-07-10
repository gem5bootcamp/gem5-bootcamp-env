HIP_PATH?= /opt/rocm
HIPCC=$(HIP_PATH)/bin/hipcc

BIN_DIR?= ./bin

GEM5_PATH?=/workspaces/gem5-bootcamp-env/gem5

CXXFLAGS=-I$(GEM5_PATH)/include
CXXFLAGS+=-I$(GEM5_PATH)/util/m5/src
LDFLAGS=-L$(GEM5_PATH)/util/m5/build/x86/out
LDFLAGS+=-lm5

square: $(BIN_DIR)/square

$(BIN_DIR)/square: square.cpp $(BIN_DIR)
	$(HIPCC) --amdgpu-target=gfx801,gfx803,gfx900,gfx902,gfx90a $(CXXFLAGS) square.cpp -o $(BIN_DIR)/square $(CXXFLAGS) $(LDFLAGS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

clean:
	rm -rf $(BIN_DIR)

.PHONY: square clean
