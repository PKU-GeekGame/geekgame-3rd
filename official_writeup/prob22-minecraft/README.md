# [Misc] 麦恩·库拉夫特

- 命题人：Mivik
- 探索的时光：100 分
- 结束了？：150 分
- 为什么会变成这样呢？：300 分

## 题目描述

<blockquote>
<p>你这辈子就是被 Minecraft 给害了，没法跟正经妹子处事，跟妹子吃饭的时候，总是在想，她要是能帮我造个树厂就好了，无人值守多树种一小时一万多原木，送她回家的时候，总是在想，她要是用矢量珍珠炮送我回家就好了。坐在她的家里的沙发上的时候，她说进房间换个衣服，你的心怦怦跳，她要是出来的时候给你展示她的全物品分类器怎么办？她要是靠过来时要拉你去打机械动力怎么办？然后妹子穿着睡衣出来了，问你做不做一些两个人才能做的事情，你反手新建一张格雷科技和神秘时代六的图让她来开荒，她沉默了一会说我说的不是游戏</p>
</blockquote>
<p>作为掌握至尊出题人之力的小 M 把 Flag 藏在了一张 Minecraft 地图里。不过他显然不想让你轻松拿到它。</p>
<p><strong>补充说明：</strong></p>
<ul>
<li>可以使用自己的 Minecraft 客户端或者使用开源客户端来游玩。请参考 <a target="_blank" rel="noopener noreferrer" href="https://mivik.moe/ctf-minecraft/">这里的说明</a>。</li>
<li>附件所给存档的 Minecraft 版本是 1.18.2。如果你的客户端版本不同，可能会出现问题。</li>
</ul>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>手玩找不到的东西，或许可以让程序帮忙？</li>
<li>Flag 2: 可以看看 <a target="_blank" rel="noopener noreferrer" href="https://minecraft.fandom.com/zh/wiki/Anvil%E6%96%87%E4%BB%B6%E6%A0%BC%E5%BC%8F">Minecraft 的存档格式</a>。</li>
<li>Flag 3: 可以看看 <a target="_blank" rel="noopener noreferrer" href="https://minecraft.fandom.com/zh/wiki/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF?variant=zh#%E7%BA%A2%E7%9F%B3%E6%A8%A1%E6%8B%9F%E7%94%B5%E8%B7%AF">红石模电</a>。</li>
</ul>
</div>

**[【附件：下载题目附件（prob22.zip）】](attachment/prob22.zip)**

## 预期解法

### Flag1

简单手玩，跟火把找路即可

### Flag2

用 `anvil-parser` 或者 `nbtlib` 来解析地图，找到钻石块的位置，其中一个就有 Flag2。

### Flag3

根据 Flag2 找到的钻石块位置可以找到红石磁带的所在地。观察一下红石磁带的结构，实质上是一个巨大的比较器环。比较器能够记录 `0-15` 的红石强度，即一个红石比较器存储 4bit 的信息。手写存档解析将比较器路径捋出来，然后得到数据流，注意到为了防止数据损毁、相邻两个比较器存的信号是一样的。去重后，得到一串二进制，观察到其中有 `IEND`、`PNG` 等关键字，将 PNG 头作为开头写入文件即可得到 flag 图片。

做法二：在输出口接命令方块，将信号强度输出到日志中，然后读取日志提取数据。

实际上做法二应当简单些，但出题人毕竟还需要生成存档，所以写的是做法一的代码。在这里放一下：

```python

import os
from struct import unpack
import zlib
import io

from nbtlib import File, schema

import tempfile


class Chunk:
    def __init__(self, location, size):
        self.location = location
        self.size = size


def read_chunks(f):
    chunks = [Chunk(int.from_bytes(f.read(3), 'big') * 4096,
                    f.read(1)[0] * 4096) for _ in range(1024)]
    f.read(4096)

    for i in range(1024):
        if chunks[i].size == 0:
            chunks[i] = None

    for chunk in chunks:
        if not chunk:
            continue

        f.seek(chunk.location)
        length = unpack('>I', f.read(4))[0]

        compression = f.read(1)[0]
        assert compression == 2

        data = f.read(length)
        inflate = zlib.decompressobj()
        data = inflate.decompress(data)
        data += inflate.flush()

        chunk.nbt = File.parse(io.BytesIO(data))

    chunk_x_base = 32
    chunk_z_base = -32

    def chunk_index(x, z):
        return (x // 16) - chunk_x_base + ((z // 16) - chunk_z_base) * 32

    def get_section(x, y, z):
        chunk = chunks[chunk_index(x, z)]
        if not chunk:
            return None

        for section in chunk.nbt['sections']:
            if section['Y'] == y // 16:
                return section

        return None

    def get_block(x, y, z):
        section = get_section(x, y, z)
        if not section:
            return None

        block_states = section['block_states']
        palette = block_states['palette']
        if len(palette) == 1:
            return palette[0]

        idx = 256 * (y % 16) + 16 * (z % 16) + (x % 16)
        length = max(4, (len(palette) - 1).bit_length())
        capability = 64 // length
        what = (block_states['data'][idx // capability] >>
                (length * (idx % capability))) & ((1 << length) - 1)
        return block_states['palette'][what]

    entities = {}
    for chunk in chunks:
        if not chunk:
            continue
        for entity in chunk.nbt['block_entities']:
            if entity['id'] == 'minecraft:comparator':
                entities[(entity['x'], entity['y'], entity['z'])] = entity

    dirs = {
        'east': (-1, 0),
        'south': (0, -1),
        'west': (1, 0),
        'north': (0, 1),
    }

    cmps = []

    x, y, z = 607, 1, -97
    while True:
        block = get_block(x, y, z)
        assert block['Name'] == 'minecraft:comparator'
        cmps.append([entities[(x, y, z)], [], 0])

        facing = block['Properties']['facing']
        dx, dz = dirs[facing]
        x += dx
        z += dz
        to = get_block(x, y, z)
        if to['Name'] == 'minecraft:comparator':
            cmps[-1][2] = -1
            continue

        candidates = []

        def search_block(x, y, z):
            blk = get_block(x, y, z)
            assert blk['Name'].endswith(
                'concrete') or blk['Name'] == 'minecraft:redstone_wire'
            if blk['Name'] == 'minecraft:redstone_wire':
                cmps[-1][1].append((x, y, z))

            for fac in dirs:
                dx, dz = dirs[fac]
                if get_block(x + dx, y, z + dz)['Name'] == 'minecraft:comparator' and get_block(x + dx, y, z + dz)['Properties']['facing'] == fac:
                    if (x + dx, y, z + dz) != (608, 102, -98):
                        candidates.append((x + dx, y, z + dz))

        search_block(x, y, z)
        for dy in (-1, 1):
            if get_block(x, y + dy, z)['Name'] == 'minecraft:redstone_wire':
                search_block(x, y + dy, z)
                for dx, dz in dirs.values():
                    if get_block(x + dx, y + dy, z + dz)['Name'].endswith('concrete'):
                        search_block(x + dx, y + dy, z + dz)
                if get_block(x, y + dy - 1, z)['Name'].endswith('concrete'):
                    search_block(x, y + dy - 1, z)

        if len(candidates) == 0:
            break

        candidates = list(set(candidates))

        if len(candidates) != 1:
            print('expected 1 candidate', x, y, z, candidates)
            quit()

        x, y, z = candidates[0]

    # 收集信号
    signals = list(map(lambda x: int(x[0]['OutputSignal']), cmps))[::-1]
    for i in range(0, len(signals), 2):
        if signals[i] != signals[i + 1]:
            print('swap', i, signals[i], signals[i + 1])
            signals = signals[1:] + [signals[0]]
            break

    hx = ''
    for i in range(0, len(signals), 2):
        assert signals[i] == signals[i + 1]
        hx += '0123456789abcdef'[signals[i]]

    data = bytes.fromhex(hx)

    if data.find(b'\x89PNG') == -1:
        data = bytes.fromhex(hx[1:] + hx[0])

    index = data.index(b'\x89PNG')
    data = data[index:] + data[:index]

    open('output.bin', 'wb').write(data)


path = './wherestheflag/region/'
for file in os.listdir(path):
    if file == 'r.1.-1.mca':
        read_chunks(open(os.path.join(path, file), 'rb+'))

```
