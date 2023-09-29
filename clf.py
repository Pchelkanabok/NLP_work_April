import pymorphy2

def lemmatize(text):
    morph = pymorphy2.MorphAnalyzer()
    words = text.split()
    res = list()
    for word in words:
        p = morph.parse(word)[0]
        res.append(p.normal_form)
    return res


def one_str(text_):
    text = str(text_)
    if "П О Р У Ч Е Н И Е" in text:
        text = ''
        text = text.replace("П О Р У Ч Е Н И Е", "Поручение")\

    punct = '!"#$%&()*\+,-\./:;<=>?@\[\]^_`{|}~„“«»†*\—/\-‘’'
    clean_text = [w.strip(punct) for w in word_tokenize(text)]

    clean_texts_withoutnone = list(filter(None, clean_text))

    for w in range(len(clean_texts_withoutnone)):
        clean_texts_withoutnone[w] = re.sub(r'[^\w\s]+|[\d]+', r'', clean_texts_withoutnone[w]).strip()

    clean_lower = [w.lower() for w in clean_texts_withoutnone if w != '']

    sw = stopwords.words('russian')
    text_minus_sw = []
    for w in clean_lower:
        if w not in sw:
            text_minus_sw.append(w)
    clean_lower_sw = text_minus_sw

    #Это с pymystem3
    """    m = Mystem()
    lem = m.lemmatize(' '.join(clean_lower_sw))
    """
    #Это с pymorphy2
    print(' '.join(clean_lower_sw))
    print(clean_lower_sw)
    lem = lemmatize(' '.join(clean_lower_sw))
    print(lem)
    now_sent = ''
    for j in lem:
        now_sent = now_sent + ' ' + j

    with open(config['model_classificator_parameters']['model_tfidf_with_name_path'], 'rb') as training_model_tfidf:
        tfidf_vectorizer = pickle.load(training_model_tfidf)
    tfidf_matrix_ = tfidf_vectorizer.transform([now_sent]).toarray()

    with open(config['model_classificator_parameters']['model_path_with_name'], 'rb') as training_model_cls:
        model = pickle.load(training_model_cls)
    y_pred_all = model.predict(tfidf_matrix_)

    return y_pred_all[0]


def create_classificator_from_model(one_column_from_df):
    res_mas = []
    for i in one_column_from_df:
        res_mas.append(one_str(i))
    result = pd.Series(res_mas)

    return result
