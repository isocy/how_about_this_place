# try:
#     with open('crawling_data/website_addresses_for_landmarks.txt', 'rt') as f:
#         landmark_urls = f.read().splitlines()
# except FileNotFoundError:
#     with open('3-1_crawl_website_addresses_for_landmarks.py', 'rt') as f:
#         exec(f.read())
#
# landmark_urls = list(set(landmark_urls))
#
# with open('crawling_data/distinct_website_addresses_for_landmarks.txt', 'wt') as f:
#     for landmark_url in landmark_urls:
#         f.write('%s\n' % landmark_url)

import pandas as pd
from tqdm import tqdm

df_url = pd.read_csv('crawling_data/일본_후지산_landmark_url.csv')
df_url.dropna(inplace=True)
df_url.drop_duplicates(subset='landmark',keep='first',inplace=True, ignore_index=True)
print(df_url.info())

city = df_url['city'][605:]
city = city.unique()

landmark_urls = []

for c in tqdm(city,desc='url 저장 중'):
    index = list(df_url.index[df_url['city']==c][:10])
    for idx in index:
        url = df_url['url'][idx]
        landmark_urls.append(url)

with open('crawling_data/distinct_website_addresses_for_landmarks_asia2.txt', 'wt') as f:
    for landmark_url in landmark_urls:
        f.write('%s\n' % landmark_url)