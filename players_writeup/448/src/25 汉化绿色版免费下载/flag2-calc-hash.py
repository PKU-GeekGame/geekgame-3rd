def calc_hash(flag: str) -> int:
  hash = 1337
  for s in flag:
    hash = hash * 13337 + ("AEIO".index(s) + 1) * 11
  hash = hash * 13337 + 66
  hash = hash % 19260817
  return str(hash)

import multiprocess

if __name__ == "__main__":
  with multiprocess.Pool(16) as pool:
    with open("strings.txt", "r", -1, "utf8") as reader:
      result = pool.map(calc_hash, reader.read().split("\n"))
  
  with open("hash.txt", "w", -1, "utf8") as writer:
    writer.write("\n".join(result))