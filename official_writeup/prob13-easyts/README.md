# [Web] 简单的打字稿

- 命题人：thezzisu
- Super Easy：300 分
- Very Easy：200 分

## 题目描述

<p><marquee direction="up" scrollamount="4" height="350"></p>
<blockquote>
<p>尊敬的用户,您好!</p>
<p>我们深刻认识到,大力推广使用TypeScript这门优秀的编程语言,将对我国社会主义现代化建设产生深远的正面影响。我们梳理了TypeScript与现代化建设的结合点,并进行了详细阐述,请您评价。</p>
<p>第一,TypeScript将提升我国软件和信息技术产业水平,强力促进经济增长。信息技术深入各行各业,软件产业已成为支柱产业。TypeScript作为新一代编程语言,将大幅提高软件开发效率和质量,降低开发成本。这将使我国软件企业在国际市场更具竞争力,抢占更大市场份额。软件产业的腾飞必将拉动整个电子信息产业的发展,为经济增长提供强大动力。信息技术进步也将使传统产业智能化升级,推动经济结构优化。</p>
<p>第二,TypeScript将提升程序员工作效率,降低企业人力成本。TypeScript编程更高效,企业用人更少,可将节省的人力资源投入到创新领域。程序员效率提升速度超过工资上涨速度,企业的人力成本将明显降低。这将减轻企业运营压力,使更多资源向技术创新聚集,推动产业结构升级。同时,新的就业岗位将涌现出来,吸纳更多人才,促进社会主义市场经济的繁荣与发展。</p>
<p>第三,TypeScript在“双碳”目标、生态文明建设中具有重要应用前景。TypeScript可广泛应用于环境监测、气候模型、碳排放统计等领域的软件开发,大幅提高工作效率。这将为制定气候政策、评估碳中和路径提供强有力的技术支持。利用TypeScript打造的环境管理系统,也将助力环境污染治理和生态文明建设。一个绿色的中国,才是一个美丽的中国。</p>
<p>我们呼吁北大等高校里富有社会责任感的青年学子,在学习TypeScript技能的同时,将之用于服务国家发展大局。让我们继续在信息技术进步的道路上阔步前行,以TypeScript为工具,建设一个我们夢想中的社会主义现代化强国,以人民为中心,实现中华民族伟大复兴!</p>
</blockquote>
<p></marquee></p>
<p>显然，题面要是让 Claude 生成，就会变成上面那个鬼样。</p>
<p>不过前人说，TypeScript 确实很安全，至少对于类型来说更是如此。那么若我<strong>把 Flag 放在类型里</strong>，阁下又将如何应对？</p>
<div class="codehilite" style="background: #f8f8f8"><pre style="line-height: 125%;"><span></span><code><span style="color: #008000; font-weight: bold">type</span> flag1 <span style="color: #666666">=</span> <span style="color: #BA2121">&#39;flag{...}&#39;</span>
<span style="color: #008000; font-weight: bold">type</span> flag2 <span style="color: #666666">=</span> object <span style="color: #666666">|</span> { <span style="color: #AA22FF; font-weight: bold">new</span> ()<span style="color: #666666">:</span> { v<span style="color: #666666">:</span> () =&gt; (a<span style="color: #666666">:</span> (a: <span style="color: #B00040">unknown</span>, b<span style="color: #666666">:</span> { <span style="color: #BA2121">&#39;flag{...}&#39;</span><span style="color: #666666">:</span> never } <span style="color: #666666">&amp;</span> Record<span style="color: #666666">&lt;</span><span style="color: #B00040">string</span>, <span style="color: #B00040">string</span><span style="color: #666666">&gt;</span>) =&gt; never) =&gt; unknown } }

<span style="color: #3D7B7B; font-style: italic">// your code here</span>
</code></pre></div>

<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>如果 JS 无法直接输出 Flag，那我们就利用类型检查器的报错来输出 Flag。</li>
<li>输出包含 <code>flag</code> 就会绷，但是能不能转化成没有 <code>flag</code> 的内容多次输出呢？</li>
</ul>
</div>

**【网页链接：访问题目网页】**

**[【附件：下载题目源码（prob13-src.tar.gz）】](attachment/prob13-src.tar.gz)**

## 预期解法

### Flag1

Flag被包含在类型中，因此无法在JavaScript里获取到（TS类型抹除）。因此，我们需要通过类型检查器的报错来获得Flag。

首先，考察如下最简单的情形：

```ts
type flag = 'flag{...}';
let a: flag = 1;
```

将会在stdout产生如下报错：

```
error: TS2322 [ERROR]: Type '1' is not assignable to type '"flag{...}"'.
let a: flag = 1;
    ^
    at file:///.../$deno$stdin.ts:2:5
```

可以发现，这个时候flag就被带出来了。Very easy, isn't it?

第二步，就是如何绕过对 `/flag/i` 正则的匹配检查。由于这个检查非常弱，以下是几种可能的解方法：

#### 转换字符串为数字

```ts
type filter_helper<T extends string> = T extends 'a' ? `97,` : T extends 'b' ? `98,` : T extends 'c' ? `99,` : T extends 'd' ? `100,` : T extends 'e' ? `101,` : T extends 'f' ? `102,` : T extends 'g' ? `103,` : T extends 'h' ? `104,` : T extends 'i' ? `105,` : T extends 'j' ? `106,` : T extends 'k' ? `107,` : T extends 'l' ? `108,` : T extends 'm' ? `109,` : T extends 'n' ? `110,` : T extends 'o' ? `111,` : T extends 'p' ? `112,` : T extends 'q' ? `113,` : T extends 'r' ? `114,` : T extends 's' ? `115,` : T extends 't' ? `116,` : T extends 'u' ? `117,` : T extends 'v' ? `118,` : T extends 'w' ? `119,` : T extends 'x' ? `120,` : T extends 'y' ? `121,` : T extends 'z' ? `122,` : T extends 'A' ? `65,` : T extends 'B' ? `66,` : T extends 'C' ? `67,` : T extends 'D' ? `68,` : T extends 'E' ? `69,` : T extends 'F' ? `70,` : T extends 'G' ? `71,` : T extends 'H' ? `72,` : T extends 'I' ? `73,` : T extends 'J' ? `74,` : T extends 'K' ? `75,` : T extends 'L' ? `76,` : T extends 'M' ? `77,` : T extends 'N' ? `78,` : T extends 'O' ? `79,` : T extends 'P' ? `80,` : T extends 'Q' ? `81,` : T extends 'R' ? `82,` : T extends 'S' ? `83,` : T extends 'T' ? `84,` : T extends 'U' ? `85,` : T extends 'V' ? `86,` : T extends 'W' ? `87,` : T extends 'X' ? `88,` : T extends 'Y' ? `89,` : T extends 'Z' ? `90,` : T extends '0' ? `48,` : T extends '1' ? `49,` : T extends '2' ? `50,` : T extends '3' ? `51,` : T extends '4' ? `52,` : T extends '5' ? `53,` : T extends '6' ? `54,` : T extends '7' ? `55,` : T extends '8' ? `56,` : T extends '9' ? `57,` : T extends '!' ? `33,` : T extends '_' ? `95,` : T extends '{' ? `123,` : T extends '}' ? `125,` : T extends '-' ? `45,` : T extends '' ? '' : never
type filter<T extends string> = T extends `${infer U}${infer U1}` ? `${filter_helper<U>}${filter<U1>}` : T extends `${infer U}` ? `${filter_helper<U>}` : never
```

如上可直接将flag串转化为ASCII编码的字符串。

#### 一次带出三个字符

类似地，可以用generic type对字符串literal实现substring功能，一次带出三个字符，从而绕过正则匹配。

#### 枚举字符

当然你也可以每次枚举下一个字符。

### Flag2

Flag2其实就是简单的类型体操。

```ts
type Helper21 = flag2 extends object | infer U ? U : never
type Helper22 = Parameters<Parameters<ReturnType<InstanceType<Helper21>['v']>>[0]>[1]
type Helper23 = Helper22 extends {
  [K in infer K1]: never
} & Record<string, string>
  ? K1
  : never
```

带出`Helper23`即为Flag1的情形。

## 花絮

1. 笔者本来想出更类型体操的题，但是这题的定位是送分题，故简化为此。
2. 转换字符串为数字是标准做法，但也没有卡其他的可能做法。
3. 为了避免掐头去尾带出Flag，你会发现两个flag的内部都有flag这个子串😋。
4. Deno是好东西。做Node题累了，换个环境也是不错的。
