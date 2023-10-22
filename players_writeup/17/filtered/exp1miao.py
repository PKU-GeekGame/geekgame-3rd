from pwn import *
# 重复把【】替换成【】喵
# 如果看到【】就跳转到【】喵
# 把【】替换成【】喵

miao1 = """
重复把【([^🏓])】替换成【🏓】喵
把【^】替换成【E】喵

loop：
    重复把【🚝】替换成【🏓】喵
    重复把【([🏓]{10})】替换成【🚝】喵

    把【$】替换成【🏓】喵
    push：
        把【^】替换成【🏓】喵
        把【(🏓)$】替换成【】喵
    如果看到【🏓$】就跳转到【push】喵
"""\
+'\n'.join(['把【^(🏓{%d})】替换成【%d】喵'%(n+1, n) for n in range(9,-1,-1)])\
+ """
如果看到【🚝】就跳转到【loop】喵

end：
把【E】替换成【】喵
谢谢喵
"""
test1 = [
    'A'* 102,
    'A'* 342,
    'A'*3,
    'A'*0,
]


miao2 = """
重复把【(\\r\\n)】替换成【\\n】喵
重复把【(\\n\\n)】替换成【\\n】喵
如果没看到【[^\\n]】就跳转到【end】喵
把【\\n$】替换成【】喵
把【^\\n】替换成【】喵
重复把【\\n】替换成【🏓🏓】喵
把【([^🏓🚝]+)🏓🏓】替换成【\\1🏓\\1💜】喵
把【^】替换成【🏊】喵
把【💜([^💜]+)$】替换成【💜\\1🏓\\1💜】喵



dec：
    把【🏓([^🏓💜]+?)💜$】替换成【🚝\\1🆙】喵
    decloop：
        把【🚝.】替换成【🚝】喵
        如果没看到【💜.+?🚝】就跳转到【enddec】喵
        把【🆙】替换成【💜】喵
        把【💜([^💜]+?)🚝】替换成【🆙\\1🏓】喵
        把【🏓([^🏓]+?)🆙】替换成【🚝\\1🆙】喵
        如果看到【^】就跳转到【decloop】喵
enddec：
    把【🚝】替换成【🏓】喵
    把【🆙】替换成【💜】喵

如果没看到【🏓💜】就跳转到【dec】喵

把【🏊】替换成【🏊💜】喵
重复把【🏊([^🏊]*?)💜([^🏊💜]+?)🏓💜】替换成【\\2\\n🏊\\1💜】喵
把【🏊💜】替换成【🏊】喵


如果没看到【🏊$】就跳转到【dec】喵
把【🏊】替换成【】喵
重复把【\\n$】替换成【】喵
重复把【^\\n】替换成【】喵

end：
谢谢喵
"""
test2 = [
    '\n'.join(['中国','','$$$','','$$$','as',',,,fff','ss','kkkkk']),
    '\n'.join(['A'*randint(0, 100) for i in range(randint(50,100))]),
    ''
]



miao = miao2
test=test2

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
    print(res)


# flag{caN_c4n_NEEd_SHoW_sh0W_WaY}