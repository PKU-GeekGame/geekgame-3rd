from pwn import remote

def main():
    conn = remote("prob08.geekgame.pku.edu.cn", 10008)
    conn.interactive()
    conn.send(b"3\n")

    conn.recvuntil("ꝋɍ ӻꝋɍӻēīⱦ ⱥłł.\n".encode())
    line = conn.recvline().decode().strip()
    print(line[:32] + " ... " + line[-32:])
    seeds = [seed[2:] for seed in line.strip("<>").split(",")]
    conn.send(",".join(seeds).encode())
    conn.send(b"\n")

    conn.interactive()

main()
