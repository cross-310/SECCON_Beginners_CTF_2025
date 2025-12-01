import os
from pwn import *
from sympy.ntheory.residue_ntheory import nthroot_mod
from fastecdsa.curve import secp256k1
from fastecdsa.point import Point

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", "9999"))
sc = remote(HOST, PORT)

sc.recvuntil(b"y = ")
y = int(sc.recvline())
x = nthroot_mod(y**2 - 7, 3, secp256k1.p)
sc.recvuntil(b"x = ")
sc.sendline(str(x).encode())
sc.recvuntil(b"a = ")
a = secp256k1.q - 1
sc.sendline(str(a).encode())
print(sc.recvline())
