import os
import re
import sys
from joblib import load

import pandas as pd

from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
from konlpy.tag import Okt
import gdown

from PyQt5.QtWidgets import *
from PyQt5 import uic

form_window = uic.loadUiType('./app.ui')[0]  # 'Ui_Form' class


class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__(None)
        self.setupUi(self)

        self.tfidf_matrix = mmread('./objects/matrix_landmark_morpheme.mtx').tocsr()
        self.tfidf_vectorizer = load('./objects/tfidf_vectorizer.joblib')
        self.embedding_model = Word2Vec.load('./models/word2vec.model')

        self.df = pd.read_csv('./datasets/df_all.csv')
        self.df_selected = None
        self.countries = set(self.df['country'])
        
        self.comboBox.addItem('모든 나라')
        for country in self.countries:
            self.comboBox.addItem(country)

        self.pushButton.clicked.connect(self.pushbutton_slot)

    def pushbutton_slot(self):
        lineedit_str = self.lineEdit.text()
        length = len(lineedit_str.split())
        if length == 0:
            return
        elif length == 1:
            recommendation = self.recommend_by_keyword(lineedit_str)
        else:
            recommendation = self.recommend_by_sentence(lineedit_str)
        if isinstance(recommendation, str):
            self.label_res.setText(recommendation)
        else:
            self.label_res.setText('\n'.join(recommendation))

    def recommend_by_sentence(self, sentence):
        if not os.path.isfile('data/stopwords.csv'):
            gdown.download(
                'https://drive.google.com/uc?id=1TBefeqPHFT_lxObF_WOmzrv891Lik6-U',
                'data/stopwords.csv', quiet=True
            )
        df_stopword = pd.read_csv('data/stopwords.csv', index_col=0)

        okt = Okt()
        sentence = re.sub('[^가-힣]', ' ', sentence)
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
        sentence_vec = self.tfidf_vectorizer.transform([sim_sentence])
        cosine_sim = linear_kernel(sentence_vec, self.tfidf_matrix)
        landmark_idx = self.recommendation(cosine_sim)
        landmark_list = self.df.iloc[landmark_idx, 2]
        return landmark_list

    def recommend_by_keyword(self, keyword):
        try:
            sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)
        except:
            return 'Use another keyword'
        words = [keyword]
        for word, _ in sim_word:
            words.append(word)

        sentence = []
        cnt = 10
        for word in words:
            sentence = sentence + [word] * cnt
            cnt -= 1
        sentence = ' '.join(sentence)
        sentence_vec = self.tfidf_vectorizer.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, self.tfidf_matrix)
        recommendation = self.get_recommendation(cosine_sim)
        return recommendation

    def recommendation(self, cos_sim):
        sim_score = list(enumerate(cos_sim[-1]))
        sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)
        sim_score_10 = sim_score[1:]
        idx_list = [i[0] for i in sim_score_10]
        return idx_list


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())
