import os

import pandas as pd


# if not os.path.isfile('data/refined_div_review_list.txt'):
#     with open('6_refine_morphemes.py', 'rt') as f:
#         exec(f.read())

category = 'asia'
with open('crawling_data/country_list_{}.txt'.format(category), 'rt', encoding='utf-8') as f:
    countries = f.read().splitlines()
with open('crawling_data/city_list_{}.txt'.format(category), 'rt', encoding='utf-8') as f:
    cities = f.read().splitlines()
with open('crawling_data/landmark_list_{}.txt'.format(category), 'rt', encoding='utf-8') as f:
    landmarks = f.read().splitlines()
with open('data/refined_div_review_list_{}.txt'.format(category), 'rt', encoding='utf-8') as f:
    reviews = f.read().splitlines()

df_landmark_review = pd.DataFrame({
    'country': countries,
    'city': cities,
    'landmark': landmarks,
    'review': reviews
})
df_landmark_review.drop_duplicates(subset='landmark', inplace=True, keep='first')
df_landmark_review.info()

if not os.path.isdir('datasets/'):
    os.mkdir('datasets/')

df_landmark_review.to_csv('datasets/df_{}.csv'.format(category), index=False)
