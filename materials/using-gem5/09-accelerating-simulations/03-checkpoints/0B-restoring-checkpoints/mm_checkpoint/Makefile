# This Makefile is used to compile the mm_ckpt.cpp file.
# gem5 specific parameters

TARGET_ISA=x86

# On prder to get the GEM5_HOME variable working, this Makefile requires
# realpath ot be installed.

GEM5_HOME=/home/gem5/gem5
$(info   GEM5_HOME is $(GEM5_HOME))

# Using g++ as the only compiler.

CXX=g++

#CFLAGS

CFLAGS=-std=c++14 -static -O3 -I$(GEM5_HOME)/include

#LDFLAGS

LDFLAGS=-L$(GEM5_HOME)/util/m5/build/$(TARGET_ISA)/out -lm5

# Object files to compile

OBJECTS=mm_checkpoint

all: mm_checkpoint

mm_checkpoint:
	$(CXX) -o $(OBJECTS) mm_checkpoint.cpp $(CFLAGS) $(LDFLAGS)

clean:
	rm -f $(OBJECTS)
