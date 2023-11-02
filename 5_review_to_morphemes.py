import os
import json

from konlpy.tag import Okt


if not os.path.isfile('crawling_data/review_list.txt'):
    with open('./4_crawl_reviews.py', 'rt') as f:
        exec(f.read())

with open('crawling_data/review_list.txt', 'rt', encoding='utf-8') as f:
    review_concats = f.read().splitlines()


okt = Okt()
div_review_list = []
for review_concat in review_concats:
    div_review_list.append(okt.pos(review_concat, stem=True))

if not os.path.isdir('data/'):
    os.mkdir('data/')

div_review_list = [[list(t) for t in review] for review in div_review_list]
with open('data/div_review_list.json', 'wt') as f:
    json.dump(div_review_list, f)
