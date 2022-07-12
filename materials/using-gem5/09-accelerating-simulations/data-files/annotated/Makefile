# This Makefile is used to compile the mm_annotated.cpp file. It
# is assumped that the cpp file, i.e., mm_annotated.cpp is locate in the 
# directory

# gem5 specific parameters

TARGET_ISA=x86

# On prder to get the GEM5_HOME variable working, this Makefile requires
# realpath ot be installed.

GEM5_HOME=$(realpath ./)
$(info   GEM5_HOME is $(GEM5_HOME))

# Using g++ as the only compiler.

CXX=g++

#CFLAGS

CFLAGS=-std=c++14 -static -O3 -I$(GEM5_HOME)/include

#LDFLAGS

LDFLAGS=-L$(GEM5_HOME)/util/m5/build/$(TARGET_ISA)/out -lm5

# Object files to compile

OBJECTS=mm_annotated

all: mm_annotated

mm_annotated:
	$(CXX) -o $(OBJECTS) mm_annotated.cpp $(CFLAGS) $(LDFLAGS)

clean:
	rm -f $(OBJECTS)
