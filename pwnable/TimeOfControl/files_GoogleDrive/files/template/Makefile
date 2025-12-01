all: build

build: exploit.c
	gcc --static -S exploit.c -o exploit.S; musl-gcc --static exploit.S -o exploit; strip exploit;

prepare: build
	sudo rm -rf ./ext; mkdir ext; cd ext; sudo cpio -id < ../../src/rootfs.cpio; sudo rm ../../src/rootfs.cpio; sudo cp ../exploit bin/; sudo chown root bin/exploit; sudo find . -print0 | sudo cpio -o --format=newc --null > ../../src/rootfs.cpio; cd ../; sudo chown root ../src/rootfs.cpio; sudo rm -rf ./ext

