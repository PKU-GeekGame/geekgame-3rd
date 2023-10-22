from pwn import *

'''
>	Move the pointer to the right
<	Move the pointer to the left
+	Increment the memory cell at the pointer
-	Decrement the memory cell at the pointer
.	Output the character signified by the cell at the pointer
,	Input a character and store it in the cell at the pointer
[	Jump past the matching ] if the cell at the pointer is 0
]	Jump back to the matching [ if the cell at the pointer is nonzero
'''

test = [
    '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.',
    # '++++++++[>++++++++<-]>++++++++.>++++++++[>++++++++++++<-]>+++++.+++++++..+++.>++++++++[>+++++<-]>++++.------------.<<<<+++++++++++++++.>>.+++.------.--------.>>+.',
#     '''>+++++>+++>+++>+++++>+++>+++>+++++>++++++>+>++>+++>++++>++++>+++>+++>+++++>+>+
# >++++>+++++++>+>+++++>+>+>+++++>++++++>+++>+++>++>+>+>++++>++++++>++++>++++>+++
# >+++++>+++>+++>++++>++>+>+>+>+>++>++>++>+>+>++>+>+>++++++>++++++>+>+>++++++
# >++++++>+>+>+>+++++>++++++>+>+++++>+++>+++>++++>++>+>+>++>+>+>++>++>+>+>++>++>+
# >+>+>+>++>+>+>+>++++>++>++>+>+++++>++++++>+++>+++>+++>+++>+++>+++>++>+>+>+>+>++
# >+>+>++++>+++>+++>+++>+++++>+>+++++>++++++>+>+>+>++>+++>+++>+++++++>+++>++++>+
# >++>+>+++++++>++++++>+>+++++>++++++>+++>+++>++>++>++>++>++>++>+>++>++>++>++>++
# >++>++>++>++>+>++++>++>++>++>++>++>++>++>+++++>++++++>++++>+++>+++++>++++++>++++
# >+++>+++>++++>+>+>+>+>+++++>+++>+++++>++++++>+++>+++>+++>++>+>+>+>++++>++++
# [[>>>+<<<-]<]>>>>[<<[-]<[-]+++++++[>+++++++++>++++++<<-]>-.>+>[<.<<+>>>-]>]
# <<<[>>+>>>>+<<<<<<-]>++[>>>+>>>>++>>++>>+>>+[<<]>-]>>>-->>-->>+>>+++>>>>+[<<]
# <[[-[>>+<<-]>>]>.[>>]<<[[<+>-]<<]<<]
# ''',
#     '''++++++++[>+++++++++<-]>.<+++++[>++++++<-]>-.+++++++..+++.< 
# ++++++++[>>++++<<-]>>.<<++++[>------<-]>.<++++[>++++++<-]> 
# .+++.------.--------.>+.
#     ''',
#     '>+++++++[<+++++++>-]<.+.+.+.+.-.-.-.-.'

]

# 码：N separate codes, P is the location PC(RIP)
# 出：output buffer
# 括：stack to parse [] jump
init_pc = '''
重复把【[^+-.\\[\\]<>]】替换成【】喵
重复把【([^NP])([^NP])】替换成【\\1N\\2】喵
把【^】替换成【括出码P】喵
'''
# ~ mark the active memory, num of 0 mark the number
init_mem = '把【$】替换成【N内~{0}】喵\n'.format('='*10)

reg_escape = '\\'
re_out_escape = lambda c: "\\"+c if c in reg_escape else c

parse_ascii = '\n'.join([f'把【分{"圆"*c}出】替换成【出{re_out_escape(chr(c)) if c >= 0x20 else ";"}】喵' for c in range(123, 31, -1)])

miao = init_pc + init_mem + '''
interpret：
如果看到【P[+]】就跳转到【plus】喵
如果看到【P[-]】就跳转到【minus】喵
如果看到【P[\\[]】就跳转到【rj】喵
如果看到【P[\\]]】就跳转到【lj】喵
如果看到【P[\\.]】就跳转到【out】喵
如果看到【P[<]】就跳转到【left】喵
如果看到【P[>]】就跳转到【right】喵

# trap
如果看到【^】就跳转到【end】喵

plus：
    把【~】替换成【~0】喵
    如果看到【^】就跳转到【nextpc】喵
minus：
    把【~0】替换成【~】喵
    如果看到【^】就跳转到【nextpc】喵
right：
    把【~([^=~]+)$】替换成【~\\1=】喵
    把【~$】替换成【~=】喵
    riszero：
        如果看到【~[^=]】就跳转到【risnonzero】喵
        把【~=】替换成【=~】喵
        如果看到【^】就跳转到【rzeroend】喵
    risnonzero：
        把【~([^=]+)=】替换成【=\\1~】喵
    rzeroend：
        如果看到【^】就跳转到【nextpc】喵
left：
    liszero：
        如果看到【[^=]~】就跳转到【lisnonzero】喵
        把【=~】替换成【~=】喵
        如果看到【^】就跳转到【lzeroend】喵
    lisnonzero：
        把【=([^=]+)~】替换成【~\\1=】喵
    lzeroend：
        如果看到【^】就跳转到【nextpc】喵
rj：
    如果看到【~0】就跳转到【nextpc】喵
    把【括】替换成【1括】喵
    rloopjump：
        把【P(.)N】替换成【N\\1P】喵
        rpush：
            如果没看到【P\\[】就跳转到【rpop】喵
            把【括】替换成【1括】喵
            如果看到【^】就跳转到【rloopend】喵
        rpop：
            如果没看到【P\\]】就跳转到【rloopend】喵
            把【1括】替换成【括】喵
        rloopend：
            如果看到【1括】就跳转到【rloopjump】喵
            如果看到【^】就跳转到【nextpc】喵

lj：
    如果没看到【~0】就跳转到【nextpc】喵
    把【括】替换成【1括】喵
    lloopjump：
        把【N(.)P】替换成【P\\1N】喵
        lpush：
            如果没看到【P\\]】就跳转到【lpop】喵
            把【括】替换成【1括】喵
            如果看到【^】就跳转到【lloopend】喵
        lpop：
            如果没看到【P\\[】就跳转到【lloopend】喵
            把【1括】替换成【括】喵
        lloopend：
            如果看到【1括】就跳转到【lloopjump】喵
            如果看到【^】就跳转到【nextpc】喵


out：
    把【出([^~]+)~([^=]+)=】替换成【分\\2出\\1~\\2=】喵
    如果看到【^】就跳转到【nextpc】喵



nextpc：
    把【P(.)N】替换成【N\\1P】喵
    如果看到【P内】就跳转到【print】喵

如果看到【^】就跳转到【interpret】喵

print：
    # 如果看到【^】就跳转到【】喵
    把【码.+$】替换成【】喵
    把【括】替换成【】喵
    把【0】替换成【圆】喵

    parse_ascii：
'''+ \
parse_ascii \
+'''
如果看到【分】就跳转到【parse_ascii】喵
把【出】替换成【】喵

end：
谢谢喵
'''

with open('filtered/miao_rule','w') as fp:
    fp.write(miao)
print(miao)
print('=============')

for t in test:
    with open('filtered/miao_text','w') as fp:
        fp.write(t)
    print('testcase', t.__repr__())
    print('=====')
    res = os.popen('/bin/python3 filtered/filtered.py filtered/miao_rule filtered/miao_text').read()
    print(res.__repr__())

print('total size', len(miao))

# context.log_level = 'debug'
conn = remote('prob04.geekgame.pku.edu.cn',10004)
conn.sendlineafter(b'Please input your token: ', b'')
conn.sendlineafter('1-3'.encode(), b'3')
conn.sendlineafter('64KB'.encode(), miao.encode())
conn.interactive()