import json
from threading import Lock
import pathlib
import time

locks = {}
meta_lock = Lock()
def get_lock(uid):
    with meta_lock:
        if uid not in locks:
            locks[uid] = Lock()
        return locks[uid]

def write(uid, item):
    assert isinstance(item, list)
    encoded = (json.dumps([time.time()]+item)+'\n').encode('utf-8')
    with get_lock(uid):
        with (pathlib.Path('logs')/f'{uid}.log').open('ab') as f:
            f.write(encoded)