import pandas as pand
"""
Здесь мы достаем нужную библиотеку которая может считывать файлы и имеет при себе несколько методов
Вообще тут может возникнуть проблема с нахожением файлов csv
У меня они просто все в одной папке на компе так что проблем не было. Но если возникнут то добавь следующую строку
import os
Я уточнял у иишки. она должна находить если не в одной папке вроде как
"""
def reading_files(docs_path="documents.csv", queries_path="queries.csv", relevance_path="dev_relevance.csv"):
    docs_datafraime = pand.read_csv(docs_path, encoding="utf-8-sig", sep=",")
    queries_datafraime = pand.read_csv(queries_path, encoding="utf-8-sig", sep=",")
    relevance_datafraime = pand.read_csv(relevance_path, encoding="utf-8-sig", sep=",")
    """
    Щас я кое что уточню. На самом деле по сути здесь используются датафреймы
    Которые позже переводятся в словарь в угоду удобсвта остальным.
    Почему же я просто не вписал все в словари?
    Дело в том что по моему заданию мне нужно рассмотреть пропуски, дубликаты и типы полей
    Конечно это можно сделать и без pandas но тогда код расстянется оооооочень сильно
    А тут как раз удобные методы в одну строчку
    С помощью метода мы читаем файл который мы написали
    Далее делаем -sig потому что у нас в начале может появится невидимый символ который называется BOM
    Да я старался тщательно просмотреть где я могу запнуться
    Ну и так как это датафрейм то как разделитель мы поставили запятую
    """
    print("Вывод небольшого отчёта")
    print("Документы:")
    print(f"Количество строк: {len(docs_datafraime)}")
    print("Типы полей: str")  
    print(f"Пропуски в тексте: {docs_datafraime.iloc[:, 3].isna().sum()}")
    print(f"Дубликаты: {docs_datafraime.iloc[:, 3].duplicated().sum()}")
    """
    Щас напишу что делают некоторые методы из pandas
    isna() - ищет пустые клетки (У нас их правда нет но отчёт есть отчёт
    sum() - думаю очевидно но ладно. Считает сумму и в совокупности с предыдущим методом суммирует
    Все пустые строки
    iloc[:, 3] - Позволяет выбрать конкретную колонку и конкретную строку ([строка, колонка])
    Я сразу поставил какую колонку мы смотри так что 3. Двоеточие же заставляет смотреть все строки а не одну конкретную
    Ну и метод duplicated() -  он смотрит повторы. Конечно очевидно что повторок не должо быть
    Но отчёт ЕСТЬ отчёт
    """
    print()
    print("Запросы:")
    print(f"Количество строк: {len(queries_datafraime)}")
    print(f"Типы полей: str")
    print(f"Пропуски в запросах: {queries_datafraime.iloc[:, 1].isna().sum()}")
    print(f"Дубликаты: {queries_datafraime.iloc[:, 1].duplicated().sum()}")
    print()
    print("Релевантность:")
    print(f"Количество строк: {len(relevance_datafraime)}")
    print(f"Типы полей: str")  
    print(f"Пропуски в ответах: {relevance_datafraime.iloc[:, 1].isna().sum()}")
    docs_dict = {}
    for i in range(len(docs_datafraime)):
        doc_id = docs_datafraime["document_id"][i]
        title = docs_datafraime["title"][i]
        section = docs_datafraime["section"][i]
        text = docs_datafraime["text"][i]
        docs_dict[doc_id] = {"title": title, "section": section, "text": text}
    queries_dict = {}
    for i in range(len(queries_datafraime)):
        query_id = queries_datafraime["query_id"][i]
        query = queries_datafraime["query"][i]
        difficulty = queries_datafraime["difficulty"][i]
        queries_dict[query_id] = {"query": query, "difficulty": difficulty}
    relevance_dict = {}
    for i in range(len(relevance_datafraime)):
        query_id = relevance_datafraime["query_id"][i]
        doc_id = relevance_datafraime["relevant_document_id"][i]
        if query_id not in relevance_dict:
            relevance_dict[query_id] = []
        relevance_dict[query_id].append(doc_id)
    """
    Тут у нас особый случай из за того что у одного айди запроса может быть несколько документов
    поэтому я тут в if создаю списко в который в дальнейшем помещаю все
    """
    return docs_dict, queries_dict, relevance_dict