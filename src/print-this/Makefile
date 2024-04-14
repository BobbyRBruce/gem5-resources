all: print-this

print_this: print-this-src.c Makefile
	gcc -O0 -ggdb3 -std=c99 -static print-this-src.c -o print-this

print-this-22-04:
	docker run -u$${UID}:$${GID} -v$$(pwd):/gem5 -w /gem5 -it --rm ghcr.io/gem5/ubuntu-22.04_all-dependencies:latest gcc -O0 -ggdb3 -std=c99 -static print-this-src.c -o print-this-22-04

print-this-24-04:
	docker run -u$${UID}:$${GID} -v$$(pwd):/gem5 -w /gem5 -it --rm ghcr.io/gem5/ubuntu-24.04_all-dependencies:latest gcc -O0 -ggdb3 -std=c99 -static print-this-src.c -o print-this-24-04

clean:
	rm -rf print-this
