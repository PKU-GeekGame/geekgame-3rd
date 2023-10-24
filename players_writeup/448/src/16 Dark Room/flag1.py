from pwn import *

COMMANDS = [
  "n",
  "n",
  "e",
  "pickup key",
  "w",
  "s",
  "s",
  "e",
  "e",
  "e",
  "pickup trinket",
  "use trinket",
  "w",
  "s",
  "usewith key door",
  "s",
  "s",
  "n",
  "w",
  "w",
  "w",
  "n",
  "pickup key",
  "s",
  "e",
  "e",
  "e",
  "n",
  "n",
  "n",
  "w",
  "w",
  "n",
  "n",
  "w",
  "w",
  "usewith key door",
  "h",
]

def play(file_name):
  writer = open(file_name, "w", -1, "utf8")
  conn = remote('prob16.geekgame.pku.edu.cn', 10016)
  conn.recvuntil(b"Please input your token: ")
  conn.send(b"MY TOKEN\n")
  time.sleep(1)
  conn.recvuntil(b"]: ", timeout=5)
  conn.send(b"newgame\n")
  conn.recvuntil(b"]: ", timeout=5)
  conn.send(b"gamer\n")
  conn.recvuntil(b"(y/n) ", timeout=5)
  conn.send(b"y\n")
  for command in COMMANDS:
    writer.write(conn.recvuntil(b"]: ", timeout=5).decode("utf8") + "\n")
    conn.send(command.encode("utf8") + b"\n")

  while True:
    result = conn.recvuntil(b"]: ", timeout=5).decode("utf8")
    writer.write(result + "\n")
    sanity = int(re.search(r"Sanity: \[[\|\-]+\] \((-?\d+)%\)", result).group(1))
    if sanity >= 118:
      conn.send(b"n\n")
      result = conn.recvuntil(b"]: ", timeout=5).decode("utf8")
      writer.write(result + "\n")
      writer.close()
      exit(0)
    elif sanity < 1:
      conn.close()
      break
    else:
      conn.send(b"h\n")
  writer.close()
  
i = 0
while True:
  play(f"output/{i}.txt")
  i += 1
  time.sleep(3.5)