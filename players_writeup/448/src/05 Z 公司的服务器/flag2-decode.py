import struct

result = b""

data = b""
for f in [1, 2, 3, 4, 5, 6, 7, 8]:
  with open(f"flag2/{f:04d}.bin", "rb") as reader:
    data += reader.read()

data = data[data.index(b"\xFF\xD8\xFF\xE0"):]

i = 0
while i < len(data):
  c = data[i]
  if c == 0x18:
    if i + 1 >= len(data):
      break
    c = data[i + 1]
    c = c ^ 0x40
    result += struct.pack("B", c)
    i += 2
    continue
  else:
    result += struct.pack("B", c)
    i += 1
    continue

with open("out.jpg", "wb") as writer:
  writer.write(result[result.index(b"\xFF\xD8\xFF\xE0"):])