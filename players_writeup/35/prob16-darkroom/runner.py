from pwn import *
import time

token = "35:MEYCIQDZ6pH1fSHQ81kNNCM6rlOVZsHOb5FQMIxhMMkXas39AgIhAPtTxQV6tZouRgMN0DetNZKZSokV5K07HRkZDJdW6hbH"
url = "prob16.geekgame.pku.edu.cn"
port = 10016

fp = open("log.txt", "w")

def Trial():
    conn = remote(url, port)
    time.sleep(0.2)
    conn.send(token+"\n")
    time.sleep(2.0)

    def newgame():
        conn.send("newgame\n")
        time.sleep(0.3)
        conn.send("aaaaaaaaaaaa\n")
        time.sleep(0.3)
        conn.send("y\n")
        time.sleep(0.3)

    def walk(d):
        conn.send(d + "\n")
        time.sleep(0.3)
    def N():
        walk("n")
    def S():
        walk("s")
    def W():
        walk("w")
    def E():
        walk("e")
    
    def use(i):
        conn.send("use " + i + "\n")
        time.sleep(0.3)

    def usewith(i, t):
        conn.send("usewith " + i + " " + t + "\n")
        time.sleep(0.3)
    
    def pickup(i):
        conn.send("pickup " + i + "\n")
        time.sleep(0.3)
    
    def h():
        conn.send("h\n")
        time.sleep(0.3)

    def getflag():
        conn.send("getflag\n")
        time.sleep(3)
    
    newgame()
    N()
    N()
    W()
    W()
    S()
    getflag()

    _ = conn.recvrepeat(timeout=2)
    
    now = []

    while True:
        conn.send("1\n")
        _ = conn.recvrepeat(timeout=0.5)
        print(_)
        u = 1 if len(_) == 0 else 0
        print("[]u = ", u)
        print("u=", u, file=fp)
        fp.flush()
        now.append(u)
        _ = conn.recvrepeat(timeout=3)
        print(_)

Trial()

