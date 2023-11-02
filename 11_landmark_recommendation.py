import os
import re

import pandas as pd
from joblib import load

from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
from konlpy.tag import Okt
from gensim.models import Word2Vec


def recommendation(cos_sim, topn):
    sim_score = list(enumerate(cos_sim[-1]))
    sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)
    sim_score_10 = sim_score[1:topn + 1]
    idx_list = [i[0] for i in sim_score_10]
    return idx_list


tfidf_paths = ['objects/matrix_landmark_morpheme.mtx', 'objects/tfidf_vectorizer.joblib']
if not all(os.path.isfile(tfidf_path) for tfidf_path in tfidf_paths):
    with open('9_TFIDF.py', 'rt') as f:
        exec(f.read())

df = pd.read_csv('datasets/df_all.csv')
tfidf_matrix = mmread('objects/matrix_landmark_morpheme.mtx').tocsr()
tfidf_vectorizer = load('objects/tfidf_vectorizer.joblib')


# Recommendation based on keyword
# embedding_model = Word2Vec.load('models/word2vec_review.model')
# keyword = ''
# sim_word = embedding_model.wv.most_similar(keyword, topn=10)
# print(sim_word)
# words = [keyword]
# for word, _ in sim_word:
#     words.append(word)
# print(words)
# 
# sentence = []
# cnt = 10
# for word in words:
#     sentence = sentence + [word] * cnt
#     cnt -= 1
# sentence = ' '.join(sentence)
# print(sentence)
# sentence_vec = tfidf_vectorizer.transform([sentence])
# cosine_sim = linear_kernel(sentence_vec, tfidf_matrix)
# landmark_idx = recommendation(cosine_sim, 10)
# landmark_list = df.iloc[landmark_idx, 2]
# print(landmark_list)


# Recommendation based on sentence
RAW_SENTENCE = '미국 역사를 알 수 있는 장소'

df_stopword = pd.read_csv('data/stopwords.csv', index_col=0)

okt = Okt()
sentence = re.sub('[^가-힣]', ' ', RAW_SENTENCE)
tokenized_sentence = okt.pos(sentence, stem=True)

df_morpheme_class = pd.DataFrame(tokenized_sentence, columns=['morpheme', 'class'])
df_morpheme_class = df_morpheme_class[(df_morpheme_class['class'] == 'Noun') |
                                      (df_morpheme_class['class'] == 'Verb') |
                                      (df_morpheme_class['class'] == 'Adjective')]

morphemes = []
for morpheme in df_morpheme_class['morpheme']:
    if len(morpheme) > 1 and morpheme not in df_stopword['stopword']:
        morphemes.append(morpheme)

embedding_model = Word2Vec.load('models/word2vec_review.model')

sim_words = []
for morpheme in morphemes:
    try:
        sim_word = embedding_model.wv.most_similar(morpheme, topn=10)
        for word, _ in sim_word:
            sim_words.append(word)
    except KeyError:
        continue

sim_sentence = ' '.join(sim_words)
sentence_vec = tfidf_vectorizer.transform([sim_sentence])
cosine_sim = linear_kernel(sentence_vec, tfidf_matrix)
landmark_idx = recommendation(cosine_sim, -2)
landmark_list = df.iloc[landmark_idx, 2]
print(landmark_list)
