# [Misc] 猫咪状态监视器

- 命题人：NanoApe
- 题目分值：200 分

## 题目描述

<p>Nano 最近新养了一只猫叫瑟维斯！</p>
<p>由于 Nano 经常外出，他希望能够远程监视瑟维斯的状态，以确保她的安全和舒适。</p>
<p>于是，为了方便照顾，Nano 开发了一款名为「瑟维斯状态查看器」（Service Checker）的监视器！</p>
<p>纯命令行无 UI，非常 Geek！</p>
<blockquote>
<p>Nano: 但我写这玩意不是为了让你拿 flag 的，也不是为了让猫猫吃 flag 的……嗯？</p>
</blockquote>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>可以看看 <code>/usr/bin/service</code> 的源码，了解一下 STATUS 命令是如何调用对应服务的。</li>
<li>LIST 命令不输出任何东西是正常现象。因为题目环境里没有运行任何服务。</li>
</ul>
</div>

**[【附件：下载题目源码（prob15-src.zip）】](attachment/prob15-src.zip)**

**【终端交互：连接到题目】**

## 预期解法

通过阅读 `/usr/sbin/service`，可以发现 service 并没有对调用的服务做任何路径检查。所以……我们可以通过路径穿越来调用任意的可执行文件！

通过路径穿越，`/usr/sbin/service` 可以调用任意的可执行文件，所以我们可以调用一下 cat 获取 `flag.txt` 的内容。

```
Command: STATUS
Service name: ../../../usr/bin/cat /flag.txt
```
