import os
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *

from tqdm import tqdm


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
    with open('crawling_data/distinct_website_addresses_for_landmarks_asia2.txt', 'rt') as f:
        landmark_urls = f.read().splitlines()
except FileNotFoundError:
    with open('3-2_remove_duplicate_landmarks.py', 'rt') as f:
        exec(f.read())

if not os.path.isdir('./crawling_data/'):
    os.mkdir('./crawling_data/')


REFRESH_INTERVAL = 10
REVIEW_CNT_MAX = 150
URL_START_IDX = 153

countries = []
cities = []
landmarks = []
review_concats = []

for landmark_url in tqdm(landmark_urls[URL_START_IDX:],desc='리뷰 따는 중'):
    driver.get(landmark_url)
    
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN).perform()
    
    while True:  # infinite loop for a elements loading
        a_elements = driver.find_elements(By.CLASS_NAME, 'gl-component-bread-crumb_item')
        try:
            country = a_elements[3].text
        except IndexError:
            continue
        break
    city = a_elements[-2].text
    landmark = a_elements[-1].text
    
    review_concat = ''
    review_cnt = 0
    prev_p_element = None
    start_cnt = time.perf_counter()
    while review_cnt < REVIEW_CNT_MAX:  # infinite loop for crawling reviews of a landmark
        # review paragraph elements
        p_elements = driver.find_elements(By.CSS_SELECTOR, 'p[class*=\'hover-pointer \']')
        if not p_elements or p_elements[0] == prev_p_element:
            if time.perf_counter() - start_cnt > REFRESH_INTERVAL:  # at least 10s
                # press the next button
                div_element = driver.find_element(By.CSS_SELECTOR, 'div[class=\'gl-cpt-pagination \']')
                try:
                    btn_element = div_element.find_element(By.CSS_SELECTOR, 'button[class=\'btn-next \'')
                except NoSuchElementException:
                    break
                while True:  # infinite loop for button click
                    try:
                        btn_element.click()
                    except ElementClickInterceptedException:
                        continue
                    break
                
                start_cnt = time.perf_counter()
            continue
        
        if review_cnt + len(p_elements) > REVIEW_CNT_MAX:
            p_elements = p_elements[:REVIEW_CNT_MAX - review_cnt]
        cur_review_cnt = len(p_elements)
        
        temp_concat = ''
        try:
            for p_element in p_elements:
                temp_concat = temp_concat + ' ' + re.compile('[^가-힣]').sub(' ', p_element.text)
        except StaleElementReferenceException:
            continue
        review_concat = review_concat + temp_concat
        review_cnt += cur_review_cnt
        
        prev_p_element = p_elements[0]
        
        div_element = driver.find_element(By.CSS_SELECTOR, 'div[class=\'gl-cpt-pagination \']')
        try:
            btn_element = div_element.find_element(By.CSS_SELECTOR, 'button[class=\'btn-next \'')
        except NoSuchElementException:
            break
        while True:  # infinite loop for button click
            try:
                btn_element.click()
            except ElementClickInterceptedException:
                continue
            break
        
        start_cnt = time.perf_counter()
    
    countries.append(country)
    cities.append(city)
    landmarks.append(landmark)
    review_concats.append(review_concat)
    
    # temporal save
    with open('./crawling_data/country_list_asia2.txt', 'at', encoding='utf-8') as f:
        f.write('%s\n' % country)
    with open('./crawling_data/city_list_asia2.txt', 'at', encoding='utf-8') as f:
        f.write('%s\n' % city)
    with open('./crawling_data/landmark_list_asia2.txt', 'at', encoding='utf-8') as f:
        f.write('%s\n' % landmark)
    with open('./crawling_data/review_list_asia2.txt', 'at', encoding='utf-8') as f:
        f.write('%s\n' % review_concat)


# with open('crawling_data/country_list.txt', 'wt', encoding='utf-8') as f:
#     for country in countries:
#         f.write('%s\n' % country)
# with open('crawling_data/city_list.txt', 'wt', encoding='utf-8') as f:
#     for city in cities:
#         f.write('%s\n' % city)
# with open('crawling_data/landmark_list.txt', 'wt', encoding='utf-8') as f:
#     for landmark in landmarks:
#         f.write('%s\n' % landmark)
# with open('crawling_data/review_list.txt', 'wt', encoding='utf-8') as f:
#     for review_concat in review_concats:
#         f.write('%s\n' % review_concat)
