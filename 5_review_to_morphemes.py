import os
import json

import pandas as pd
from konlpy.tag import Okt
from tqdm import tqdm

category = 'asia'

# df = pd.read_csv('crawling_data/reviews_list_{}.csv'.format(category))
# df2 = pd.read_csv('crawling_data/reviews_list_asia2.csv')
# df = pd.concat([df,df2],ignore_index=True)
# df.drop_duplicates(subset='landmark',keep='first',inplace=True)
# print(df.info())

# country = list(df['country'])
# city = list(df['city'])
# landmark = list(df['landmark'])
# review = list(df['review'])
#

# with open('crawling_data/country_list_asia2.txt'.format(category), 'rt', encoding='utf-8') as f:
#     country = f.read().splitlines()
# with open('crawling_data/city_list_asia2.txt'.format(category), 'rt', encoding='utf-8') as f:
#     city = f.read().splitlines()
# with open('crawling_data/landmark_list_asia2.txt'.format(category), 'rt', encoding='utf-8') as f:
#     landmark = f.read().splitlines()
# with open('crawling_data/review_list_asia2.txt'.format(category), 'rt', encoding='utf-8') as f:
#     review = f.read().splitlines()
#
# for i in range(len(country)):
#     with open('./crawling_data/country_list_{}.txt'.format(category), 'at', encoding='utf-8') as f:
#         f.write('%s\n' % country[i])
#     with open('./crawling_data/city_list_{}.txt'.format(category), 'at', encoding='utf-8') as f:
#         f.write('%s\n' % city[i])
#     with open('./crawling_data/landmark_list_{}.txt'.format(category), 'at', encoding='utf-8') as f:
#         f.write('%s\n' % landmark[i])
#     with open('./crawling_data/review_list_{}.txt'.format(category), 'at', encoding='utf-8') as f:
#         f.write('%s\n' % review[i])

# if not os.path.isfile('crawling_data/review_list_{}.txt'.format(category)):
#     with open('./4_crawl_reviews.py', 'rt') as f:
#         exec(f.read())
#
with open('crawling_data/review_list_{}.txt'.format(category), 'rt', encoding='utf-8') as f:
    review_concats = f.read().splitlines()

okt = Okt()
div_review_list = []
for review_concat in tqdm(review_concats,desc='형태소로 분리 중'):
    div_review_list.append(okt.pos(review_concat, stem=True))

if not os.path.isdir('data/'):
    os.mkdir('data/')

div_review_list = [[list(t) for t in review] for review in div_review_list]
with open('data/div_review_list_{}.json'.format(category), 'wt') as f:
    json.dump(div_review_list, f)
