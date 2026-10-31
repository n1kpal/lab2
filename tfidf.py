from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import preprocess

'''
 Объявляем главную функцию поиска `tfidf_search`.
  Она принимает:
  1. `query` — строка с текстом запроса, который ввёл пользователь (например, `"кошка на окне"`).
  2. `doc_tokens` — словарь со всеми нашими документами, где ключ — это `doc_id` (например, `"doc1"`), а значение — список уже обработанных токенов (слов) этого документа.
  3. `config="C"` — режим предобработки текста (по умолчанию `"C"` — леммы без стоп-слов).
'''
def tfidf_search(query, doc_tokens, config="C"):
    doc_ids = list(doc_tokens.keys())
    docs = []
    for words in doc_tokens.values():
        docs.append(" ".join(words))

    # Словарь и матрица весов (со слайда 22)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(docs)
    vocab = vectorizer.vocabulary_
    matr = X.toarray()

    q_text = " ".join(preprocess(query, config))
    q_vec = vectorizer.transform([q_text])

    '''
      Метод `fit_transform` делает сразу два действия:
  1. `fit` — сканирует все документы, находит все уникальные слова и строит словарь.
  2. `transform` — переводит каждый документ в вектор чисел (строку матрицы), где каждое число — это вес конкретного слова
    '''


    #Косинусное сходство
    sims = cosine_similarity(q_vec, X)[0]

    #Документы с сходством > 0
    res = []
    for i in range(len(doc_ids)):
        if sims[i] > 0:
            res.append((float(sims[i]), doc_ids[i]))
    res.sort(reverse=True)

    #Итоговый список для выходных данных, если нужны только слова - убираем score
    ans = []
    for score, doc_id in res[:5]:
        ans.append((doc_id, score))

    return ans