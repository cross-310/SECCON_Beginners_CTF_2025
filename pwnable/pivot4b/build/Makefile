all: chall

chall: src.c Makefile
	gcc src.c -o chall -fcf-protection=none -fno-stack-protector -no-pie -Wl,-z,lazy,-z,relro
