data = []
with open("zdata_ptf_inner.txt", "r") as fp:
    for line in fp:
        data += line.strip().split()

esc_mp = {}

with open("zdata.bin", "wb") as fp:
    i, n = 0, len(data)
    while i < n:
        c = data[i]
        if(c == '18'):
            i += 1
            c = hex(0x40 ^ int(data[i], 16))[2:]
            # fill 0 to 2 digits
            if len(c) < 2:
                c = '0' * (2 - len(c)) + c
            
            if c == '29':
                i += 1
                for _ in range(4):
                    if(data[i] == '18'): i += 1
                    i += 1
                continue
            
            # Count
            if c in esc_mp:
                esc_mp[c] += 1
            else:
                esc_mp[c] = 1
        fp.write(bytes.fromhex(c))
        i += 1

print(esc_mp)

# flag{traFf1c_aNa1y51s_4_ZMODEM}
