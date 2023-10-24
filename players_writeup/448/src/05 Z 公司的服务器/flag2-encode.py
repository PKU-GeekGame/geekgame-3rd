from pwn import *

context.log_level = "debug"
io = process(["sz", "test.jpg"])
time.sleep(1)
io.send(b"\x2a\x2a\x18\x42\x30\x31\x30\x30\x30\x30\x30\x30\x36\x33\x66\x36\x39\x34\x0a\x0a")
time.sleep(1)
io.recv()
io.send(b"\x2a\x2a\x18\x42\x30\x39\x30\x30\x30\x30\x30\x30\x30\x30\x61\x38\x37\x63\x0a\x0a")
time.sleep(1)

out = 1
while True:
  x = io.recv(timeout=5)
  if not x:
    break
  with open(f"test/{out:04d}.bin", "wb") as writer:
    writer.write(x)
  out += 1
io.close()