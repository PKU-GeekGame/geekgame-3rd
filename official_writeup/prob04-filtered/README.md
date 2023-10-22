# [Algorithm] 关键词过滤喵，谢谢喵

- 命题人：MaxXing
- 字数统计喵：150 分
- 排序喵：250 分
- Brainfuck 喵：250 分

## 题目描述

> 一段题目描述里的申必代码：

```html
<style>
body>#root>.ant-app .header .header-nav .ant-menu-title-content::after,
body>#root>.ant-app .header .header-logo>.clickable::after,
body>#root>.ant-app .ant-btn::after,
body>#root>.ant-app .announcement .ant-card-extra>a::after,
body>#root>.ant-app .ant-tag::after,
body>#root>.ant-app .portal-user-info-status::after,
body>#root>.ant-app .portal-chall-header>*::after {
    content: "喵";
}
</style>
```

你好喵，我是粉色头发的少女喵，王牌发明家喵！

我擅长过滤文本中的一些关键词喵，附件里的程序是我最新的发明：**\*\*filtered\*\*** 喵！

把它交给了一个英国小女孩，看起来效果很不错喵！

这个程序可以进行正则匹配喵，就像你可以同时使用 `关.*?喵，.*?谢谢喵` 来匹配“关注⭕️⭕️⭕️⭕️喵，关注⭕️⭕️⭕️⭕️谢谢喵”和这道题目的标题“关键词过滤喵，谢谢喵”——当你理解了这一点，你就理解了正则喵！

为了过滤更复杂的东西，甚至是进行文本替换，你可以写一些像这样的规则喵：

```
  重复把【 】替换成【】喵
  如果看到【MaxXing】就跳转到【什么也不做】喵
  把【关注(.+?)喵】替换成【举办\1喵】喵

什么也不做：
  谢谢喵
```

把它输入给程序，程序就可以按照你的要求处理文本了喵，很方便喵！

现在你已经完全掌握了最先进的关键词过滤技术了喵（建议再仔细看看程序的实现喵），接下来请帮我完成一些工作喵！

谢谢喵！

> 注意喵，所有 flag 的输入里都不会出现 emoji 喵，可能在做文本替换的时候有用喵！
>
> 每个 flag 的具体评测规则见附件的 judge.py 喵！

### 字数统计喵

输入一个字符串，输出 10 进制的字符串长度喵，结果需要和 Python 中的 `len(...)` 保持一致喵！

### 排序喵

输入一个字符串，忽略其中的空行，并将剩余的行按照字数从小到大排序喵！

比如输入是：

```
aaa
b

cc
```

输出就是：

```
b
cc
aaa
```

### Brainfuck 喵

鉴于越来越多的谜语人把关键词藏在 brainfuck 代码里，所以请你帮我用替换规则写一个 brainfuck 解释器喵，把他们绳之以法喵！

输入一个合法的 brainfuck 程序，语法可参考[这个描述](https://esolangs.org/wiki/Brainfuck)，输出程序执行后的输出喵！

为了不让这个过程太折磨，我们做一些简化喵：

* Memory cell 中的内容一定是非负整数喵！
* 不需要处理输入操作（也就是 `,`）和其他扩展操作（`#`、`!` 之类）喵！
* 输出字符的 ASCII 一定介于 32（空格）和 122（`z`）之间（含端点）喵！

### 第二阶段提示：

* **\*\*filtered\*\*** <del>抄袭</del> 参考了 Slashalash 和 REGXY 两种 esolang 的设计，你或许可以上网搜索看看一些用它们编写的程序喵！搜不到的话可以试试 bing 喵！
* 就像[睡排序](https://www.rosettacode.org/wiki/Sorting_algorithms/Sleep_sort)一样，文本按字数排序也可以用类似的方法实现喵！比如每次把所有行都删掉一个字符，然后把最先删完的那行排在最前……之类的喵！
* 实现 Brainfuck 解释器可能需要一些耐心喵！注意 Brainfuck 程序中除 `>`、`<`、`+`、`-`、`.`、`[` 和 `]` 以外的字符都应该被忽略，以及你可能需要一些额外的状态来记录循环嵌套的层数喵！

**[【附件：下载过滤程序和评测程序喵！（prob04-src.zip）】](attachment/prob04-src.zip)**

**【终端交互：连接到题目喵！】**

## 预期解法

这可能是本届比赛算法（algorithm）题分类里最符合大家对算法题印象的算法题，但其实这道题本来是个 misc 喵……

而且，老实说其实这类编程题没什么预期解法喵（躺躺喵

以及，这道题看起来如此无聊的原因是，出题人 MaxXing 实在是没活了喵，只能在题目描述里喵两声这样，喵（

![patpat](assets/patpat.gif)

#### 不过好消息是，我们的 **\*\*filtered\*\*** 现已全面支持面向 writeup 的编程喵！

#### 只需要写好每道题的 writeup，然后~~释放忍术~~施展魔法喵！

#### 于是每个 flag 的 writeup 就可以用 [filtered.py](docker/filtered.py) 执行了喵，神奇喵！

![patpat](assets/blyat.gif)

### Flag 1：字数统计喵

看看 [counter.md](counter.md) 喵！

### Flag 2：排序喵

看看 [sort.md](sort.md) 喵！

### Flag 3：Brainfuck 喵

看看 [brainfuck.md](brainfuck.md) 喵！

### Docker 环境

适用于本题目的 Docker 环境见 [docker](docker) 目录喵！
