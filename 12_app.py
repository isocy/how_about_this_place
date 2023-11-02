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
        self.embedding_model = Word2Vec.load('./models/word2vec_review.model')

        self.df = pd.read_csv('./datasets/df_all.csv')

        self.RECOMMENDATION_CNT = 10

        self.countries = list(set(self.df['country']))
        self.countries.sort()

        self.str_all_countries = '모든 나라'
        self.comboBox.addItem(self.str_all_countries)
        for country in self.countries:
            self.comboBox.addItem(country)

        self.pushButton.clicked.connect(self.pushbutton_slot)

    def pushbutton_slot(self):
        self.label_res.setText('')
        self.label_loading.setText('로딩 중...')

        lineedit_str = self.lineEdit.text()
        length = len(lineedit_str.split())
        if length == 0:
            self.label_loading.setText('')
            return
        elif length == 1:
            idx_list = self.recommend_by_keyword(lineedit_str)
            print(idx_list)
        else:
            idx_list = self.recommend_by_sentence(lineedit_str)

        res_str = ''
        if self.comboBox.currentText() != self.str_all_countries:
            country = self.comboBox.currentText()
            idx_10 = []
            idx_cnt = 0
            for landmark_idx in idx_list:
                if country == self.df.iloc[landmark_idx, 0]:
                    idx_10.append(landmark_idx)
                    idx_cnt += 1
                    if idx_cnt == self.RECOMMENDATION_CNT:
                        break

            for landmark_idx in idx_10:
                landmark_row = self.df.iloc[landmark_idx, 1:3]
                res_str = res_str + ' / '.join(landmark_row) + '\n'
        else:
            idx_10 = idx_list[:min(len(idx_list), self.RECOMMENDATION_CNT)]

            for landmark_idx in idx_10:
                landmark_row = self.df.iloc[landmark_idx, :3]
                res_str = res_str + ' / '.join(landmark_row) + '\n'

        if not idx_10:
            self.label_loading.setText('다른 단어를 입력하거나 문장을 입력해주세요.')
            return

        self.label_loading.setText('')
        self.label_res.setText(res_str)

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
        return landmark_idx

    def recommend_by_keyword(self, keyword):
        try:
            sim_word = self.embedding_model.wv.most_similar(keyword, topn=9)
        except KeyError:
            return []
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
        landmark_idx = self.recommendation(cosine_sim)
        return landmark_idx

    def recommendation(self, cos_sim):
        sim_score = list(enumerate(cos_sim[-1]))
        sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)
        sim_score = sim_score[1:]
        end_idx = 0
        for t in sim_score:
            if t[1] < 0.05:
                break
            end_idx += 1
        idx_list = [t[0] for t in sim_score[:end_idx]]
        return idx_list


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())
