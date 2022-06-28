.DEFAULT_GOAL := gem5-tutorial-env

gem5-tutorial-env: gem5-tutorial-env-pull builder gnu-cross-compiler-riscv64 gnu-cross-compiler-aarch64
	docker build . -t gcr.io/gem5-test/gem5-tutorial-env:latest

gem5-tutorial-env-pull:
	docker pull gcr.io/gem5-test/gem5-tutorial-env:latest

builder: builder-pull
	docker build . -f Dockerfile-builder -t gcr.io/gem5-test/gem5-builder:latest

builder-pull:
	docker pull gcr.io/gem5-test/gem5-builder:latest

gnu-cross-compiler-riscv64: gnu-cross-compiler-riscv64-pull
	docker build gnu-cross-compilers -f gnu-cross-compilers/Dockerfile-riscv64 -t gcr.io/gem5-test/gnu-cross-compiler-riscv64:latest

gnu-cross-compiler-riscv64-pull:
	docker pull gcr.io/gem5-test/gnu-cross-compiler-riscv64:latest

gnu-cross-compiler-aarch64: gnu-cross-compiler-aarch64-pull
	docker build gnu-cross-compilers -f gnu-cross-compilers/Dockerfile-aarch64 -t gcr.io/gem5-test/gnu-cross-compiler-aarch64:latest

gnu-cross-compiler-aarch64-pull:
	docker pull gcr.io/gem5-test/gnu-cross-compiler-aarch64:latest

clean:
	- docker image rm gcr.io/gem5-test/gem5-builder:latest
	- docker image rm gcr.io/gem5-test/gnu-cross-compiler-riscv64:latest
	- docker image rm gcr.io/gem5-test/gnu-cross-compiler-aarch64:latest
	- docker image rm gcr.io/gem5-test/gem5-tutorial-env:latest

push: gem5-tutorial-env
	docker push gcr.io/gem5-test/gem5-builder:latest
	docker push gcr.io/gem5-test/gnu-cross-compiler-riscv64:latest
	docker push gcr.io/gem5-test/gnu-cross-compiler-aarch64:latest
	docker push gcr.io/gem5-test/gem5-tutorial-env:latest
