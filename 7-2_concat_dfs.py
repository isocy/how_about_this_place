import pandas as pd


df_landmark_review = pd.concat([
    pd.read_csv('datasets/df_north-america.csv')
    # ,pd.read_csv('datasets/df_asia'),
    # pd.read_csv('datasets/df_europe'),
    # pd.read_csv('datasets/df_others.csv')
], axis='rows', ignore_index=True)

df_landmark_review.info()

df_landmark_review.to_csv('./datasets/df_all.csv', index=False)
