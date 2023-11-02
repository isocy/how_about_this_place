import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *


if not os.path.isfile('./paths/chrome_driver_path.txt'):
    with open('1_install_Chrome_driver.py', 'rt') as file:
        exec(file.read())

with open('./paths/chrome_driver_path.txt', 'rt') as file:
    service = Service(file.read())


options = Options()
user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari'
              '/537.36')
options.add_argument('user_agent=' + user_agent)

driver = webdriver.Chrome(service=service, options=options)


try:
    with open('crawling_data/website_address_fragments_for_cities.txt', 'rt') as f:
        address_frags = f.read().splitlines()
except FileNotFoundError:
    with open('2_crawl_website_address_fragments_for_cities.py', 'rt') as f:
        exec(f.read())


REFRESH_INTERVAL = 0.5

landmark_urls = []
for address_frag in address_frags:
    url = ('https://kr.trip.com/travel-guide/attraction/{}/tourist-attractions/comment-count-1011-100'
           '/?locale=ko-KR&curr=KRW').format(address_frag)
    
    driver.get(url)
    
    try:
        driver.find_element(By.CLASS_NAME, 'error-inner')
    except NoSuchElementException:
        pass
    else:
        continue
    
    cur_page = 1
    while True:  # infinite loop for pages traverse
        try:
            driver.find_element(By.CLASS_NAME, 'pc-poi-list-empty')
        except NoSuchElementException:
            pass
        else:
            break
        
        a_elements = driver.find_elements(By.CLASS_NAME, 'online-poi-item-card')
        if not a_elements:
            continue

        should_be_retried = False
        
        start_cnt = time.perf_counter()
        while True:  # infinite loop for attribute loading
            try:
                landmark_urls = landmark_urls + [a_element.get_attribute('href') for a_element in a_elements]
            except StaleElementReferenceException:
                if time.perf_counter() - start_cnt > REFRESH_INTERVAL:  # at least 0.5s
                    should_be_retried = True
                    break
                continue
            break
        
        if should_be_retried:
            driver.get('https://kr.trip.com/travel-guide/attraction/{}/tourist-attractions/comment-count-1011-100'
                       '/{}.html/?locale=ko-KR&curr=KRW'.format(address_frag, cur_page))
            continue
        
        try:
            btn_element = driver.find_elements(By.CLASS_NAME, 'ant-pagination-item-link')[1]
        except IndexError:
            break
        if btn_element.get_attribute('disabled'):
            break
        
        while True:  # infinite loop for button click
            try:
                btn_element.click()
            except ElementClickInterceptedException:
                continue
            break
        
        cur_page += 1


with open('crawling_data/website_addresses_for_landmarks.txt', 'wt') as f:
    for landmark_url in landmark_urls:
        f.write('%s\n' % landmark_url)
