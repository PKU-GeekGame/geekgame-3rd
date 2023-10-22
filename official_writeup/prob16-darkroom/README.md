# [Misc] Dark Room

- 命题人：DuanYuFi
- Flag 1：150 分
- Flag 2：250 分

## 题目描述

<p>这是一个文本游戏，在游戏中你将要寻找钥匙、获取宝物、寻求帮助，最后逃脱小黑屋通关。</p>
<p>地图中存在两个 Flag，你需要根据游戏提示、甚至寻找能够破坏或利用的游戏规则，来找到他们。祝好运！</p>
<p><strong>补充说明：</strong></p>
<ul>
<li>题目源码在 <a target="_blank" rel="noopener noreferrer" href="https://github.com/tinichu316/Dark_Room">tinichu316/Dark_Room</a> 的基础上经过了一点修改。</li>
<li>本题的连接频率限制是 3 秒一次。</li>
<li>为了避免不同用户之间存档混乱，每次连接时均会启动一个新的实例，即不能读取上次连接的存档。</li>
</ul>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>Flag 1：<code>help</code> 真的有用。</li>
<li>Flag 2：程序报错时会泄露一些源代码。</li>
</ul>
</div>

**【终端交互：连接到题目】**

## 预期解法

地图如下所示：

```text
# Front_Door   #             #           #          #              #         #
# Locked_Door2 # Hallway     # Hallway   # Bad_Room #              #         #
# FlagRoom     #             # Hallway   #          #              #         #
#              #             # Dark_Room # Hallway  # Hallway      # Lootway #
#              # Good_Choice #           #          # Locked_Door1 #         #
#              # Choice_Room # Hallway   # Hallway  # Hallway      #         #
#              # Bad_Choice  #           #          # Loot_Dirty   #         #
```

首先，根据游戏源代码可知最优解在结束的时候只有 90 分，但需要 117 分才能过关。
然后，根据 help 指令的介绍，可以有概率增加 san 值，每次有 20% 概率增加 10。
根据过关要求，只要成功连续增加三次 san 值，就达到了足够获取 flag1 的条件，因此不断重新连接，直到 san 值达到要求即可。

其次，达到 flag 房间之后，会要求输入一个整数来猜测一个大数，这是根本不可能实现的。
不过，如果这里输入一个非数字字符串，会触发一个 ValueError，程序会泄漏一部分的源码，通过阅读源码可以让选手猜测出这里存在侧信道的风险，进而通过侧信道来获取 flag2。
