import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


reviews_df = pd.read_csv("list.csv", sep=',')
# print(reviews_df)
description_list = reviews_df
print(reviews_df.columns)

print(reviews_df.description.values)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(reviews_df.description.values)
print(X_train_counts.shape)
print(count_vect.vocabulary_)
