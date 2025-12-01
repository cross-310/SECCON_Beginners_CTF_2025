import os
from pwn import *

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", "9999"))
sc = remote(HOST, PORT)

sc.recvuntil(b"> ")
sc.sendline(b"a"*16)
sc.recvuntil(b"> ")
sc.sendline(b"b"*16)
sc.recvuntil(b": ")
ct = bytes.fromhex(sc.recvline().decode())
val = [False] + [ct[:16] == ct[i:i+16] for i in range(0, len(ct)-16, 16)]
print(bytes([sum(val[i+j]<<7-j for j in range(8)) for i in range(0, len(val), 8)]))
