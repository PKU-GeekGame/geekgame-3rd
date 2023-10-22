from pwn import *
import time

token = "35:MEYCIQDZ6pH1fSHQ81kNNCM6rlOVZsHOb5FQMIxhMMkXas39AgIhAPtTxQV6tZouRgMN0DetNZKZSokV5K07HRkZDJdW6hbH"
url = "prob08.geekgame.pku.edu.cn"
port = 10008

conn = remote(url, port)
time.sleep(0.2)
conn.send(token+"\n")
time.sleep(1.0)
conn.send("3\n")
time.sleep(2.0)
# read until <...> appears, do not use recvall() here
data = conn.recvuntil(">").decode()
# get the string inside <...>
data = data[data.find("<")+1:data.find(">")].split(',')
conv = [s[2:] for s in data]
ans = ",".join(conv)
# send
conn.send(ans+"\n")
time.sleep(1.0)
# read all the data
data = conn.recvall().decode()
print(data)