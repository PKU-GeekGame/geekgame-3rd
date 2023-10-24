## 前言

之前参加了三届 hackergame，今年第一次参加 geekgame，能拿到 43 名、2547 分的成绩感觉还不错（

总体的题目难度对我来说感觉很有挑战性，不过也有不少能做的题。尤其是 geekgame 二阶段放出提示的机制，有些题等于是把答案直接递出来了，给了一个尝试的机会。如果是比赛结束后看到题解，就不太有动力再去亲自动手做题了，这样二阶段给提示的机制挺不错的。

## prob23-signin

## 一眼盯帧

签到题很简单，只需要从 gif 上读出每一帧显示的字母。我比较推荐使用 [mpv](https://mpv.io/)，这也是我用来逐帧播放本题 gif 的工具，它是一个功能强大的视频播放器，也支持查看图片，有许多内置快捷键，并且支持编写脚本来拓展其功能。

首先把 gif 文件下载到本地，然后在命令行使用 mpv 打开 gif 文件：

``` shell
mpv path/to/your/prob23-signin.gif --keep-open
```

这里的 `keep-open` 选项是为了让 mpv 在播放结束后不要退出。更多信息详见 mpv 的手册。

或者也可以打开 mpv 窗口，然后把下载到的 gif 文件拖动到 mpv 窗口上，也会开始播放，不过这样播放到结尾 mpv 就会自动退出。

刚才说到，mpv 有很多内置快捷键，其中逗号 `,` 和点号 `.` 两个键就是用于逐帧播放的快捷键，逗号后退一帧，点号前进一帧。这样就不难拿到 gif 上显示出的文字了。

不过这还不是最终的 flag，可以看到它是以 `synt{` 开头的。观察 synt 这几个字母的 ASCII 码可以发现，它相对于 flag 四个字母做了一个移位，每个字母增加了 13，可以猜测它是经过了凯撒密码 [ROT13](https://en.wikipedia.org/wiki/ROT13) 变换后得到的，于是网上找一个 ROT13 在线解码工具或者写一小段代码即可获得 flag。

## prob18-trivia

## 小北问答!!!!!

本体是搜索引擎考察题。不论你做什么，使用搜索引擎都是非常非常重要的基本功。

### 日语单词 “はちみー” 的含义是什么？A. 猫 / B. 马 / C. 可爱 / D. 以上都不对

虽然不懂日语，不过看前三个选项大概能猜到，就是最近网上的究极烂梗“哈基米”，B站有不少科普，此处不做赘述。简单把这个词在搜索引擎搜索一下，比如可以搜到[这个页面](https://dic.pixiv.net/a/%E3%81%AF%E3%81%A1%E3%81%BF%E3%83%BC)，即可知道它的意思是“蜂蜜”或“蜂蜜饮料”，所以选 D。

### 在北京大学（校级）高性能计算平台中，什么命令可以提交一个非交互式任务？

直接搜索“北京大学（校级）高性能计算平台”即可搜到官网，进去找到使用教程，在[这个页面](https://hpc.pku.edu.cn/_book/guide/quickStart.html)即可看到，使用 `sbatch` 命令提交非交互式任务。

### 根据 GPL 许可证的要求，基于 Linux 二次开发的操作系统内核必须开源。例如小米公司开源了 Redmi K60 Ultra 手机的内核。其内核版本号是？

直接搜索 `Redmi K60 Ultra kernel` 即可搜到一个 GitHub 仓库：https://github.com/MiCode/Xiaomi_Kernel_OpenSource ，使用 `CTRL-F` 搜索 `Redmi K60 Ultra`，点击这一行表格的最右侧一列的链接进入，可以看到源码在 corot-s-oss 分支。

那么下一个问题就是如何在 Linux 源码中查看内核版本。搜索 `kernel source version`，即可搜到[一个 StackOverflow 问答](https://stackoverflow.com/questions/12151694/where-do-i-find-the-version-of-a-linux-kernel-source-tree)，里面提到在源码顶层的 `Makefile` 文件里就可以看到版本号。点进去查看：

``` Makefile
VERSION = 5
PATCHLEVEL = 15
SUBLEVEL = 78
EXTRAVERSION =
NAME = Trick or Treat
```

所以版本号应该是 `5.15.78`。

### 每款苹果产品都有一个内部的识别名称（Identifier），例如初代 iPhone 是 iPhone1,1。那么 Apple Watch Series 8（蜂窝版本，41mm 尺寸）是什么？

这里直接搜索 `apple identifier` 之类的关键词搜不到什么有用的信息。不过可以搜索 `"iPhone1,1"`，注意这里的双引号，是为了防止搜索引擎把一个关键词拆开。这样可以轻易搜到一个 GitHub gist 页面：https://gist.github.com/adamawolf/3048717 ，其中包括了各个苹果产品的内部识别名称，`CTRL-F` 搜索题目中的型号，发现有 4 个结果：

```
Watch6,14 : Apple Watch Series 8 41mm case (GPS)
Watch6,15 : Apple Watch Series 8 45mm case (GPS)
Watch6,16 : Apple Watch Series 8 41mm case (GPS+Cellular)
Watch6,17 : Apple Watch Series 8 45mm case (GPS+Cellular)
```

再经过搜索引擎搜索可知，41mm 蜂窝版本应该是对应 `41mm case (GPS+Cellular)`，所以答案是 `Watch6,16`。

### 本届 PKU GeekGame 的比赛平台会禁止选手昵称中包含某些特殊字符。截止到 2023 年 10 月 1 日，共禁止了多少个字符？

看到这题才意识到 geekgame 平台是开源的，把页面拉到最下面即可找到代码。显然昵称应该是在后端校验的，于是查看后端代码仓库 https://github.com/PKU-GeekGame/gs-backend 。

然后需要确定该搜索的关键词，打开昵称设置界面，按 `F12` 打开浏览器 devtools，翻到其中的“网络(Network)”一栏，然后尝试修改一次昵称，可以看到浏览器向服务器的 `/service/wish/update_profile` 路径发起了一个 POST 请求。于是回到 GitHub 页面，使用 GitHub 的搜索功能在仓库里搜索 `update_profile`，发现代码里调用了一个 `check_profile` 函数，继续搜索即可找到校验昵称字符的[完整代码](https://github.com/PKU-GeekGame/gs-backend/blob/878cce9f9ff402086dae27af6859b1f71f8123e3/src/store/user_profile_store.py#L53-L68)。

然后把这段代码复制下来，包括开头的 `unicode_chars` 函数和 `from unicategories import categories`，在本地使用 python 运行 `len(DISALLOWED_CHARS)` 即可知道有多少禁止的字符。这里需要安装一个第三方库 `unicategories`。

我本地环境是 python 3.11，所以一开始的结果怎么也不对，直到题目放出提示，说本题目结果与 python 版本有关。我此前也怀疑过这个可能，因为 python 有一个标准库 unicodedata，在每个 python 版本附带的 Unicode 版本就是不同的。

还好我本地的 archlinux 环境上安装了从 3.7 到 3.12 的每个版本，于是我排序并输出了所有禁止的字符（[点此查看源码](q18-trivia/q4.py)），然后运行 `python3.11 q4.py > py311.txt` 把每个 python 版本的输出重定向到文件中，然后使用 `diff` 命令比较，在每个 python 版本新增的禁止字符中选一个，拿去添加到昵称里看服务器是否拒绝。第 4 次尝试后发现在 python 3.8 中新增的字符被服务器拒绝了，所以应该选择 python 3.8 的输出结果，也就是 `4445`。

### 在 2011 年 1 月，Bilibili 游戏区下共有哪些子分区？（按网站显示顺序，以半角逗号分隔）

这道题涉及B站的早期历史。应该有许多人听说过，bilibili 最早不叫这个名字，而是叫 mikufans，后来才改名的。这就意味着早期B站至少改过一次域名。首先需要确定当时B站的域名是什么，然后就可以在[互联网时光机 Wayback Machine](https://web.archive.org/) 查看过去存档的B站页面了。

首先搜索了一下萌娘百科，不过并没有看到详细的相关历史。干脆使用搜索引擎搜索，查到了一篇 2017 年的专栏：[cv57580](https://www.bilibili.com/read/cv57580/)，其中提到：

> **2011年6月25日** bilibili.us 域名失效，正式访问域名更改为 bilibili.tv

也就是说在那之前B站的域名应该是 bilibili.us。于是在 wayback machine 找到 2011 年 1 月的游戏区（[链接](https://web.archive.org/web/20110131163353/http://bilibili.us/video/game.html)），就可以看到几个子分区名了，于是答案是 `游戏视频,游戏攻略·解说,Mugen,flash游戏`。

### 这个照片中出现了一个大型建筑物，它的官方网站的域名是什么？

照片上包含了几家赞助商的名字，于是使用这几家赞助商的名字搜索 `启迪控股 清华科技园 中关村`，可以搜到[这个页面](http://www.iaspbo.com.cn/contents/2/533)，和照片上完美符合。所以这应该是 2023 年卢森堡 IASP 世界大会的照片。在这个网站可以看到[另一个页面](http://www.iaspbo.com.cn/contents/2/532)，其中第一张图上就是这张照片里的建筑。网页上提到：

> 我们第一晚的聚会是在卢森堡爱乐乐团举行的欢迎招待会，...

于是搜索“卢森堡爱乐乐团”，搜到它的 Wikipedia 词条 [Philharmonie Luxembourg](https://en.wikipedia.org/wiki/Philharmonie_Luxembourg)，果然就是图上的建筑。官网是 https://www.philharmonie.lu/ ，不过题目正则表达式要求不包括前面的 www，所以答案是 `philharmonie.lu`。

## prob05-zserver

## Z 公司的服务器

### flag1

根据题目描述，这应该是一种古老的、在今天不太为人所知的协议。首先下载题目抓包得到的流量包，然后在 wireshark 中打开，可以看到它是一段 TCP 流量，右键菜单 -> 追踪流 -> TCP 流，会弹出一个窗口显示 tcp 内部传输的内容。

我首先直接复制了一小段，贴到搜索引擎中，搜不到任何有用的结果。尝试使用 [scapy](https://scapy.net/) 分析流量，scapy 也不认识这是什么协议。实在想不到办法，我想到把 hexdump 格式的流量信息发给 chatgpt 碰碰运气，要知道 chatgpt 那可是遍观互联网，不一定聪明但见识可渊博了（

在几次修改问题、几次刷新 chatgpt 输出之后，惊讶地发现 chatgpt 终于给出了有用的信息：

> 给定的十六进制转储看起来与 ZMODEM 文件传输协议相关。ZMODEM 是一种文件传输协议，提供错误检查、压缩和自动重试功能，通常用于通过串行通信链路传输文件。
>
> 在十六进制转储中，你可以看到类似于 "**.B" 后跟数字的模式，这是 ZMODEM 控制序列的特征。开头的 `rz.` 也表明这是 ZMODEM；`rz` 是一个常用的 ZMODEM 文件接收程序。

（[点此查看导出的 chatgpt 对话](https://chat.openai.com/share/75ad0c3c-200e-400c-99cc-052260a1ff13)）

原来这是一个叫做 zmodem 的协议，搜索发现它是上世纪 80 年代的东西，那可真是古老。然后发现，其实不需要 chatgpt 也可以搜到结果，直接搜 `rz file transfer` 就可以了，我一开始复制的流量内容太多反而干扰了搜索。

然后我去 [archwiki](https://wiki.archlinux.org) 尝试搜索看看有没有相关页面，很可惜没有（毕竟这协议太古老了）。然后我在 archlinux 上搜索相关软件包，搜到了一个 `lrzsz`，其中提供了 zmodem 协议使用的 rz 和 sz 命令。可是安装之后，看了半天官网和手册也没搞明白这东西怎么用。接着搜索 lrzsz 的使用教程，搜到了这篇文章：[Using rz/sz to transfer files](https://gangmax.me/blog/2016/12/08/using-rz-slash-sz-to-transfer-files/)，其中提到可以使用支持 zmodem 的终端模拟器或者 GNU screen 来传输文件。于是打开一个 screen 会话，在里面运行 `nc prob05.geekgame.pku.edu.cn 10005` 连接到服务器，之后按文章所说的来操作，就拿到了服务器传来的第一个 flag。

### flag2

第一问都做出来了，第二问就很简单了。只需要重放抓包到的协议流量就可以了。

经过尝试，发现一次性输出全部抓到的数据是不行的，于是猜测数据包的先后顺序不能错。然后我写了一个脚本，把抓到的流量复制进去。它是一个 tcp 服务器，在连接到来时向终端输出接受到的数据，每按下一次回车就发送一段数据。之后在 screen 会话里用 nc 连接这个本地服务器，如法炮制，就拿到了 flag.jpg 文件。

[点此查看代码](q05-zserver/q2.py)。注意此代码依赖 python 第三方库 trio。

### 补充

实际上，赛后我才发现，除了古老的 lrzsz 之外，还有一个新的 zmodem 实现 [trzsz](https://github.com/trzsz/trzsz)。另外之前听说过一个基于 HTTP 的远程 shell 服务器 [ttyd](https://github.com/tsl0922/ttyd)，它也对 zmodem 有支持。

## prob24-password

## 基本功

这道题说得很明白，是破解 zip 文件的加密。题目说密码长度有 50 个字节，并且很可能是随机的，这就等于明示暴力破解不可能。这说明题目中 zip 文件的加密很可能存在弱点，我们需要利用它的弱点。

使用 7zip 打开压缩包，可以在“压缩”这一列看到算法是 `ZipCrypto Store`。某些别的工具应该也可以看到这一信息。经过搜索得知这表明数据未经压缩，然后直接使用 `ZipCrypto` 算法加密。与此同时，直接搜到了这篇文章：[Cracking encrypted archives (PKZIP: ZipCrypto)](https://www.acceis.fr/cracking-encrypted-archives-pkzip-zip-zipcrypto-winzip-zip-aes-7-zip-rar/)，其中提到 ZipCrypto 容易受到已知明文攻击，只需要知道文件的明文中至少 12 个字节的内容和位置，并且其中至少 8 个字节是连续的，就可以发动已知明文攻击。并且文中详细描述了使用 [bkcrack](https://github.com/kimci86/bkcrack) 执行此攻击的步骤。

### challenge_1

在 zip 格式中，每个文件都是单独存储的，互不相干。这意味着每个文件都是单独压缩、单独加密的。并且在 zip 中文件名是不加密的，打开本题的 zip 包，可以看到其中有两个文件，第一个是 `chromedriver_linux64.zip`，第二个是 `flag1.txt`。经过简单搜索，我没找到这里的 chromedriver_linux64 的原始文件，因此猜测这可能需要利用 zip 格式的某些能预先知道的元数据，就像上面文章里 svg 文件的 xml 头一样。

所以需要了解 zip 的基本文件格式。我搜到了[这个网页](https://docs.fileformat.com/compression/zip/)和 [Wikipedia 词条](https://en.wikipedia.org/wiki/ZIP_(file_format)#File_headers)。

可以得知，只要不是空的 zip 包，zip 文件开头 4 字节是以小端序存储的 `0x04034b50`，按字节顺序应该是 `50 4b 03 04`。

接下来 2 个字节是解压此文件所需的最低版本号，以小端序存储。尝试随便压缩点什么文件，以及观察电脑里现有的 zip 包，发现它可能是 `0a 00` 也可能是 `14 00`。观察文件的二进制数据可以使用 [xxd](https://man.archlinux.org/man/xxd.1) 命令，它是 vim 项目的一部分。另外 busybox 也有一个轻量版的 xxd 命令。配合 head 命令就可以查看文件的开头几十个字节。例如：

``` shell
$ head -c 30 challenge_1.zip | xxd
00000000: 504b 0304 0a00 0900 0000 2910 4d57 ecbb  PK........).MW..
00000010: 6ecf ac30 5900 a030 5900 1800 1c00       n..0Y..0Y.....
```

接下来 2 个字节表示“一般用途”，经过我的尝试和观察，它一般就是 `00 00`，但是本题目下发的两个 zip 包这两个字节都是 `09 00`，让人有点摸不着头脑。

接下来 2 个字节表示压缩算法。对于较小的文件，zip 实现可能默认不会压缩，而是直接存储，那么就是 `00 00`。如果文件不太小，就会使用默认的 DEFLATE 算法来压缩，那么就是 `08 00`。看上去这个文件不小，那么多半是经过压缩的。

这就是文件开头能猜测的全部内容了，但这还不够 12 字节。好在 zip 文件末尾还有一个 End of Central Directory Record 部分，如果它不包含注释那么长度就应该是 22 字节。并且 zip 包的文件原始长度（即明文长度）是已知的，是 5845152，那么就等于我们知道了文件结尾这一部分的偏移量，是 5845130。而这一部分的开头会有固定 4 字节 `50 4b 05 06`，这样就足够我们破解了。

上面有两个字段的值不能确定，只好一个一个尝试。每次爆破在我的电脑上都需要运行大约 1 小时，还是比较长的。最终成功的猜测是：

``` bash
xxd -r <(echo "00000000: 504b 0304 1400 0000 0800") > plain.dat
bkcrack -C challenge_1.zip -c chromedriver_linux64.zip -p plain.dat -x 5845130 504b0506
```

成功之后，bkcrack 输出了密钥 `a07691d6 69ff16f6 85e8542f`，我们假设 flag 文件也是用同一个密钥加密的（这是最常见的情况，并且如果不这样此题就无解了），使用如下命令解密 flag 即可：

``` shell
bkcrack -C challenge_1.zip -c flag1.txt -k a07691d6 69ff16f6 85e8542f -d flag1.txt
```

### challenge_2

我感觉这题的两问难度设置有点问题，感觉第二问明显比第一问简单。不过也可能是我第一问没找到那个原始文件，做复杂了。

这一问的 zip 包里只有一个文件，是 `flag2.pcapng`。在之前做 zserver 那题时我就好奇搜了一下，搜到了这个文件格式的[官网](https://pcapng.com/)，得知这是一个新一代的网络数据包格式，我对抓包了解不多，看上去似乎它已经是事实标准。它的官网就有这个文件格式的信息，使用上一问同样的方法就可以轻易且无歧义地猜测到足够用于攻击的名文。

首先文件的开头必须是一个 SHB 块，这个块开头固定有 4 个字节 `0a 0d 0d 0a`。下来 4 字节是块长度，它应该不太容易预测，就跳过它。再接下来也就是在偏移量 8 的位置，固定是 4 个标记字节序的字节，在小端序的情况下就是 `4d 3c 2b 1a`。因为现实中绝大部分机器都是小端的，所以可以合理假设这里就是小端。再接下来 4 个字节是版本号，但看上去现实中只有一个版本，那就是 `0x0001 0x0000` 表示 1.0 版，在小端序下就是 `01 00 00 00`。

到目前位置就已经有 12 个字节，足够破解了。不过官网还提到，接下来 8 个字节通常都是 `ff ff ff ff ff ff ff ff`，如果把这 8 字节也算进去，可以减少破解所需的时间。

最终使用的命令是：

``` bash
xxd -r <(echo "00000000: 4d3c 2b1a 0100 0000") > plain.dat
bkcrack -C challenge_2.zip -c flag2.pcapng -p plain.dat -o 8 -x 0 0a0d0d0a -d flag2.pcapng
```

实际我做题的时候，因为信了文章中说的“可以把 CRC 的最高一个字节添加到文件开头偏移量为 -1 的位置来当已知明文使用”，导致破解了好几次都失败，甚至尝试了大端序的情况。结果最后把那个画蛇添足的 CRC 字节去掉就成功了。所以不考虑这个插曲的话，在我的做法中第二问应该是比第一问简单的。

拿到解密的 pcapng 文件后，和 zserver 那题一样，在 wireshark 中打开，然后右键追踪 tpc 流，就可以拿到 flag。

## prob14-emoji

## Emoji Wordle

### Level 1

第一问答案固定，所以可以用一个简陋的算法来做。因为这是 emoji 而非真正的词语，没有固定组合，更没有词频，所以不能像 [3blue1brown 的视频](https://www.bilibili.com/video/av381782571/)里展示的方法那样求解。Wordle 是个挺有名的游戏，之前火过一段时间。如果你不了解 wordle 的规则可以自行搜索或者观看上面这个视频。

[点此查看代码](q14-emoji-wordle/solve.py)

代码里的算法不够聪明，实现得也比较复杂，不过我还是解释一下我的思路。

首先因为 emoji 没有固定的“词语”，所以假设 emoji 序列是随机生成的，并且每个位置是相互独立的。在求解过程中，每个位置都需要记住自己的状态，如果这个位置遇到了绿色，就记住这个位置的正确字符；如果这个位置遇到了黄色或者红色，就说明该字符并不存在于这个位置，这个位置需要把这些排除掉的字符记下来，之后不再尝试。

对于全局的状态，如果遇到了绿色那么不需要做什么事，因为每个具体的位置已经记住了答案。如果遇到了黄色，那么就说明整个序列中一定有某个位置存在这个字符，但无法确定出现了多少次（再一次，这与 [3blue1brown 的第二期视频](https://www.bilibili.com/video/av424966119/)中提到的原版 wordle 的算法不同）。而如果遇到了红色，就说明这个字符不存在于此序列中，需要从全局中排除掉。

在生成下一个猜测时，对整个序列从左向右迭代，每个位置猜测一个字符。当一个位置生成猜测时，如果这个位置已经猜到了正确的字符，那么它的任务就是帮助全局找到更多存在于这个序列的字符、排除掉更多不存在的字符。所以它需要从所以还从全局未尝试过的字符中随机选择一个，并且需要尽可能避免与该位置左侧已经猜测过的字符重复，如果重复那就造成了浪费。当所有字符都被尝试过至少一次后，这个位置就直接把之前猜对的字符放上去。

如果一个位置生成猜测时还没有猜到正确的字符，它既需要负责帮全局寻找字符、排除字符，也需要为自己这个位置寻找正确的字符。对于如何在二者之间选择，我使用了一个没有道理的启发式方法：比较全局还未尝试过的字符和该位置候选的字符，哪个数量更多就选择在哪个当中随机猜一个。一个位置的候选字符，指的是已知存在于序列中的字符（在别的位置出现黄色），去掉该位置已经排除掉的字符（在该位置出现黄色）。

上面这段算法，组成了代码中的 `gen_a_guess` 方法。

因为同一个字符可能重复出现，并且我们没法知道它出现了多少次，所以在我的算法里，一个位置猜对，对于其它位置而言不能提供信息。当然如果考虑每个字符随机生成，同一个字符在序列中出现次数越高的概率就越小，不过我没有在算法中考虑这一点。因此这个算法的每个位置在候选字符中猜测时，基本上就是暴力穷举，效率会很低。不过对于解出第一问来说足够了。

另外，在我最初的代码里，没有意识到题目中可能的 emoji 字符很少，而是使用了一个 python 库 [emoji](https://github.com/carpedm20/emoji)，使用了所有已知的只占一个 Unicode 码位的 emoji，总共有 1386 个。在做第二问时才意识到没有那么多。

### Level 2

做第二问时，我意识到题目使用的 emoji 总数应该没有那么多，用于在 html 中生成占位符的可能就是所有题目所用到的 emoji 了。于是我写了[一个脚本](q14-emoji-wordle/get_emoji_list.py)，抓取到了全部 128 个 emoji。发现这 128 个 emoji 的 Unicode 码位是连续的，从 `U+1f410` 到 `U+1f48f`。

即使如此，想要在 8 步内猜对的可能性也可以忽略不计。既然是 web 题，而本题的 html 和 js 非常简单，那只能看看 cookie 了。好在第二问的 cookie 呈现出非常明显的规律，这显然就是把 emoji 序列编码在 cookie 里了。

在 cookie 里可以看到明显不断重复的字符串 `"x1RDgzRF"`，并且刚好重复了 64 次，等于 emoji 序列的长度。而剩下的每一段数据长度为 8 个字节，并且前 5 字节实际上也是一样的，都是 `"x1REM"`，因此实际上只有最后 3 个字节编码了信息。

使用第一问的脚本对第二问的题跑了几遍，肯定不成功，但有少数 emoji 会猜对，这样就能拿到一些 cookie 编码与 emoji 的对应关系，从而分析其编码。观察到大部分 emoji 的编码末尾字节都是 `"1FVl"` 中的一个，并且对应的 Unicode 码位递增 1。也就是说，如果前 7 字节都一样，最后 1 字节是 `F` 的 emoji 的码位就比是最后 1 字节是 `1` 的 emoji 码位刚好大 1。

同样的方法分析，倒数第 2 字节有 `"MNOQR"` 几种可能，并且对应的 Unicode 码位大致递增 4，就像是“进了一位”。不过有不少例外情况。通过不断试错补充例外，最后得到了一张末尾 2 字节与 Unicode 码位的对应关系表，末尾 2 字节总共对应 16 个码位。详见代码中的 `table_map`。

同样，倒数第 3 字节有 `"z0123456"` 几种情况，对应的 Unicode 码位递增 16，这次没有例外。

不过上面所述的规律都不包括第 64 个位置的 emoji 也就是最后一个 emoji，不太了解原因，但只有这一个的话可以靠运气猜出来。

[点此查看将 cookie 解码为 emoji 的代码](q14-emoji-wordle/q2.py)

实际上，我觉得我这种方法做得太复杂了。如果要找 cookie 与 emoji 的对应关系，完全可以暴力枚举全部 128 个 emoji。预期解应该不是我这种非常麻烦的做法。

## prob01-homepage

## 第三新XSS

### flag1

在浏览器中，源（Origin）是个很重要的概念，它表示一个完整的由**协议**（例如 http 或 https）、**主机名**（例如 prob01.geekgame.pku.edu.cn，完整匹配，且不包括子域名）、**端口号**组成的三元组，如果有任何一个不同就认为不是同一个源。由于[同源策略](https://developer.mozilla.org/zh-CN/docs/Web/Security/Same-origin_policy)的保护，浏览器能够防止跨源的 js 访问数据。但是反过来说，对于同一个源之内的 js 脚本就基本等于不设防，一个路径的 js 可以访问另一个路径下的数据。

即使对上述内容了解得不清楚也不要紧，做题时只需要有一点模糊的印象就够了。因为本题需要从 cookie 中提取 flag，所以我们需要跨路径访问 cookie。这就可以查阅 [MDN 文档的 `document.cookie` 一节](https://developer.mozilla.org/zh-CN/docs/web/api/document/cookie)，这一节介绍了使用 js 访问 cookie 的接口。可以在其中的“安全”一节看到，文档明确说明了 cookie 的 path 属性不能保护 cookie 阻止来自 js 的访问，并且清楚地给出了一个例子，即：使用一个 iframe 元素引用另一个路径的页面，之后访问它的 `contentDocument.cookie` 属性。

实际操作中发现，执行 js 脚本时 iframe 可能还没有加载完成，因此先 sleep 500 毫秒。完整代码如下：

``` html
<html>
  <iframe id="admin_iframe" src="/admin/"></iframe>
  <script>
    function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    }
    async function main() {
      await sleep(500)
      let admin = document.getElementById("admin_iframe")
      let cookie = admin.contentDocument.cookie
      document.title = "cookie: " + cookie
    }
    main()
  </script>
</html>
```

### flag2

这一问我是第二阶段看到提示后才做出来的。

在第一阶段时，看到 xssbot 的源码，我不太熟悉 selenium 的 API，不过看到创建并关闭了 2 次 webdriver，猜测这可能相当于打开并关闭浏览器。在浏览器中存储的数据有不同的生命周期，有的是遵从会话（session）生命周期，在关闭标签页或关闭浏览器后就会消失。还有一些资源是持久（permanent）的，即使关掉浏览器也能长期保存，在下次打开浏览器后仍然有效。例如对于 cookie 而言，如果没有设置 `expires` 或者 `max-age` 属性的 cookie 就是会话生命周期的，如果设置了二者之一那么就是持久生命周期的，会在指定时间后过期。另一个例子是 [Web Storage API](https://developer.mozilla.org/zh-CN/docs/Web/API/Web_Storage_API)，其中 sessionStorage 具有会话生命周期，而 localStorage 具有持久生命周期且不会过期。

回到题目，本题在第一个会话中访问我们提供的页面，在第二个会话中访问 admin 页面并设置 cookie。这就意味着我们需要设置某种持久的资源，并且能在第二次会话中执行 js 读取 cookie。当时由于时间关系，本题我没有多考虑，直到第二阶段看到提示中说要使用 [service worker](https://developer.mozilla.org/zh-CN/docs/Web/API/Service_Worker_API)。在阅读本题解时，我也建议读者先阅读一下它的文档。

看了一下 service worker 的文档，想起来之前听说过也见过一种叫做 [PWA](https://developer.mozilla.org/zh-CN/docs/Web/Progressive_web_apps) 的技术，可以在浏览器中做到类似原生桌面应用程序的效果，其中就涉及到把网页缓存在本地，这样即使没有网络的情况下也可以使用 PWA 应用程序。而 PWA 用于实现缓存的方法就是 service worker。

使用 service worker 解决本题时，需要三个网页：一个页面交给 xssbot 直接访问，注册 service worker；一个页面用来提供 service worker 的 JavaScript 代码；一个页面包含实际读取 cookie、把 cookie 设置到网页标题的功能。第二个页面的 mime 文件类型是 `text/javascript`，另外两个都是 `text/html`。

具体过程是，首先 xssbot 访问第 1 个页面，在其中把第 2 个页面的 js 注册成 service worker，并且注册到网站的根目录：

``` html
<html>
  <script>
    async function main() {
      let registration = await navigator.serviceWorker.register(
        "../sw/", {scope: "/"},
      )
    }
    main()
  </script>
</html>
```

在提交页面里把这个 html 上传到网站的任意路径里。

然后在 service worker 的 js 里，我们需要拦截 fetch 事件，然后用我们自己的页面作为响应来替换 `/admin/` 上的页面：

``` js
self.addEventListener("fetch", (event) => {
    event.respondWith(handle_fetch_event(event))
})

async function handle_fetch_event(event) {
    return await fetch("/hijack/")
}
```

然后把这个 js 上传到网站的 `sw` 路径上，响应头中的 `Content-Type` 需要改成 `text/javascript`。

然后把读取 cookie 的页面上传到网站的 `hijack` 路径上：

``` html
<html>
  <script>
    function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    }
    async function main() {
      while (true) {
        let cookie = document.cookie
        document.title = "cookie: " + cookie
        await sleep(100)
      }
    }
    main()
  </script>
</html>
```

不过，这样实际操作的时候，会发现浏览器控制台中报错，说位于 `/sw/` 路径的 js 脚本不能作为 service worker 注册在网站根目录 `/` 上，除非在服务器响应这个 js 脚本时带上一个 `Service-Worker-Allowed` 响应头。在搜索引擎中搜索，在[一个 StackOverflow 问答](https://stackoverflow.com/questions/49084718/how-exactly-add-service-worker-allowed-to-register-service-worker-scope-in-upp)找到了答案，需要为 js 添加一个 `"Service-Worker-Allowed": "/"`，添加过后就成功拿到了 flag。

## prob13-easyts

## 简单的打字稿

### flag1

这是一道 typescript 类型体操的题。虽然我不熟悉 ts，不过我对 python 的静态类型提示（type hints）有所了解，它与 ts 有很多相似的地方：它们都是为动态类型语言添加的静态类型标注，属于“渐进类型” [[1]](https://peps.python.org/pep-0483/#summary-of-gradual-typing) [[2]](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-func.html#gradual-typing)；这些类型信息只在类型检查时生效，在运行时这些类型信息会被擦除、没有效果（即“类型擦除”）；都有泛型、子类型、并集类型、never 类型、字面值等概念。

静态类型是一个比较大的话题，在题解里受限于篇幅没法展开去讲，有兴趣的读者可以自行查阅一些有关 python 或 typescript 的资料。

阅读本题的源码，然后简单查阅一些 typescript 的文档，可以看到 flag1 是一个字符串字面值类型（是一个类型，而不是该类型的一个值）：

``` ts
type flag1 = 'flag{123}'
```

和 python 中的字符串字面值类型一样，它表示一个在静态检查时就知道完整内容的字符串，通常就是写死在源代码里的。在类型检查的时候，只有检查器能推断出字符串的内容刚好能对应上的时候，才会认为类型匹配，否则那些在运行时动态生成的字符串、不能提前预知内容，就会认为与字符串字面值类型不匹配。例如：

``` ts
// 类型匹配，检查通过
let foo: flag1 = 'flag{123}'
// 类型不匹配，报错
let bar: flag1 = 'flag{abc}'
let baz: flag1 = prompt('user input:')
```

更多例子可以在 [typescript playground](https://www.typescriptlang.org/zh/play) 在线尝试。

接下来我们需要知道如何把 flag1 的类型名称输出出来。在 python 中，通常是使用 [`reveal_type`](https://mypy.readthedocs.io/en/stable/common_issues.html#reveal-type) 函数来输出一个变量的类型，但 ts 里似乎没有等价的东西。不过经过搜索，[得知](https://stackoverflow.com/questions/56918574/can-i-get-typescript-to-reveal-what-type-it-has-determined-for-an-expression)可以直接给变量赋一个不匹配的类型的值，报错中就会包含类型的名称，例如：

``` ts
let foo: flag1 = "abc"
```

不过经过尝试以及阅读代码后发现，输出的内容不能包括 `flag` 这个字符串本身，否则就会“绷”。但是 flag 的字符串字面值一定是包含 `flag` 的，这该怎么办呢？

于是考虑能不能让报错只输出类型的一部分，这一步有点不太容易想到。一段时间思考后，我想起 python 中字符串可以切片，那么 ts 里在类型检查时就已知的字符串字面值能不能在类型检查时切片呢？如果字符串字面值类型可以切片，那么就可以切掉开头的 `flag` 输出剩下的信息。

按照这个思路搜索，很快搜到了一个 StackOverflow 问答：[Can I slice literal type in TypeScript](https://stackoverflow.com/questions/70831365/can-i-slice-literal-type-in-typescript)，下面的回答直接给出了答案，虽然不能切片，但可以 split。于是直接把回答里的代码复制过来，然后只要我们按左大括号 `{` 对 flag1 类型 split，然后使用右侧半边作为新的字符串字面值类型，就可以解决问题了。

代码如下：

``` ts
type Split<S extends string, D extends string> =
    string extends S ? string[] :
    S extends '' ? [] :
    S extends `${infer T}${D}${infer U}` ? [T, ...Split<U, D>] : [S];
type Foo = Split<flag1, "{">
let [a, b] = "" as unknown as Foo
let foo: "x" = b
```

这题第一问的最终解法已经远超我的预期，没想到 ts 的类型系统能玩出这么复杂的花活，据我所知不仅仅是 python，甚至 rust 也没有这么复杂。于是 flag2 我就直接放弃了。

## prob25-krkr

## 汉化绿色版免费下载

这题我是在二阶段提示下才做出来的

### flag1

一开始我的思路走错了，先运行了一遍程序，在结尾看到背景色与前景色一致的 flag1 后，就觉得需要读取内存寻找 flag，然后就开始用 x32dbg 调试了，但花了不少时间没有结果，就放弃了。

一段时间后看到做出来的人很多，又回来看看这题。考虑到存档中可能存有信息，所以我在结尾处存了一个档，然后搜索存档后缀名 `.kdt`，得知这是一个 galgame 框架 kirikiri 的存档格式，并且找到了存档解包工具 [`kirikiritools`](https://github.com/arcusmaximus/KirikiriTools)。然而解开存档后，发现是纯文本，但里面的内容根本看不懂是什么含义。尝试在题目提供的存档与我自己的存档上运行 `diff`，也看不明白存档信息究竟存储在哪里。于是又放弃了。

第二阶段，看到提示说要解包 xp3，我才意识到之前忘了这一点。经过搜索，才发现 krkr 并不是我想象中那样一个非常冷门的框架，而是个很常见的框架，许多 galgame 都使用了它，并且网上有不少解包工具和解包教程。（~~吃了没玩过 galgame 的亏~~）

我选择了 [GARbro](https://github.com/morkt/GARbro)，然后在解包得到的 `scenario` 目录中找到了本题目的源码。其中 flag1 就在 `done.ks` 当中。

### flag2

拿到源码后，看到其中的 `round1.ks` 和 `round2.ks`，才明白存档里写的信息是什么意思。看到 hash 变量记录了输入的 flag，但是它是 flag 的字符经过一系列模 19260817 的乘法和加法运算后得到的，很难从中反推出原始 flag。

不过提示说解包两个 `.ksd` 文件看看，我第一问就注意到，即使不做任何操作，游戏启动时也会读取和写入这两个文件。现在带着源码回头来看，看到 `datasu.ksd` 里很可能记录了每个字母出现的次数，尝试开了一轮游戏输入了一次字母 u，然后把新的 datasu 与旧的 datasu 使用 diff 命令比较，可以确定下来是 `trail_round1_sel_*` 这些变量分别表示每个字母出现了多少次。

``` shell
$ sort prob25/savedata/datasu.ksd.bak | grep '"trail_round1_sel'
 "trail_round1_sel_a" => int 6,
 "trail_round1_sel_e" => int 3,
 "trail_round1_sel_end" => int 17,
 "trail_round1_sel_fin" => int 1,
 "trail_round1_sel_i" => int 1,
 "trail_round1_sel_loop" => int 18,
 "trail_round1_sel_o" => int 6,
```

于是可知，字母 a 出现 6 次，e 出现 3 次，i 出现 1 次，o 出现 6 次，字母 u 没有出现，共计 16 个字母。

这样问题就简单了，由排列组合知识可知，符合要求的可能性总共有 `C(16, 6) * C(10, 6) * C(4, 3) * C(1, 1) == 6726720` 种，数量很小，写代码逐个尝试即可，不到一分钟即可得到结果。

[点此查看代码](q25-krkr/q2.py)

## prob09-easyc

## 初学 C 语言

### flag1

只要对C语言有所了解，阅读代码后很快就能发现问题：用户输入的字符串被直接传递给 `printf` 的第一个参数作为格式字符串。实际上不仅仅是C语言，任何编程语言里使用不受信任的字符串作为格式字符串都是安全漏洞，除非文档明确说明可以接受不信任的字符串模板。比如 python 有一个很有名的坑：[格式字符串可以访问任意变量](https://realpython.com/python-string-formatting/#4-template-strings-standard-library)。另外 2021 年末著名的 [log4shell](https://www.techsolvency.com/story-so-far/cve-2021-44228-log4j-log4shell/) 漏洞，当时影响了大量基于 java 的服务器，包括 minecraft 在内。这个漏洞也是把不受信任的字符串当作格式字符串从而导致了远程代码执行漏洞。

C语言当然也有此问题，只是具体表现形式不同，这就要说到C语言的可变参数函数。为了实现可变参数函数，ABI 要求调用方把可变参数一个一个 push 到栈上，而被调用方从栈顶往下一个个读就能按顺序读，就可以读到全部的可变参数。

但是，被调用方并不知道总共传递了多少个可变参数，它只是在栈上一个个往下读，这就意味着利用这一点，我们可以读取整个栈的内存。在 ctf-wiki 对此也有介绍：[格式化字符串漏洞](https://ctf-wiki.org/pwn/linux/user-mode/fmtstr/fmtstr-intro/)。我们只需要使用一连串 `%p` 或者 `%016llx` 就能输出栈的数据，再从 16 进制转换回原始字节就能获取到 flag1，转换时要注意字节序，x86_64 是小端序架构。

关于C语言的 printf 支持哪些语法，详见 [cppreferece](https://zh.cppreference.com/w/c/io/fprintf)。此外，posix 还规定了一种语法，[可以直接读取第 n 个参数](https://man.archlinux.org/man/fprintf.3p#:~:text=Conversions%20can%20be%20applied%20to%20the%20nth%20argument%20after%20the%20format%20in%20the%20argument%20list%2C%20rather%20than%20to%20the%20next%20unused%20argument.)，例如：

``` c
printf("%165$p")
```

就可以读取相当于第 165 个参数的位置的栈内存，并且以指针格式输出。这大大方便了我们利用此漏洞。

做本题时我是在 ipython 中交互式完成的。我的代码里的 `get_data` 函数和 `xxd_data` 函数封装了读取、解析并输出栈内存的功能。[点此查看代码](q09-easyc/solve.py)

### flag2

这应该是这次我花时间最多的一题了。这是我第一次通过写入栈内存，从而构造任意代码执行。

首先阅读源码，其中的注释提到 flag2 需要在别处读取，那么等于明示这题需要利用漏洞获取 shell。但 printf 只能读取内存，没法写入，该怎么办呢？或者，其实 printf 可以协议内存？

是的，printf 可以写入内存。如上面 cppreference 文档所示，以及 ctf-wiki 也提到，printf 支持一个 `%n` 格式，它不是格式化输出参数，而是把这个参数的值当作一个指针，然后把到目前为止写入的字符数写入到这个指针对应的内存中去。它也支持 `%hhn` 这样一次只写入一个字节。

于是，我们只要确定好我们可以控制的 buf 内存是第几个参数，然后在对应位置处写入我们想要写入的地址，就可以使用 `%hhn` 来写入任意内存了。因此参照 ctf-wiki 的[栈缓冲区溢出](https://ctf-wiki.org/pwn/linux/user-mode/stackoverflow/x86/stack-intro/)一章，覆盖掉函数返回的地址，把控制流导向我们想要执行的代码。

顺便一提，如果是不熟悉汇编、调用约定、系统调用的读者，我推荐阅读一下这篇文章，非常适合入门：[Raw Linux Threads via System Calls](https://nullprogram.com/blog/2015/05/15/)

做本题时需要使用 gdb 在本地调试，我搜到了一个 [gdb cheatsheet 速查表](https://gist.github.com/rkubik/b96c23bd8ed58333de37f2b8cd052c30)，对不熟悉 gdb 的用户（比如我）很有帮助。

因为本题目的可执行文件开启了不可执行栈保护，我们不能直接在栈上写入 shellcode 然后跳转执行，所有需要使用 ctf-wiki 提到的 ROP（面向返回编程）技巧。我这里选择了 [ret2syscall](https://ctf-wiki.org/pwn/linux/user-mode/stackoverflow/x86/basic-rop/#ret2syscall) 方案，使用 `ROPgadget` 命令来寻找可利用的指令，从而写入寄存器，调用 `execve` 系统调用。

另外，本题的代码是使用 `-static-pie` 链接的，这意味着它是静态链接，并且是位置无关代码，也就是说代码指令在内存中的地址在每次执行之间可能变化，但指令之间的相对偏移量不会变。在写入跳转地址的时候要注意根据偏移量来计算真正的地址。

最后，通过 `execve` 系统调用来执行 `/bin/bash` 即可获得 shell，拿到 flag2。本题一开始我是执行 `/bin/sh`，还纳闷为什么本地成功，在服务器上就失败。第二天我才想起来可能是执行命令的路径不对。

[点此查看代码](q09-easyc/solve.py)

## prob07-noexec

## 禁止执行，启动

### flag1

本题目的执行环境比较特殊，它自定义了一个 `get_flag` 系统调用，并且除了 `/bin` 目录之外的可执行文件都不允许执行，而 `/bin` 目录不可写。

在做出上面 C 语言这题的第二问之后，这题的 flag1 就很好解决了。使用 lldb 调试器在随便哪个会执行到的 ret 指令处下一个断点，修改内存和寄存器，从而调用 `get_flag` 系统调用。关于 lldb 与 gdb 使用上的区别，可以参阅 [lldb 文档](https://lldb.llvm.org/use/map.html)。

[这是我做题过程中用到的一些命令](q07-noexec/q1.txt)

## prob04-filtered

## 关键词过滤喵，谢谢喵

这是一个有趣的 [esolang](https://en.wikipedia.org/wiki/Esoteric_programming_language) 题目，核心是正则表达式替换。

阅读代码发现，`重复把【foo】替换成【bar】喵` 的实现是在字符串上循环调用 python 标准库的 [`re.sub`](https://docs.python.org/zh-cn/3/library/re.html#re.sub)，这与 `sed 's/foo/bar/g'` 的语义不同，第一次替换生成的字符仍然会参与下一次查找替换。因此在编写代码时注意到这一点很重要。

### 字数统计喵

这题的思路有点像小游戏 2048 或者“合成大西瓜”，把代表低位数字的字符“合成”成代表高位数字的字符。

具体思路是，先把所有字符都替换成同一个字符，然后每 10 个字符合并成另一个字符，重复进行这样的合并，最终根据剩余字符的数量来替换成对应的 0 到 9 的数字，就成功得到十进制的字符数量。另外要注意遇到 0 时判空的问题。

[点此查看代码生成脚本](q04-filtered/q1.py)

[点此查看代码](q04-filtered/q1.txt)

### 排序喵

排序当中最重要的操作就是比较和交换，但我想不到如何使用正则替换实现比较长度。所以我选择了一种粗暴的办法，从长度 1 开始往上枚举，先把所有长度 1 的行挪到最前面，然后是长度 2 的行，以此类推。在 64 kB 的限制下，我的代码最多能支持一行 873 个字符的情况。好在本题没有卡单行长度，不然这题我就做不出来了。

[点此查看代码生成脚本](q04-filtered/q2.py)

[点此查看代码](q04-filtered/q2.txt)

## prob21-gzip

## 未来磁盘

### flag1

本题我是在二阶段提示下做出来的。可惜时间所限，不然我在一阶段时会去找资料学一下 deflate 流的格式。

首先根据一阶段提示，尝试压缩 `/dev/zero`，看到先是输出大量的 `00`，在大约 1024 字节后会开始大量输出 `55`，但会周期性地输出少量别的字节。如果在全零字节中间插入一小段文本代表 flag，会发现后面的压缩字节变成 `aa`。这应该就能用来寻找 flag 的位置。

首先用 `zcat` 命令和 `file` 命令来弄清楚文件被压缩了几次：

``` shell
$ zcat flag1.gz | file -
/dev/stdin: gzip compressed data, max compression, from TOPS/20
$ zcat flag1.gz | zcat | file -
/dev/stdin: gzip compressed data, max compression, from TOPS/20
$ zcat flag1.gz | zcat | zcat | file -
/dev/stdin: data
$ zcat flag1.gz | zcat | zcat | head -c 1024 | xxd -a
00000000: 0000 0000 0000 0000 0000 0000 0000 0000  ................
*
000003f0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
$ zcat flag1.gz | zcat | wc -c
7547056623
$ numfmt --to=iec --format="%.2f" 7547056623
7.03G
```

这说明 flag1 被压缩了 3 次，压缩一次后的文件有大约 7G。

接下来寻找 `aa` 字节首次出现的位置：

``` shell
zcat flag1.gz | zcat | pv -s 7547056623 | hexdump | grep 'aaaa aaaa aaaa aaaa' -m1
```

找到对应的偏移量是 3773534560。然后寻找 flag 压缩数据的起始位置：

``` shell
zcat flag1.gz | zcat | pv -s 7547056623 | head -c 3773534560 | tail -c 65536 | hexdump
```

最后找到正确的偏移量，导出这一部分：

``` shell
$ zcat flag1.gz | zcat | pv -s 7547056623 | head -c 3773534560 | tail -c 4218 | head -c 64 | tee out2.gz | xxd
00000000: d8a1 6313 0061 2000 802b 252b d884 74d6  ..c..a ..+%+..t.
00000010: 368f 8144 04d3 d88a bb0b ce71 37c2 fdc6  6..D.......q7...
00000020: b51f cf4c 778f b2d5 35c6 997b b434 9757  ...Lw...5..{.4.W
00000030: 0d00 0000 0000 0000 0000 0000 0000 0000  ................
```

根据二阶段提示，说可以去除重复周期出现的部分，于是从文件开头导出一段包含 `55` 字节的部分，合并在一起解压：

``` shell
$ zcat flag1.gz | zcat | head -c $((0x2022)) > out.gz
$ cat out.gz out2.gz | zcat | xxd -a
00000000: 0000 0000 0000 0000 0000 0000 0000 0000  ................
*
0080f6f0: 0000 0000 0066 6c61 677b 6d30 7265 5f47  .....flag{m0re_G
0080f700: 5a49 505f 6669 3165 5f62 306d 427d 0000  ZIP_fi1e_b0mB}..
0080f710: 0000 0000 0000 0000 0000 0000 0000 0000  ................

gzip: stdin: unexpected end of file
*
0082b680: 0000 0000 0000                           ......
```

即可获得 flag。

## prob08-cookie

## 小章鱼的曲奇

### Smol Cookie

阅读代码，本题提供了一个 python 随机数序列的 2500 个字节。首先阅读官方文档可知，它使用的算法是梅森旋转算法，经过搜索可知它可以轻易根据输出重建内部状态，从而预测未来的输出字节。

我搜到了当时 python 提出标准库 secrets 时的 [PEP 506](https://peps.python.org/pep-0506/)，其中引用了 Tim Peters 的一段重建 Random 随机数生成器内部状态的代码：https://mail.python.org/pipermail/python-ideas/2015-September/036077.html

我把这段代码放在了 [crack_mt.py](q08-cookie/crack_mt.py) 里。然后就能轻易解出本题。[点此查看代码](q08-cookie/q1.py)

### SUPA BIG Cookie

阅读第二问的判题代码后，发现第三问的判题代码明显存在疏漏，第二问里检查了我们提供的随机种子与服务器提供的随机种子是否一致，而第三问没有，于是有一个非常 trivial 的解。

[点此查看代码](q08-cookie/q3.py)
