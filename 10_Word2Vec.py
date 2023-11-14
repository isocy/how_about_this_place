import os

import pandas as pd
from gensim.models import Word2Vec
from tqdm import tqdm

# if not os.path.isfile('data/refined_div_review_list.txt'):
#     with open('6_refine_morphemes.py', 'rt') as f:
#         exec(f.read())
#
# with open('data/refined_div_review_list.txt', 'rt', encoding='utf-8') as f:
#     div_review_list = f.read().splitlines()

df = pd.read_csv('datasets/df_all.csv')
div_review_list = list(df['review'])

tokens = []
for div_review in tqdm(div_review_list,desc='Tokenizer'):
    token = div_review.split()
    tokens.append(token)

if not os.path.isdir('models/'):
    os.mkdir('models/')

embedding_model = Word2Vec(tokens, vector_size=100, window=4, min_count=5, workers=12, epochs=100, sg=1)
embedding_model.save('./models/word2vec_review.model')
# print(list(embedding_model.wv.index_to_key))
