def int2aeio(number: int, length: int = 16):
  s = ""
  while number > 0 or length > 0:
    number, digit = divmod(number, 4)
    s = "AEIO"[digit] + s
    length -= 1
  return s

writer = open("strings.txt", "w", -1, "utf8", None, "\n")

for i in range(0, 4 ** 16):
  s = int2aeio(i)
  if s.count("A") == 6 and s.count("E") == 3 and s.count("I") == 1 and s.count("O") == 6:
    writer.write(s + "\n")
    writer.flush()