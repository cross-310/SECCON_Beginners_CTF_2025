import os
from pwn import *

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", "9999"))
sc = remote(HOST, PORT)

def enc_oracle(pt):
    sc.recvuntil(b"> ")
    sc.sendline(b"1")
    sc.recvuntil(b"> ")
    sc.sendline(pt.hex().encode())
    sc.recvuntil(b": ")
    return bytes.fromhex(sc.recvline().decode())

def dec_oracle(pt):
    sc.recvuntil(b"> ")
    sc.sendline(b"2")
    sc.recvuntil(b"> ")
    sc.sendline(pt.hex().encode())
    sc.recvuntil(b": ")
    return bytes.fromhex(sc.recvline().decode())

def get_ticket(answer):
    sc.recvuntil(b"> ")
    sc.sendline(b"3")
    sc.recvuntil(b": ")
    challenge = bytes.fromhex(sc.recvline().decode())
    sc.recvuntil(b"> ")
    sc.sendline(answer.hex().encode())
    sc.recvline()
    return challenge

chal = get_ticket(b"a")
chal = [chal[i:i+16] for i in range(0, len(chal), 16)]

f3 = b"\x10"*16
d = dec_oracle(f3)
iv = xor(b"\x10"*16, d[:16], d[16:])
f2 = xor(f3, d[16:], chal[2])
f1 = xor(dec_oracle(f2)[:16], iv, chal[1])
f0 = xor(dec_oracle(f1)[:16], iv, chal[0])
f4 = enc_oracle(xor(f3, iv, chal[3]))[:16]
f5 = enc_oracle(xor(f4, iv, chal[4]))[:16]
f6 = enc_oracle(xor(f5, iv, chal[5]))[:16]

get_ticket(f0+f1+f2+f3+f4+f5+f6)

sc.recvuntil(b"> ")
sc.sendline(b"4")
print(sc.recvline().decode())
