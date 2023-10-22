import zlib
def crc32_combine(crc1, crc2, len2):
    """Explanation algorithm: https://stackoverflow.com/a/23126768/654160
    crc32(crc32(0, seq1, len1), seq2, len2) == crc32_combine(
        crc32(0, seq1, len1), crc32(0, seq2, len2), len2)"""
    # degenerate case (also disallow negative lengths)
    if len2 <= 0:
        return crc1
    # put operator for one zero bit in odd
    # CRC-32 polynomial, 1, 2, 4, 8, ..., 1073741824
    odd = [0xedb88320] + [1 << i for i in range(0, 31)]
    even = [0] * 32
    def matrix_times(matrix, vector):
        number_sum = 0
        matrix_index = 0
        while vector != 0:
            if vector & 1:
                number_sum ^= matrix[matrix_index]
            vector = vector >> 1 & 0x7FFFFFFF
            matrix_index += 1
        return number_sum
    # put operator for two zero bits in even - gf2_matrix_square(even, odd)
    even[:] = [matrix_times(odd, odd[n]) for n in range(0, 32)]
    # put operator for four zero bits in odd
    odd[:] = [matrix_times(even, even[n]) for n in range(0, 32)]
    # apply len2 zeros to crc1 (first square will put the operator for one
    # zero byte, eight zero bits, in even)
    while len2 != 0:
        # apply zeros operator for this bit of len2
        even[:] = [matrix_times(odd, odd[n]) for n in range(0, 32)]
        if len2 & 1:
            crc1 = matrix_times(even, crc1)
        len2 >>= 1
        # if no more bits set, then done
        if len2 == 0:
            break
        # another iteration of the loop with odd and even swapped
        odd[:] = [matrix_times(even, even[n]) for n in range(0, 32)]
        if len2 & 1:
            crc1 = matrix_times(odd, crc1)
        len2 >>= 1
        # if no more bits set, then done
    # return combined crc
    crc1 ^= crc2
    return crc1

def combine(s1,s2,*s3):
    if len(s3)>0:
        return combine(combine(s1,s2),*s3)
    return (s1[0]+s2[0],crc32_combine(s1[1],s2[1],s2[0]))

def dup(s1,n):
    res=(0,0)
    s=s1
    while n>0:
        if n%2!=0:
            res=combine(res,s)
        s=combine(s,s)
        n//=2
    return res

def lenhash(i):
    return (len(i),zlib.crc32(i)) 

def footer(i):
    return i[1].to_bytes(4,"little")+(i[0]%(2**32)).to_bytes(4,"little")

def gen(ii=1,jj=1):
    l1=21133561+16907256*(32766*ii+510)
    l2=16907256+16907256*(32766*jj+766)
    z=zlib.compressobj(9,wbits=31)
    x1=z.compress(b'\x00'*21133561)
    x2=z.compress(b'\x00'*16907256)
    x3=z.compress(flag)
    x4=z.compress(b'\x00'*16907256)
    x5=z.compress(b'\x00'*16907256)
    x6=z.flush()
    z2=zlib.compressobj(9,wbits=31)
    y1=z2.compress(x1+x2*510)
    y2=z2.compress(x2*32766)
    y3=z2.compress(x3+x4+x5*766)
    y4=z2.compress(x5*32766)
    tt=x6[:-8]+footer(combine(dup(lenhash(b'\x00'),l1),lenhash(flag),dup(lenhash(b'\x00'),l2)))
    y5=z2.compress(tt)
    y6=z2.flush()[:-8]
    y7=footer(combine(lenhash(x1),dup(lenhash(x2),32766*ii+510),lenhash(x3+x4),dup(lenhash(x5),32766*jj+766),lenhash(tt)))
    print(combine(lenhash(x1),dup(lenhash(x2),32766*ii+510),lenhash(x3+x4),dup(lenhash(x5),32766*jj+766),lenhash(tt)))
    z3=zlib.compressobj(9,wbits=31)
    p=[]
    p.append(z3.compress(y1))
    for i in range(ii//1000):
        print(i)
        p.append(z3.compress(y2*1000))
    p.append(z3.compress(y2*(ii%1000)))
    p.append(z3.compress(y3))
    for i in range(jj//1000):
        print(i)
        p.append(z3.compress(y4*1000))
    p.append(z3.compress(y4*(jj%1000)))
    p.append(z3.compress(y5+y6+y7))
    p.append(z3.flush())
    return b''.join(p)