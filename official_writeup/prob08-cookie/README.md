# [Algorithm] 小章鱼的曲奇

- 命题人：Mivik
- Smol Cookie：150 分
- Big Cookie：250 分
- SUPA BIG Cookie：300 分

## 题目描述

<p>Smol Tako 是一只小章鱼。</p>
<p>众所周知，章鱼都很喜欢吃曲奇。作为一名资深的曲奇评论家，Smol Tako 更是只身前往世界各地，寻找最美味、最具特色的曲奇。</p>
<p>终于，跟随一张古老的藏宝图，Smol Tako 来到了 ⱦħē łⱥꞥđ ꝋӻ đēłīꞡħⱦ。据说，在这里的深渊，驻守着 Ancient Tako，它守护着世界上最美味的曲奇。但 Ancient Tako 使用的语言是古神之语，Smol Tako 无法理解。它找到了精通网络安全的你，希望你能帮助它翻译古神之语，让它获得曲奇。</p>
<blockquote>
<p>我去，<a target="_blank" rel="noopener noreferrer" href="https://b23.tv/HNVDJ9z">管人吃</a>！</p>
</blockquote>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>Flag 2: 可以看看 <a target="_blank" rel="noopener noreferrer" href="https://github.com/python/cpython/blob/main/Modules/_randommodule.c">Python 的 Random 实现</a>。</li>
<li>Flag 3: 由于出题人不慎少判断了一个条件，此题存在一个非常简单的非预期解。</li>
</ul>
</div>

**[【附件：下载题目附件（prob08-server.py）】](attachment/prob08-server.py)**

**【终端交互：连接到题目】**

## 预期解法

出题人的话：本题来自于出题人在 SECCON 2022 Qual 的一次怨念。当时题目需要构造一个能生成满足指定条件随机数序列的种子，但本人误以为 `signal.alarm(100)` 中的单位是 `ms`，于是花半天搓了一个很快的算法，结束后看别人 z3 一把梭感觉好崩溃。后来稍微改了一下整出了这个题面，但非常弱智地漏判了一些情况，并且没有找人验题，导致了一堆非预期。私密马赛，给大家磕个头。

### Flag1

第一个 flag 实际上泄露了 python random 的前 2500 个 bytes。如果对 python random 的实现比较熟悉的话，不难得知其适用的伪随机数算法（MT19937）是不密码学安全的；即，在得知其一个 round 的状态（624 个 uint32，即 2496 bytes）便可以反推出其内部状态，从而预测随机数序列。具体做法可见 [梅森旋转算法(MT19937)及其逆向详解](https://zhuanlan.zhihu.com/p/599672127)，这里不再赘述。

### Flag2

第二个 flag 给我们了一个 seed，要求我们给出另一个 **不同的** seed，这两个 seed 生成的随机数序列会和另一个随机数序列进行异或，按照和第一个 flag 相似的方式加密了 2500 个空字节再加上 flag。注意到，这个随机数序列并非是从头开始的，而是提前消耗了前 `entropy` 个字节。我们不妨构造一个与 `seed1` 不同的 `seed2`，使得他们生成的随机数序列完全一致。

如果去深挖 python 中 random 模块 MT19937 初始化的实现，会发现其并非是典型的初始化，而是先使用固定的种子（`19650218`）初始化后再根据一套算法扰动了 `mt` 数组（见 [\_randommodule.c](https://github.com/python/cpython/blob/4091deba88946841044b0a54090492a2fd903d42/Modules/_randommodule.c#L214)）。

```c
static void
init_by_array(RandomObject *self, uint32_t init_key[], size_t key_length)
{
    size_t i, j, k;       /* was signed in the original code. RDH 12/16/2002 */
    uint32_t *mt;

    mt = self->state;
    init_genrand(self, 19650218U);
    i=1; j=0;
    k = (N>key_length ? N : key_length);
    for (; k; k--) {
        mt[i] = (mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 30)) * 1664525U))
                 + init_key[j] + (uint32_t)j; /* non linear */
        i++; j++;
        if (i>=N) { mt[0] = mt[N-1]; i=1; }
        if (j>=key_length) j=0;
    }
    for (k=N-1; k; k--) {
        mt[i] = (mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 30)) * 1566083941U))
                 - (uint32_t)i; /* non linear */
        i++;
        if (i>=N) { mt[0] = mt[N-1]; i=1; }
    }

    mt[0] = 0x80000000U; /* MSB is 1; assuring non-zero initial array */
}
```

为了能完全控制 `mt`，我们不妨构造一个长度为 `N` 的 key，将整个算法用 z3 实现一遍求解即可。

#### 非预期解

1. 由于 random 模块对数字类型种子取了绝对值，种子直接取反即可得到相同的输出状态。
2. 直接枚举 entropy…
3. 更牛逼的来了，研究一下发现多个 MT19937 异或起来等价于一个 MT19937，为什么呢？？因为整个 twist 过程的操作包括异或都是都是都是结合的啊啊!!?直接用 flag1 的 exp 就做出来了我天，写到这里出题人已经失去活下去的欲望了，正在找个地把自己埋了。怎么会有这种弱智的啊啊啊啊啊啊？？？？？人哪有不疯的？硬撑罢了！人哪有不疯的？硬撑罢了！人哪有不疯的？硬撑罢了！人哪有不疯的？硬撑罢了！人哪有不疯的？硬撑罢了！人哪有不疯的？硬撑罢了！人哪有不疯的？硬撑罢了！人哪有不疯的？硬撑罢了！

### Flag3

第三个 flag 干的是一样的事，只不过有了较严格的时间限制。不妨再仔细观察上面的代码，其中，下面一个 `for` 是完全可逆的。而对于上面的 `for`，我们也可以容易地构造一个长度为 `N` 的 key。构造代码如下：

```python
def construct(seed):
    mt = list(Random(seed).getstate()[1])[:-1]

    assert mt[0] == (2 ** 31)
    mt[0] = mt[-1]

    i = 2
    for k in range(1, N):
        if i == 1:
            i = N
        i -= 1
        mt[i] += i
        mt[i] ^= (mt[i - 1] ^ (mt[i - 1] >> 30)) * 1566083941
        mt[i] &= mask

    mt[0] = mt[-1]

    key = []
    i = 2
    j = 624
    for k in range(N):
        if i == 1:
            i = N
        i -= 1
        j -= 1
        m = mt[i]
        m -= j
        t = ma[i]
        if not k:
            t = mt[i]
        m -= t ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1664525)
        if i == 1:
            mt[i - 1] = ma[0]
        key.append(m & mask)

    s = 0
    for k in key:
        s = (s << 32) | k

    return s
```

#### 非预期解

1. 出题人忘判 seed 不相等，直接给出 seed 即可。
2. 由于用的是 zip，直接构造一个种子就行。
