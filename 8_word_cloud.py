import os
import collections

import pandas as pd
from matplotlib import font_manager
import matplotlib.pyplot as plt
import gdown

from wordcloud import WordCloud


LANDMARK_IDX = 64

font_path = 'fonts/malgun.ttf'

if not os.path.isfile('fonts/malgun.ttf'):
    gdown.download(
        'https://drive.google.com/uc?id=1a647msm7ciE6LXh2yQWYVJLU7eQp4TTn',
        font_path, quiet=True
    )

font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rc('font', family='NanumBarunGothic')

if not os.path.isfile('datasets/df_all.csv'):
    with open('7-2_concat_dfs.py', 'rt') as f:
        exec(f.read())

df = pd.read_csv('datasets/df_all.csv')

words = df.iloc[LANDMARK_IDX, 3].split()
word_dict = collections.Counter(words)
word_dict = dict(word_dict)
print(word_dict)

wordcloud_img = WordCloud(
    background_color='white', max_words=2000, font_path=font_path
).generate_from_frequencies(word_dict)

plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()
