all: chall

chall: src.c Makefile
	gcc src.c -o chall -fcf-protection=none -fno-stack-protector -pie -Wl,-z,relro -Wl,-z,now
