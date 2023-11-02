import os

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump
from scipy.io import mmwrite


if not os.path.isfile('datasets/df_all.csv'):
    with open('7-2_concat_dfs.py', 'rt') as f:
        exec(f.read())

df = pd.read_csv('datasets/df_all.csv')
df.info()

tfidf_vectorizer = TfidfVectorizer(sublinear_tf=True)
tfidf_matrix = tfidf_vectorizer.fit_transform(df['review'])
print(tfidf_matrix.shape)

if not os.path.isdir('objects/'):
    os.mkdir('objects/')

dump(tfidf_vectorizer, 'objects/tfidf_vectorizer.joblib')
mmwrite('objects/matrix_movie_morpheme.mtx', tfidf_matrix)
