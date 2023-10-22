# [Binary] Baby Stack

- 命题人：于新雨
- Flag 1：200 分
- Flag 2：300 分

## 题目描述

<p>A pwn challenge 4 babies (or college students)！</p>
<blockquote>
<p>这样的栈溢出题目对于小朋友来说有些幼稚，但对大学生刚刚好。</p>
</blockquote>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>你可以 <a target="_blank" rel="noopener noreferrer" href="/service/attachment/prob10-babystack/prob10-src.zip">下载题目源码</a>。</li>
<li>Flag 1: integer overflow and stack overflow~</li>
<li>Flag 2: format string leak，format string任意地址写。可以参考 <a target="_blank" rel="noopener noreferrer" href="https://ctf-wiki.org/pwn/linux/user-mode/fmtstr/fmtstr-exploit/#_13">CTF Wiki</a>，但是给的例子是 32 位的，需要改成 64 位的。</li>
<li>在 2.27 及以后的 glibc 版本中，<code>system</code> 会使用 <code>movaps</code> 指令，此时会要求 <code>rsp</code> 按 16 字节对齐。如果 gdb 调试时发现停止在了这一行，可以通过使用一个单独的 ret gadget 来使其对齐。</li>
</ul>
</div>

**[【附件：下载题目附件（prob10.zip）】](attachment/prob10.zip)**

**【终端交互：连接到挑战 1】**

**【终端交互：连接到挑战 2】**

**[【隐藏附件：prob10-src.zip】](attachment/prob10-src.zip)**

## 预期解法

解题脚本见 [sol](sol/) 目录，题目源码见 [src](src/) 目录。两个挑战的编译选项分别是：

- `gcc -fno-stack-protector -no-pie -Og -o /babystack /babystack.c`
- `gcc -fno-stack-protector -no-pie -D_FORTIFY_SOURCE=0 -Og -o /teenagerstack /teenagerstack.c`

### Flag 1

- 整数溢出
  - 自己实现了一个get_line函数，一下循环的变量是unsigned int类型，在终止条件的时候size转成unsigned int比较，当传入size为0的时候，终止条件为i< UMAX,就可以溢出了~

- 栈溢出
  - 改main的返回地址为backdoor,注意应该会有movaps的问题，在 2.27 及以后的 glibc 版本中，system 会使用 movaps 指令，此时会要求 rsp 按 16 字节对齐。如果 gdb 调试时发现停止在了这一行，可以通过使用一个单独的 ret gadget 来使其对齐。远程环境为高版本 libc 存在该问题


### Flag 2

纯格式化字符串利用，预期是用第一个格式化字符串泄漏libc，第二个改puts函数的got表为system函数地址，然后传入"/bin/sh\x00"即可

感觉格式化字符串任意地址写有点小绕，可以参考ctf-wiki: https://ctf-wiki.org/pwn/linux/user-mode/fmtstr/fmtstr-exploit/#_14