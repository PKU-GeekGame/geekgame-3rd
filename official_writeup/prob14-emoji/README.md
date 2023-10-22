# [Web] Emoji Wordle

- 命题人：debugger
- Level 1：150 分
- Level 2：150 分
- Level 3：200 分

## 题目描述

<blockquote>
<p>⬛⬛🟨⬛⬛</p>
<p>⬛⬛🟨⬛🟩</p>
<p>🟨⬛🟨🟩🟩</p>
<p>🟩🟩⬛🟩🟩</p>
<p>🤡🤡🤡🤡🤡</p>
</blockquote>
<p>你能在规定的次数之内猜出由 64 个 Emoji 组成的 Wordle 吗？猜测结果正确就能拿到 Flag。</p>
<p><strong>补充说明：</strong></p>
<ul>
<li>Level 1 的答案是固定的；Level 2 和 3 的答案是随机生成并存储在会话中的。</li>
<li>此题属于 Web 而非 Algorithm。解出此题无需知道答案的生成算法。</li>
</ul>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>本题使用了 Play Framework。这是一种无状态 Web 框架，其实服务器什么都没有存储。</li>
<li>可以看看 <a target="_blank" rel="noopener noreferrer" href="https://www.playframework.com/documentation/2.8.x/SettingsSession">它的 Session 实现</a>，留意一下每次请求 Cookie 发生了什么变化。</li>
<li>另外，输入框里面的 Placeholder 是从 128 个 Emoji 中随机（有放回）抽取 64 个，但是答案只会涉及 64 种 Emoji。在知道答案涉及的 64 种 Emoji 的前提下，可以用 64 次猜测得到答案。</li>
</ul>
</div>

**【网页链接：访问题目网页】**

## 预期解法

此题前两个level仅仅是铺垫，第一个level可以直接爆破（答案是固定的，不带Cookie可以猜任意多次），第二个level直接把答案写在Session里面，而Session是编码在Cookie里面。

首先要知道题目使用了Play Framework，这点搜索题目用的Cookie名称（PLAY_SESSION）就能知道。根据搜索或者Play Framework的官方文档可以知道Play Framework是一种无状态的Web框架，Cookie里面存储了JWT编码的Session。

因此，可以通过还原Cookie的方式把Session回退到旧状态，从而实现任意次猜测。如果每一位都猜64次，那么最多需要4096次才能猜出答案，这不是理想的做法（虽然并行发送请求仍然可能能在一分钟内发4096个请求）。

在知道是哪64种emoji的前提下，第一次猜64个emoji1就能知道哪些位置是emoji1；第二次猜64个emoji2；……这样64次就能把答案猜出来。但是拿到flag还需要一次猜测。其实第64次猜测是不需要的，因为排除了前63种emoji后剩下的位置只能是第64种emoji。也就是说，Level 1可以完全不通过修改Cookie解出。

至于怎么知道是哪64种emoji，可以从所有emoji字符中每次取64个emoji字符给Level 3（如果请求不带Cookie，每次会重新生成一个答案），对同一组emoji重复多次，这样就能知道某个emoji是否可能出现在答案中。或者Level 2的Cookie里面就包含了答案，生成大量答案，看里面有哪些不同的字符。

以下是Level 3的求解脚本。把level3换成level2或level1可以解出另两个Level。

```python
def solve():
    cookie=requests.get("https://prob14.geekgame.pku.edu.cn/level3").cookies
    v=[0]*64
    x=[chr(i+0x1F410) for i in b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"]
    for z in x:
        print(x.index(z))
        p=[ord(i) for i in requests.get("https://prob14.geekgame.pku.edu.cn/level3?guess="+z*64,cookies=cookie).text.split()[28][14:-2]]
        for j in range(64):
            if p[j]==129001:
                v[j]=z
    return requests.get("https://prob14.geekgame.pku.edu.cn/level3?guess="+''.join(v),cookies=cookie).text

solve()
```

另外本题把之前的猜测结果存储到LocalStorage里面，因为服务器没有存储任何信息，而Cookie有4096字节长度限制，所以也不能存到Session里面。

### 命题背景

本题的思路来自[VolgaCTF 2023 Qualifier的Muk-jji-ppa一题](https://r3kapig-not1on.notion.site/VolgaCTF-2023-Qualifier-Jeopardy-37275b59a8a740ff9c75e16f2c03cf80)，该题用Go实现了一个网页游戏，没有提供代码，但是简单尝试可以发现服务器是无状态的，于是Game Over了可以把旧的Cookie还原回来重试。之前又知道Play Framework是一种无状态的网页框架，因此就想利用Play Framework出一道题目。本来想出的是扫雷，但是ranwen在本届出了一个扫雷，所以就换了一个别的游戏。
