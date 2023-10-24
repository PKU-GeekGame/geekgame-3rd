import json
import os
import re
import requests

with open("emoji_list.txt", "r", -1, "utf8") as reader:
  x = "".join(reader.read().split("\n"))

cookies = None

for i in range(0, len(x), 64):
  sub = x[i:i+64]
  response = requests.get(f"https://prob14.geekgame.pku.edu.cn/level3?guess={sub}", cookies=cookies)
  if not cookies:
    cookies = response.cookies
  result = re.search(r"[🟥🟨🟩]+", response.text).group(0)
  assert len(result) == len(sub)
  with open(f"3/{i // 64}.txt", "w", -1, "utf8", None, "\n") as writer:
    writer.write(sub + "\n" + result)

STATUS_NOT_IN = 0
STATUS_IN = 1
STATUS_CORRECT_POS = 2

char_pos = {
  i: [] for i in range(64)
}
char_in = ""

for file_name in os.listdir("3"):
  if not file_name.endswith(".txt"):
    continue
  with open(f"3/{file_name}", "r", -1, "utf8") as reader:
    x, y = reader.read().strip().split("\n")
  
  for i, (char, status) in enumerate(zip(x, y)):
    if status != "🟥":
      char_in += char

for i in char_in:
  sub = i * 64
  response = requests.get(f"https://prob14.geekgame.pku.edu.cn/level3?guess={sub}", cookies=cookies)
  result = re.search(r"[🟥🟨🟩]+", response.text).group(0)
  assert len(result) == len(sub)
  with open(f"3/{ord(i)}.txt", "w", -1, "utf8", None, "\n") as writer:
    writer.write(sub + "\n" + result)

for file_name in os.listdir("3"):
  if not file_name.endswith(".txt"):
    continue
  with open(f"3/{file_name}", "r", -1, "utf8") as reader:
    x, y = reader.read().strip().split("\n")
  
  for i, (char, status) in enumerate(zip(x, y)):
    if status == "🟩":
      char_pos[i] = char

sub = "".join(char_pos.values())
assert len(sub) == 64
response = requests.get(f"https://prob14.geekgame.pku.edu.cn/level3?guess={sub}", cookies=cookies)
print(response.text)