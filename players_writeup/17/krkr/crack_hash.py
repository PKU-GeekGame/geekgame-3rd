from Crypto.Util.number import *
from itertools import product
import numpy as np
import numba

# import pyximport; pyximport.install()
# import crack

N = 19260817
m = 13337
choice = [11,22,33,44,55,66]
# note we can derive 13337 ** k === n mod 19260817

init = 1337 # 9*191

@numba.jit(nopython=True)
def get_hash(l):
    h = 0
    for i in l:
        h = (h * m + i + 1) % N
    return h

def get_hash_orig(l):
    h = init
    for i in l:
        h = (h * m + choice[i]) % N
    return h

# print(get_hash([0]))
# 先过一遍，找出开始第二遍后prev_hash对应内存（dword） 7748521

C = 7748521

minv = inverse(m, N)
eleven_inv = inverse(11, N)
C_no_end = ((C - 66) * minv) % N
C_no_end_no_init_norm = ((C_no_end - 1337 * pow(m,10+11,N))*eleven_inv) % N
print(C_no_end_no_init_norm)
print(1337 % 11, m%11, C_no_end)

# 1337 correspond to m ** 11

@numba.jit(nopython=True)
def iter_hash(dim = 21):
    # from itertools import product
    # iter_pools = 
    START_NUM, END_NUM = 0, 4
    cur_set = np.ones((dim,), dtype=np.int32) * START_NUM
    cur_index = 0
    
    while True:
        # run set
        h = get_hash(cur_set)
        if h == C_no_end_no_init_norm:
            # print(cur_set, get_hash_orig([*cur_set, 5]))
            # print('flag{', end='')
            outstr = ''
            for c in cur_set:
                outstr += 'AEIOU'[c - START_NUM]
            print('out', outstr)
        
        # iterate to next
        while cur_set[cur_index] == END_NUM:
            cur_set[0:cur_index+1] = START_NUM
            cur_index += 1
            if cur_index == dim:
                # finish
                return
        cur_set[cur_index] += 1
        cur_index = 0
        # print(cur_set)

    # flag2: flag{OEIUIOAAAU}, no
    print(''.join(['AEIOU'[i] for i in hash_num]))

iter_hash()



# for hash_num in product(*[range(5) for i in range(10)]):
#     h = get_hash([*hash_num])
#     if h == C_no_end_no_init_norm:
#         print(hash_num, get_hash_orig([*hash_num, 5]))
#         print(''.join(['AEIOU'[i] for i in hash_num]))
#         continue