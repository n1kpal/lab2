#Сравнение конфигураций A/B/C/D.
#Прогон всех запросов с каждой конфигурацией A/B/C/D. С использованием поиска, написанного ранее. А также сравнение результата.
#Функция принимает словари документов и запросов и возвращает словарь:
#внешний ключ - "A"/"B"/"C"/"D"; внутренний ключ - айди запроса;
# значение - список пар (айди документа, оценка того насколько подходит документ под запрос). Сортируется по убыванию

from preprocess import preprocess # задача 2
from baseline import baseline_search # задача 3
from tfidf import tfidf_search # задача 4

Configs = ("A", "B", "C", "D")
k = 5 # это, чтобы возвращалось не больше пяти документов

# сначала применяем функцию для подготовки документов
def tokens(texts, config):
    return {str(key): preprocess(text, config) for key, text in texts.items()}


# Прогоняем все запросы через поиск с каждой конфигурацией A/B/C/D.
# searcher: "tfidf" (задача 4) или "baseline" (задача 3). Прогоняем по ним и сравниваем результат

def allConfigs(documents, queries, searcher="tfidf"):
    if searcher not in ("tfidf", "baseline"):
        raise ValueError(f"Неправильный ввод: {searcher!r}")
    result = {}

    for cfg in Configs:
        # токенизируем документы
        doctoc = tokens(documents, cfg)
        slov = {} #Промежуточный словарь
        for sid, stext in queries.items():
            if searcher == "tfidf":
                slov[str(sid)] = tfidf_search(
                    query = stext,
                    doc_tokens = doctoc,
                    config = cfg,
                )
            else:
                slov[str(sid)] = baseline_search(
                    query = stext,
                    doc_tokens = doctoc,
                    config = cfg,
                    top_k = k,
                    metric = "coverage",
                )
        result[cfg] = slov
    return result