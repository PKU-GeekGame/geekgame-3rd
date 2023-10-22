import pwn
pwn.context(arch = 'i386', os = 'linux')

r = pwn.remote('prob08.geekgame.pku.edu.cn', 10008)
r.send("TOKEN")
for i in range(15):
    print(f"{i}\n{r.recvline(timeout=1).decode()}")
r.send(b'3\r\n')
s = r.recvline_startswith("<").decode()
r.send(s[1:-1].encode() + b'\r\n')
for i in range(20):
    print(f"{i}\n{r.recvline(timeout=1).decode()}")