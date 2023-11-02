import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *


if not os.path.isfile('./paths/chrome_driver_path.txt'):
    with open('1_install_Chrome_driver.py', 'rt') as f:
        exec(f.read())

with open('./paths/chrome_driver_path.txt', 'rt') as f:
    service = Service(f.read())


options = Options()
user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari'
              '/537.36')
options.add_argument('user_agent=' + user_agent)

driver = webdriver.Chrome(service=service, options=options)


url = 'https://kr.trip.com/travel-guide/north-america-120004/cities/?locale=ko-KR&curr=KRW'

driver.get(url)


REFRESH_INTERVAL = 0.5

address_frags = []

cur_page = 1
while True:  # infinite loop for pages traversal
    img_elements = driver.find_elements(By.CLASS_NAME, 'img-warp')
    if not img_elements:
        continue
    
    should_be_retried = False
    
    temp_frags = []
    for img_element in img_elements:
        a_element = None
        start_cnt = time.perf_counter()
        while True:  # infinite loop for a tag loading
            try:
                a_element = img_element.find_element(By.TAG_NAME, 'a')
            except StaleElementReferenceException:
                if time.perf_counter() - start_cnt > REFRESH_INTERVAL:  # at least 0.5s
                    should_be_retried = True
                    break
                continue
            break
        if should_be_retried:
            break

        start_cnt = time.perf_counter()
        while True:  # infinite loop for page loading
            try:
                temp_frags.append(a_element.get_attribute('href').split('/')[5])
            except StaleElementReferenceException:
                if time.perf_counter() - start_cnt > REFRESH_INTERVAL:  # at least 0.5s
                    should_be_retried = True
                    break
                continue
            except AttributeError:
                should_be_retried = True
            break
        if should_be_retried:
            break
    
    if should_be_retried:
        driver.get('https://kr.trip.com/travel-guide/north-america-120004/{}/?locale=ko-KR&curr=KRW'.format(
            cur_page))
        continue
    address_frags = address_frags + temp_frags
    
    try:
        btn_element = driver.find_element(By.CSS_SELECTOR, 'button[class=\'btn-next \']')
    except NoSuchElementException:
        break
    while True:  # infinite loop for button click
        try:
            btn_element.click()
        except ElementClickInterceptedException:
            continue
        break
    
    cur_page += 1


if not os.path.isdir('crawling_data/'):
    os.mkdir('crawling_data/')

with open('crawling_data/website_address_fragments_for_cities.txt', 'wt') as f:
    for frag in address_frags:
        f.write('%s\n' % frag)
