# -*- coding: utf-8 -*-
"""Amazon Reviews Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BgDCK0MGS3qCnTvhbPMtB4TKTNAg6J3J
"""

import pandas as pd
import numpy as np
import seaborn as sns

from google.colab import files
files.upload()

amazon_df = pd.read_csv('Reviews.csv')

amazon_df.head()

amazon_df.info()

amazon_df.describe()

# Length of Text
amazon_df['Length'] = amazon_df['Text'].apply(len)

amazon_df.Length.describe()

#Longest Text
amazon_df[amazon_df['Length'] == 21409]['Text'].iloc[0]

#Shortest Text
amazon_df[amazon_df['Length'] ==12 ]['Text'].iloc[0]

sns.countplot(y='Score', data=amazon_df)

# Percentage of Each review
amazon_1 =amazon_df[amazon_df['Score'] == 1]
amazon_2 =amazon_df[amazon_df['Score'] == 2]
amazon_3 =amazon_df[amazon_df['Score'] == 3]
amazon_4 =amazon_df[amazon_df['Score'] == 4]
amazon_5 =amazon_df[amazon_df['Score'] == 5]

print('1-Star Percentage :', (len(amazon_1)/ len(amazon_df))*100,'%')
print('2-Star Percentage :', (len(amazon_2)/ len(amazon_df))*100,'%')
print('3-Star Percentage :', (len(amazon_3)/ len(amazon_df))*100,'%')
print('4-Star Percentage :', (len(amazon_4)/ len(amazon_df))*100,'%')
print('5-Star Percentage :', (len(amazon_5)/ len(amazon_df))*100,'%')

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def clean_text(text):
  text = [word for word in text if word not in string.punctuation]
  text_join = ''.join(text)
  text_join_clean = [word for word in text_join.split() if word.lower() not in stopwords.words('english')]
  return text_join_clean

amazon_df_clean = amazon_df['Text'].apply(clean_text)

vectorizer = CountVectorizer(analyzer = clean_text)
amazon_vec = vectorizer.fit_transform(amazon_df['Text'])
amazon_tfidf = TfidfTransformer().fit_transform(amazon_vec)

"""# Split the Data and Train"""

from sklearn.model_selection import train_test_split
X = amazon_tfidf
y = amazon_df['Score'].values
X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=1,test_size=0.3)

X.shape

y.shape

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train,y_train)

"""Evaluate the model

"""

from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
y_preds = model.predict(X_text)
sns.heatmap(confusion_matrix(y_test,y_preds), annot=True)

print(classification_report(y_test,y_preds))

print(accuracy_score(y_test,y_preds))

