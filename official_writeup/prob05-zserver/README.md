# [Misc] Z 公司的服务器

- 命题人：debugger
- 服务器：150 分
- 流量包：200 分

## 题目描述

<p>Z 公司有很多服务器。出于安全考虑，这些服务器不能直接通过 SSH 登录，需要经过层层跳板，传输文件很不方便。</p>
<p>但是<strong>有一种古老的方法</strong>可以拿到服务器上的文件。这究竟是什么方法呢？</p>
<p>同时，黑客还拿到了一段这个服务器的流量。连接到服务器即可用这种方法接收 Flag 1，流量包中记录了用这种方法接收到的 Flag 2。</p>
<div class="well">
<p><strong>萌新教学：</strong></p>
<p>如下面的说明所示，本题在 <code>prob05.geekgame.pku.edu.cn</code> 主机开放了 TCP 10005 端口。
你可以点击链接启动网页终端。如果涉及网页终端难以输入的特殊字符，也可以使用命令行工具 netcat 或者 pwntools 等带 socket 通信功能的库连接到这个端口。参见 <a href="#/info/faq">FAQ：关于终端交互</a>。</p>
<p>请与这个端口上的程序交互获得 Flag。连接频率限制是 30 秒 3 次。</p>
<p>题目会要求输入个人 Token 来验证你的选手身份。点击页面底部的 “复制个人 Token” 按钮可以复制自己的 Token。网页终端会自动填入 Token。</p>
</div>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>这是题目的 Dockerfile：</li>
</ul>
<div class="codehilite" style="background: #f8f8f8"><pre style="line-height: 125%;"><span></span><code>FROM ubuntu:22.04
RUN apt update &amp;&amp; apt install -y lrzsz
WORKDIR /
COPY flag.txt /
CMD sz flag.txt
</code></pre></div>

<ul>
<li>有些工具对此协议支持存在 bug，你可以换别的试试。</li>
<li>可以看看 <a target="_blank" rel="noopener noreferrer" href="http://gallium.inria.fr/~doligez/zmodem/zmodem.txt">这个协议的规范</a>。</li>
</ul>
</div>

**【终端交互：连接到题目】**

**[【附件：下载题目附件（prob05.pcapng）】](attachment/prob05.pcapng)**

## 预期解法

### 服务器

首先先要知道数据用ZMODEM协议传输。连接到服务器会显示“`*B00000000000000`”（流量包里面也有），Google或者百度搜索一下这个就能知道。

接着有多种不同做法：

1. 可以直接用支持ZMODEM协议的终端模拟器。用终端模拟器随便连接到一台远程机器，或者在本地运行sshd（Windows的话需要在WSL 1里面运行）之后连接到localhost，然后在命令行运行`nc prob05.geekgame.pku.edu.cn 10005`，就可能能下载到flag.txt文件。在我试过的几种软件中，AbsoluteTelnet和WindTerm可以正常下载flag.txt文件；XShell收不到文件，但是多次按回车能把flag输出到屏幕上；SecureCRT和WoTerm则完全接收不到文件。
2. 参考这个协议的规范自己写交互。这个有点麻烦；因为有现成的第三方库，这里就不给具体实现了。
3. 使用[modem](https://pypi.org/project/modem/)之类的第三方库也可以实现ZMODEM协议交互。

### 流量包

流量包里面有多个TCP包。但是因为TCP是基于字节流的协议，所以TCP包的边界是无意义的，连续的包应该拼接成一个整体，这样就得到了一个20277字节的串。

接着去除ZMODEM转义字符，按照ZMODEM规范，任何字节如果第5和第6个bit都是0，则需要转义，伪代码如下：
```
if (CH&0x60 == 0) {
CH => ZDLE CH^0x40 // ZDLE=0x18
}
```
根据这个规则去除转义字符，得到一个16214字节的串：
```python
y=b''
while x:
    if x[0]==0x18 and (x[1]^0x40)&0x60==0:
        y=y+bytes([x[1]^0x40])
        x=x[2:]
    else:
        y=y+bytes([x[0]])
        x=x[1:]
```
按照ZMODEM规范，这个串结构是：
```
*
0x18 C # 帧类型为'C'（32位CRC的二进制模式）。注意上面代码会把这两个字节转成一个字节0x03
0x0a   # ZDATA
0x00000000
<4字节CRC>
<不超过1024字节数据> 0x18 0x69 <4字节CRC>
<不超过1024字节数据> 0x18 0x69 <4字节CRC>
……
<不超过1024字节数据> 0x18 0x68 <4字节CRC>
```

因为数据片段数是未知的，可以先按照0x18 0x69和0x18 0x68把数据串拆成一些片段，去除里面的CRC，然后把里面的数据取出，就能还原原来的flag.jpg文件。

### 命题背景
正如题面所说，有些公司的生产环境机器出于安全起见，登录需要经过跳板机，同时还采取更多安全措施，常见的如下：
* 跳板机仅限公司内网访问，因此如果在公司外必须先连接公司VPN
* 跳板机不支持ProxyJump
* 跳板机不支持端口转发（因为办公网被认为是不安全的，可能有病毒）
* 跳板机和生产环境机器都设置防火墙，只支持访问白名单网站
* 自己实现了身份认证系统，因此访问跳板机和生产环境机器既不使用密码也不用密钥对，而是使用2FA token；同时集中管理跳板机和生产环境机器的访问权限
* 甚至把跳板机的Shell也换掉，这样跳板机除了用于连接生产环境机器没有别的功能

如此SCP、rsync之类的需要直接或者通过代理/端口转发访问机器的工具都不能用来在办公网和生产环境机器之间传输文件。此时解决方案主要有几个：
* 用ZMODEM（就是本题）
* 维护一台办公网和生产环境机器都能访问的SFTP服务器，用这个机器中转文件
* 维护一台办公网和生产环境机器都能访问的中转机器（Server），然后办公网和生产环境机器（Client）都安装一个特定软件，利用这个Server实现两个Client之间的文件传输。和上一条不同的是文件不会保存在中转机器中
