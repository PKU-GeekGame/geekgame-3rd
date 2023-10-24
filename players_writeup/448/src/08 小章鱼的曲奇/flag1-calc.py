def xor_arrays(a, b, *args):
  if args:
    return xor_arrays(a, xor_arrays(b, *args))
  return bytes([x ^ y for x, y in zip(a, b)])

with open("input1.txt", "r", -1, "utf8") as reader:
  input1 = bytes.fromhex(reader.read().strip())

with open("input2.txt", "r", -1, "utf8") as reader:
  input2 = bytes.fromhex(reader.read().strip())

print(xor_arrays(input1, input2).strip(b'\0'))