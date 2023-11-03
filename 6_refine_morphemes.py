import os
import json

import pandas as pd

import gdown


# if not os.path.isfile('data/div_review_list.json'):
#     with open('5_review_to_morphemes.py', 'rt') as f:
#         exec(f.read())

category = 'asia'

with open('data/div_review_list_{}.json'.format(category), 'rt') as f:
    div_review_list = json.load(f)

if not os.path.isfile('data/stopwords.csv'):
    gdown.download(
        'https://drive.google.com/uc?id=1TBefeqPHFT_lxObF_WOmzrv891Lik6-U',
        'data/stopwords.csv', quiet=True
    )
df_stopword = pd.read_csv('data/stopwords.csv', index_col=0)


for review_idx in range(len(div_review_list)):
    df_morpheme_class = pd.DataFrame(div_review_list[review_idx], columns=['morpheme', 'class'])
    df_morpheme_class = df_morpheme_class[(df_morpheme_class['class'] == 'Noun') |
                                          (df_morpheme_class['class'] == 'Verb') |
                                          (df_morpheme_class['class'] == 'Adjective')]

    morphemes = []
    for morpheme in df_morpheme_class['morpheme']:
        if len(morpheme) > 1 and morpheme not in df_stopword['stopword']:
            morphemes.append(morpheme)

    div_review_list[review_idx] = ' '.join(morphemes)

with open('data/refined_div_review_list_{}.txt'.format(category), 'wt', encoding='utf-8') as f:
    for review in div_review_list:
        f.write('%s\n' % review)
