import nltk
import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression
from nltk.tokenize import word_tokenize
from pymystem3 import Mystem
from nltk.corpus import stopwords
import re
nltk.download('punkt')
nltk.download('stopwords')

def creat_classificator_from_model(one_column_from_df):
    for i in range(len(one_column_from_df)):
        if "П О Р У Ч Е Н И Е" in one_column_from_df[i]:
            one_column_from_df[i] = one_column_from_df[i].replace(
                "П О Р У Ч Е Н И Е", "Поручение")

    massive = []
    for text in one_column_from_df:
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
            text[w] = re.sub(r'[^\w\s]+|[\d]+', r'', text[w]).strip()

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
        one_column_from_df[i] = now_sent

    with open('models/tfidf_2', 'rb') as training_model_tfidf:
        tfidf_vectorizer = pickle.load(training_model_tfidf)
    tfidf_matrix_ = tfidf_vectorizer.transform(one_column_from_df).toarray()

    X_all = tfidf_matrix_

    with open('models/clssfr_2', 'rb') as training_model_cls:
        model = pickle.load(training_model_cls)
    y_pred_all = model.predict(X_all)

    result = pd.Series(y_pred_all)
    return result
