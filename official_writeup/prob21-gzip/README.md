# [Algorithm] 未来磁盘

- 命题人：debugger
- Flag 1：150 分
- Flag 2：300 分

## 题目描述

<p>2077 年，随着核聚变、脑机接口和时光机技术的成熟，人类终于可以在磁盘上存储十亿人愿意生活在其中的虚拟世界。</p>
<p>2077 年的小 Z 有一块 1EB 大小的磁盘。小 Z 在上面干了这些事：</p>
<ul>
<li>生成两个巨大的全 0 文件：<code>fallocate -l size1 file1 &amp;&amp; fallocate -l size2 file2</code>（这里 <code>size1</code> 和 <code>size2</code> 是未知的值，但不会超过 1EB）</li>
<li>把两个文件和 Flag 拼起来：<code>cat file1 flag file2 &gt; file</code></li>
<li>用 gzip 压缩生成的文件：<code>gzip file</code></li>
<li>得到的文件还很大，因此他重复了几次压缩操作：<code>mv file.gz file &amp;&amp; gzip file</code></li>
<li>把得到的 <code>file.gz</code> 传送回 2023 年</li>
</ul>
<p>现在你得到了从 2077 年传送回来的 <code>file.gz</code> 文件。你能解压出里面的 Flag 吗？</p>
<p><strong>补充说明：</strong>Flag 1 的原文件大小约 7TB，Flag 2 的原文件大小约 27PB。</p>
<div class="well">
<p><strong>提示：</strong></p>
<ul>
<li>运行 <code>cat /dev/zero | gzip | hexdump</code>，看看会输出什么。</li>
<li>运行 <code>cat /dev/zero | gzip | gzip | hexdump</code> 呢？如果你看不到任何输出，有什么办法可以加速这个计算过程？</li>
</ul>
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>Flag 1: 直接解压大约需要 8 小时。你一定要真的解压<strong>到硬盘</strong>上吗？</li>
<li>Flag 2: 可以阅读一下 <a target="_blank" rel="noopener noreferrer" href="https://github.com/sigpwny/UIUCTF-2023-Public/blob/main/challenges/web/futuredisk/SOLVE.md">这个题解</a>。事实上本题的题面也是从那道题改写的。</li>
<li>另外，之前的提示中的两个命令最后都会产生周期性的输出，这个周期是多少？既然输出是周期性的，你可以尝试删除中间结果中重复出现的部分。</li>
</ul>
</div>

**[【附件：下载题目附件（prob21.zip）】](attachment/prob21.zip)**

## 预期解法

首先，运行以下代码，
```python
z=zlib.compressobj(9,wbits=31)
for i in range(10**10):
    k=z.compress(b'\x00')
    if k:
        print(i,len(k))
```

可以发现每4226814个0字节会生成一段输出，且4段输出总长是16433字节。实际上，gzip包装了deflate流，deflate流是一种比特流，由一些段组成，4226814个0字节可以压缩成一个段，除了第一个和最后一个之外每个段的长度和内容都是相同的，但是段的长度不是整数字节，所以四个段相连才能对齐到字节。

对于Flag 1，解压到最后一层（7GB），会发现里面有大量重复出现的16433字节片段。在前半部分和后半部分各取一个片段（因为字节对齐不同两个片段是不同的），然后替换所有片段为空，可以得到一个较小的文件，再解压这个文件（如果用Python的zlib或gzip库解压，需要去掉后面表示文件长度和校验码的8字节），就能拿到flag。此外还可以使用`gzip -dc < flag | grep -z "flag{.*}"`直接解压并查找flag。

Flag 2直接解压需要27000小时，显然是不现实的。如果变量x存储上述16433字节片段，下面代码可以寻找反复压缩x得到的周期：

```
k={}
z=zlib.compressobj(9,wbits=31)
for i in range(1,10000000):
    u=z.compress(x)
    if u:
        h=md5(u).hexdigest()
        print(i,h,k.get(h,-1))
        k[h]=i
```

32766个x可以压缩成一个长837373字节的串。因此解法也和上面类似：
* 手工解压到倒数第二层（大约会产生一个30GB的文件）
* 取一个连续的长837373字节的串（直接从文件里面取即可，无须用上面的方法生成），把文件里面所有这种串替换为空（同样，前半部分和后半部分的串是不同的）
* 解压，得到一个较小的最后一层文件
* 重复Flag 1的过程就能得到Flag 2

如果不知道周期的长度，也可以使用以下代码得到：
```python
f=open("flag.gz","rb") #flag.gz是倒数第二层的文件
x=f.read(500000000)
x[1000001:].index(x[1000000:1100000]) #会得到837372
```

如果机器存不下30GB文件，可以先解压到倒数第三层（约200MB），把倒数第三层分成若干片段，然后再按片段解压，各片段拼接的结果就是倒数第二层，但是可以每一次拼接后都替换掉837373字节的串。


### 附注
本题目的附件生成代码可见gen.py。里面同时实现了计算CRC32的功能。运行gen(25000,25000)就能得到Flag 2的文件。

### 命题背景
去年GeekGame里面有一个题目思路，给一个有很多文件的压缩包和一个IPFS地址或磁力链接，从这些文件里面找出给定的地址或链接代表的文件，里面有flag。后来xmcp觉得静态附件可能会有选手把文件真的传到IPFS里面，磁力链接不唯一（infohash里有分块大小信息piece_length，所以一个文件可能有无穷多个infohash），而生成动态附件又麻烦，所以最后没有选用该题目。里面有一个flag就像本题这样，给了一个很大的含有flag的文件，要求选手解压出flag来。本届就把这一部分单独取出来成为一道题目。去年的版本中文件只有几十GB，硬盘足够大的直接解压就能拿到flag；后来看到UIUCTF的题目之后才发现可以把文件做得更大。
