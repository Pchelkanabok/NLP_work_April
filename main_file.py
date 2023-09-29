import nltk
import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression
from nltk.tokenize import word_tokenize
from pymystem3 import Mystem
from nltk.corpus import stopwords
import re
import psycopg2
nltk.download('punkt')
nltk.download('stopwords')

connection = psycopg2.connect(host="localhost", port="2669", password="pass", dbname="bd_name", user="postgres")
connection.autocommit = True
df_orig = pd.read_sql("Select * from table_name WHERE 'Группа' is NULL", connection)

df_orig = df_orig.reset_index(drop=True)

ind_mas = []
for i in df_orig["Краткое содержание, что поручено"]:
    ind_mas.append(i)

for i in range(len(df_orig['Краткое содержание, что поручено'])):
    if "П О Р У Ч Е Н И Е" in df_orig['Краткое содержание, что поручено'][i]:
        df_orig['Краткое содержание, что поручено'][i] = df_orig['Краткое содержание, что поручено'][i].replace("П О Р У Ч Е Н И Е", "Поручение")

massive = []
for text in df_orig['Краткое содержание, что поручено']:
    text = str(text)
    massive.append(text)

punct = '!"#$%&()*\+,-\./:;<=>?@\[\]^_`{|}~„“«»†*\—/\-‘’'
clean_texts = []
for text in massive:
    text = str(text)
    clean_words = [w.strip(punct) for w in word_tokenize(text)]
    clean_texts.append(clean_words)

clean_texts_withoutnone = []
for text in clean_texts:
    text = list(filter(None, text))
    clean_texts_withoutnone.append(text)
clean_texts = clean_texts_withoutnone

clean_text_numbers = []
for text in clean_texts:
  for w in range(len(text)):
    text[w] = re.sub(r'[^\w\s]+|[\d]+', r'',text[w]).strip()

clean_texts_lower = []
for text in clean_texts:
    text_ = [w.lower() for w in text if w != '']
    clean_texts_lower.append(text_)
clean_lower = clean_texts_lower

sw = stopwords.words('russian')
clean_lower_sw = []
text_minus_sw = []
for text in range(len(clean_lower)):
    text_minus_sw = []
    for w in clean_lower[text]:
        if w not in sw:
            text_minus_sw.append(w)
    clean_lower[text] = text_minus_sw
clean_lower_sw = clean_lower

m = Mystem()
clean_lem = []
for text in clean_lower_sw:
    lem = m.lemmatize(' '.join(text))
    clean_lem.append(lem)
for text in clean_lower_sw:
    lem = m.lemmatize(' '.join(text))
    clean_lem.append(lem)

now_sent = []
for i in range(len(clean_lem)):
  now_sent = []
  for j in range(len(clean_lem[i])):
    if clean_lem[i][j] != '\n':
      clean_lem[i]

now_sent = ''
for i in range(len(clean_lem)):
  now_sent = ''
  for j in clean_lem[i]:
    now_sent = now_sent + j
  df_orig["Краткое содержание, что поручено"][i] = now_sent


with open('models/tfidf_2', 'rb') as training_model_tfidf:
  tfidf_vectorizer = pickle.load(training_model_tfidf)
tfidf_matrix_ = tfidf_vectorizer.transform(df_orig["Краткое содержание, что поручено"]).toarray()

X_all = tfidf_matrix_

with open('models/clssfr_2', 'rb') as training_model_cls:
  model = pickle.load(training_model_cls)
y_pred_all = model.predict(X_all)


for i in range(len(y_pred_all)):
    with connection.cursor() as cursor:
        str_sql = "UPDATE table_name SET 'Группа' = '" + y_pred_all[i] +"' WHERE 'Краткое содержание, что поручено' = '" + ind_mas[i] + "'"
        cursor.execute(str_sql)
connection.close()
