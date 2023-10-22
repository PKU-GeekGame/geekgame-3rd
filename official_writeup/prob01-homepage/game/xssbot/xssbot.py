from selenium import webdriver
from pyvirtualdisplay import Display
import time
import sys
import traceback
import os
import re
from pathlib import Path
import shutil

import logger
from flag import getflag, checktoken

import functools
print = functools.partial(print, flush=True)

display = Display(visible=0, size=(800, 600))
display.start()
time.sleep(.3)

token = os.environ['hackergame_token']
uid = checktoken(token)

if not uid:
    print('bad token!')
    sys.exit(1)

def get_traceback(e):
    lines = traceback.format_exception(type(e), e, e.__traceback__)
    return ''.join(lines)

try:
    hacker_url = input('Your blog URL: ')
    assert len(hacker_url)<=1000
    
    logger.write(uid, ['enter_url', hacker_url])
    
    #match = re.match(r'^(https?)://([^/]+)/([/a-z0-9~_-]+)$', hacker_url)
    match = re.match(r'^(https?)://(prob99-[0-9a-z]{8}\.geekgame\.pku\.edu\.cn)/([/a-z0-9~_-]+)$', hacker_url)
    assert match is not None
    
    protocol, host, path = match.groups()
    admin_url = f'{protocol}://{host}/admin/'
    
    print('\nStarting up the browser...')
    
    data_path = Path('selenium_data').resolve()
    if data_path.is_dir():
        shutil.rmtree(data_path)
    data_path.mkdir()
    
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox') # sandbox not working in docker :(
    options.add_argument(f"user-data-dir={data_path}")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    if protocol=='http': # flag 1
    
        with webdriver.Chrome(options=options) as driver:
            print('\nSetting up flag 1')
            driver.get(admin_url)
            time.sleep(.5)
            driver.execute_script(f'document.cookie = "flag={getflag(token, 1)}; path=/admin"')
            time.sleep(.5)
            
            print('\nVisiting your webpage')
            driver.get(hacker_url)
            time.sleep(1)
            logger.write(uid, ['ch1_source_hacker', driver.page_source[:8192]])
            
            title = driver.title
            print('\nThe page title is:', title)
            logger.write(uid, ['final_title', title])
            
    else: # https, flag 2
        
        with webdriver.Chrome(options=options) as driver:
            print('\nVisiting your webpage')
            driver.get(hacker_url)
            time.sleep(1)
            logger.write(uid, ['ch2_source_hacker', driver.page_source[:8192]])
            
        with webdriver.Chrome(options=options) as driver:
            print('\nSetting up flag 2')
            driver.get(admin_url)
            time.sleep(.5)
            logger.write(uid, ['ch2_source_admin', driver.page_source[:8192]])
            
            driver.execute_script(f'document.cookie = "flag={getflag(token, 2)}; path=/admin"')
            time.sleep(1)
            
            title = driver.title
            print('\nThe page title is:', title)
            logger.write(uid, ['final_title', title])

    print('\nSee you later :)')
    logger.write(uid, ['leaving'])
    
except Exception as e:
    print('ERROR', type(e))
    tb = get_traceback(e)
    logger.write(uid, ['exception', str(type(e)), str(e), tb])
