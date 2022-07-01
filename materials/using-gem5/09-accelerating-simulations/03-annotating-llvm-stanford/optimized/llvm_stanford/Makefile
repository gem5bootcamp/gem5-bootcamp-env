# gem5 specific parameters

TARGET_ISA=x86

# On prder to get the GEM5_HOME variable working, this Makefile requires
# realpath ot be installed.

GEM5_HOME=/home/gem5/gem5
$(info   GEM5_HOME is $(GEM5_HOME))

# Using g++ as the only compiler.

CXX=gcc

#CFLAGS

CFLAGS= -static -O3 -I$(GEM5_HOME)/include

#LDFLAGS

LDFLAGS=-L$(GEM5_HOME)/util/m5/build/$(TARGET_ISA)/out -lm5

# Object files to compile

OBJECTS=Bubblesort FloatMM IntMM Oscar Perm Puzzle Queens Quicksort RealMM Towers Treesort

all: Bubblesort FloatMM IntMM Oscar Perm Puzzle Queens Quicksort RealMM Towers Treesort

Bubblesort:
	$(CXX) -o Bubblesort Bubblesort.c $(CFLAGS) $(LDFLAGS)

FloatMM:
	$(CXX) -o FloatMM FloatMM.c $(CFLAGS) $(LDFLAGS)

IntMM:
	$(CXX) -o IntMM IntMM.c $(CFLAGS) $(LDFLAGS)

Oscar:
	$(CXX) -o Oscar Oscar.c $(CFLAGS) $(LDFLAGS)

Perm:
	$(CXX) -o Perm Perm.c $(CFLAGS) $(LDFLAGS)

Puzzle:
	$(CXX) -o Puzzle Puzzle.c $(CFLAGS) $(LDFLAGS)

Queens:
	$(CXX) -o Queens Queens.c $(CFLAGS) $(LDFLAGS)

Quicksort:
	$(CXX) -o Quicksort Quicksort.c $(CFLAGS) $(LDFLAGS)

RealMM:
	$(CXX) -o RealMM RealMM.c $(CFLAGS) $(LDFLAGS)

Treesort:
	$(CXX) -o Treesort Treesort.c $(CFLAGS) $(LDFLAGS)

Towers:
	$(CXX) -o Towers Towers.c $(CFLAGS) $(LDFLAGS)

clean:
	rm -f $(OBJECTS)
