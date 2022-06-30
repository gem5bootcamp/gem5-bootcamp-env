m5-exit-example: gem5/util/m5/build/x86/out/m5
	gcc -o m5-exit-example m5-exit-example.c -L./gem5/util/m5/build/x86/out -lm5 -I./gem5/include

gem5/util/m5/build/x86/out/m5: gem5
	cd gem5/util/m5 && scons build/x86/out/m5 -j `nproc`

gem5:
	cp -r ../../../../gem5 gem5
	- rm gem5/build

clean:
	- rm -r gem5
	- rm m5-exit-example
