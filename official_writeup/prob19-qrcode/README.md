# [Algorithm] 华维码

- 命题人：NanoApe
- 华维码 · 特难：200 分
- 华维码 · 特小：400 分

## 题目描述

<p>想要获得华维 Mate 60？首先你得来试一试华维码！</p>
<p><b>Huavvei Mate Hard？华维码 · 特难！</b></p>
<blockquote>
<p>Q: 怪，华容道为什么会和二维码搭上关系？</p>
<p>A: 这你就不知道了，这是多么遥遥领先的出题思路！</p>
</blockquote>
<p><b>Huavvei Mate Nano？华维码 · 特小！</b></p>
<blockquote>
<p>Q: Hard 难度我能理解，但 Nano 是什么难度？</p>
<p>A: 你看那些华容道格子是不是很 Nano？</p>
</blockquote>
<p><strong>补充说明：</strong></p>
<ul>
<li>此题属于 Algorithm 而非 Web。按页面要求通关即可获得 Flag，无需利用 Web 漏洞。</li>
<li>操作步数上限为 30000。正常的操作步数应远小于此限制。</li>
</ul>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>可以看看 <a target="_blank" rel="noopener noreferrer" href="https://blog.tonycrane.cc/p/409d352d.html">这篇博客</a>。</li>
</ul>
</div>

**【网页链接：访问题目网页】**

## 预期解法

### Level Hard

通过定位点，可以确定 16 个块的位置，剩余 8 块排列组合搜索所有可能的摆放方式，并检查生成的二维码能否被正确扫描，复杂度 8!=40320。

### Level Nano

复杂度过高，这下搜索不给力了……

但我们可以通过一些二维码的编码规则来降低复杂度。

首先，可以先猜测一下二维码的编码方式，例如最常用的 Byte Mode Encoding。

接着，在 Version 7-L 中，一共有两个 blocks，如果内容长度小于 78 的话，第二个 blocks 就全都是 11101100 00010001，纠错码也是固定的。

所以可以通过爆破长度来确定最终的字符串长度是 63，然后根据 blocks 2 的内容，确定所有碎片的位置，复杂度直接降为 O(1)。

最后再手推一下 9*9 的华容道就可以了！

#### 非预期解

Flask 3.0 太坏了！下载二维码碎片的时候，Flask 会在响应中带一个文件名相关的 header，文件名有这个二维码碎片的编号（0-80），直接按顺序拼就完事了……
