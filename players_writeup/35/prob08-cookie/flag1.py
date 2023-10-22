from randcrack import RandCrack
import binascii

raw = ""
rc = RandCrack()

with open("flag1.in", "r") as fp:
    raw = fp.read()
bins = binascii.unhexlify(raw)

# print(bins)
assert(len(bins) == 2529)
pure = bins[0:625*4]
enc = bins[625*4:]

for i in range(624):
    rc.submit(int.from_bytes(pure[i*4:i*4+4], "little"))

# check
std = int.from_bytes(pure[624*4:625*4], "little")
out = rc.predict_getrandbits(32)
print(std, out)

key = rc.predict_getrandbits(29*8)
ans = ""
for i in range(29):
    a, b = key % 256, enc[i]
    key //= 256
    ans += chr(a ^ b)
print(ans)

# for i in range(624):
#     rc.submit(int(raw[i*8:i*8+8], 16))

# print(rc.predict_getrandbits(32))
# print(int(raw[624*8:625*8], 16))
# # assert(rc.predict_getrandbits(32) == int(raw[624*8:625*8], 16))

# key = rc.predict_getrandbits(29*8)
# enc = int(raw[625*8:], 16)
# print(key)
# print(enc)
# ans = ""
# for i in range(29):
#     a, b = key % 256, enc % 256
#     key //= 256
#     enc //= 256
#     ans += chr(a ^ b)
# print(ans)
