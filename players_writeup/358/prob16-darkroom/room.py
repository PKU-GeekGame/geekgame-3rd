import time
import pwn
import datetime
pwn.context(arch = 'i386', os = 'linux')

r = pwn.remote('prob16.geekgame.pku.edu.cn', 10016)
def read(to=0.5):
    while (s := r.recvline(timeout=to).decode()):
        if len(s) == 0:
            break
        print(s)
# EXPLOIT CODE GOES HERE
# r.send(pwn.asm(pwn.shellcraft.sh()))
r.send(b'358:MEUCIQDb6YWezKSY0SgaNk20CRFNyXYqZsevxHpO_pEVGRy4xgIgA6JkMXKrvX3FgHkv-hl2ya1EJFro347G-X1gaxMv_-8=\r\n')

read(3)
for operation in [
        "newgame",
        "Miyazono",
        "y",
        " hhhnne",
        "pickup key",
        " wssees",
        "usewith key door",
        " ssnwwwn",
        "pickup key",
        " seeenne",
        "pickup trinket",
        "use trinket",
        " wwwnnww",
        "usewith key door",
]:
    print(f">>> {operation}")
    if operation[0] == " ":
        for op in operation[1:]:
            print(f">>> {op}")
            r.send((op + "\n").encode())
            read()
    else:
        r.send((operation + "\n").encode())
        read()
r.send(b'n\n')
while (s := r.recvline(timeout=1).decode()):
    if len(s) == 0:
        break
    print(s)

# r.send(b'Miyazono')
# print(r.recv().decode())

# r.send(b'y')
# print(r.recv().decode())
