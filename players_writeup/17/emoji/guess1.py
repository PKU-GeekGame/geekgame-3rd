# 141 in total
import requests
from bs4 import BeautifulSoup
import time
import os

if os.path.isfile('emoji_guess/emoji_dump.txt'):
    with open('emoji_guess/emoji_dump.txt', 'r') as fp:
        EMOJI_CHARS = fp.read().split('\n')

else:
    # http://unicode.org/Public/emoji/3.0/emoji-data.txt
    with open('emoji_guess/emoji-data.txt','r') as fp:
        emoji_db = fp.read().split('\n')

    EMOJI_CHARS = set()
    for line in emoji_db:
        if not line.startswith('#') and line.strip() != '':
            emo_range = line.split(' ')[0]
            if '..' in emo_range:
                st, ed = [eval('0x'+c.lower()) for c in emo_range.split('..')]
                EMOJI_CHARS |= {chr(c) for c in range(st, ed+1)}
            else:
                EMOJI_CHARS |= {chr(eval('0x'+emo_range.lower()))}
    print(EMOJI_CHARS, len(EMOJI_CHARS))

    EMOJI_CHARS = list(EMOJI_CHARS)

    with open('emoji_guess/emoji_dump.txt', 'w') as fp:
        fp.write('\n'.join(EMOJI_CHARS))

print(EMOJI_CHARS,len(EMOJI_CHARS))

# EMOJI_CHARS = list((
#     {chr(0x200d)}  # zwj
#     | {chr(0x200b)}  # zwsp, to break emoji componenets into independent chars
#     | {chr(0x20e3)} # keycap
#     | {chr(c) for c in range(0xfe00, 0xfe0f+1)} # variation selector
#     | {chr(c) for c in range(0xe0020, 0xe007f+1)} # tag
#     | {chr(c) for c in range(0x1f1e6, 0x1f1ff+1)} # regional indicator
# ))

URL1 = 'https://prob14.geekgame.pku.edu.cn/level1?guess='
URL3 = 'https://prob14.geekgame.pku.edu.cn/level3?guess='
# print(EMOJI_CHARS)
# browse through possibility
# {"alg":"HS256"}
# {"data":{"level":"1","remaining_guesses":"64"},"nbf":1697458448,"iat":1697458448}
RED = "🟥"
YELLOW = "🟨"
GREEN = "🟩"

emoji_train = ''.join(EMOJI_CHARS[0:64])
r = requests.get(URL3 + emoji_train)    
cookies = r.cookies
print(cookies, cookies['PLAY_SESSION'])
print(r.text.split('results.push("')[1].split('"')[0])

emoji_train = ''.join(EMOJI_CHARS[0:64])
r = requests.get(URL3 + emoji_train, cookies=cookies)    
cookies_next = r.cookies
print(cookies_next, cookies_next['PLAY_SESSION'])
print(r.text.split('results.push("')[1].split('"')[0])

emoji_train = ''.join(EMOJI_CHARS[0:64])
r = requests.get(URL3 + emoji_train, cookies=cookies)    
cookies_nextnext = r.cookies
print(cookies_nextnext, cookies_nextnext['PLAY_SESSION'])
print(r.text.split('results.push("')[1].split('"')[0])
print(cookies_nextnext == cookies_next)

def req_server(lv):
    if lv == 1:
        return lambda emo: requests.get(URL1 + emo)
    elif lv == 3:
        return lambda emo: requests.get(URL3 + emo, cookies=cookies)

REQ = req_server(3)

NONRED = []
for i in range(0, len(EMOJI_CHARS), 64):
    emoji_train = ''.join(EMOJI_CHARS[i:i+64])
    r = REQ(emoji_train).text
    result = r.split('results.push("')[1].split('"')[0]
    print(i, emoji_train, result)
    for ii, col in enumerate(result):
        if col != RED:
            NONRED.append(emoji_train[ii])
    time.sleep(.1)
    # break
print(NONRED)

FINAL_RES = {}
for i, emo in enumerate(NONRED):
    emoji_train = emo * 64
    r = REQ(emoji_train).text
    result = r.split('results.push("')[1].split('"')[0]
    print(i, emoji_train, result)
    for ii, col in enumerate(result):
        if col != YELLOW and col != RED:
            assert ii not in FINAL_RES
            FINAL_RES[ii] = emo
    time.sleep(.1)
print(FINAL_RES)

# FINAL_RES = {46: '👃', 50: '👂', 18: '👞', 25: '👴', 48: '👆', 57: '👆', 62: '👆', 28: '👵', 56: '👜', 36: '👢', 53: '👢', 8: '👱', 59: '👱', 26: '👿', 20: '👧', 2: '👼', 44: '👼', 11: '💆', 29: '💆', 54: '💆', 9: '👇', 39: '👶', 1: '💅', 38: '💅', 43: '💅', 52: '👲', 47: '💂', 6: '💊', 7: '💊', 10: '👔', 16: '👔', 30: '👩', 15: '👳', 51: '👳', 0: '💈', 41: '💈', 5: '👗', 24: '👸', 14: '👓', 33: '👓', 55: '👤', 3: '💁', 4: '👦', 13: '👦', 34: '👦', 31: '👽', 17: '👉', 19: '💄', 40: '👅', 42: '👈', 32: '👛', 61: '👛', 63: '👡', 45: '👁', 27: '👙', 35: '👝', 49: '👄', 12: '👺', 23: '👺', 58: '👺', 60: '👺', 22: '💃', 37: '💃', 21: '👘'}

real_res = ''.join([FINAL_RES[i] for i in range(64)])
r = REQ(real_res)
print(r.text)

