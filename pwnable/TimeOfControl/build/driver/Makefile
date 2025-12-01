obj-m := ctf4b.o
KBUILD_DIR := ~/Work/ctf-problems/buildroot/output/build/linux-6.12.27/

all:
	$(MAKE) CC=musl-gcc -C $(KBUILD_DIR) M=$(shell pwd) modules

clean:
	$(MAKE) CC=musl-gcc -C $(KBUILD_DIR) M=$(shell pwd) clean
