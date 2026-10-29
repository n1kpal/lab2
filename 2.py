import csv
import re
import pymorphy3
import nltk
from nltk.corpus import stopwords

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

morph = pymorphy3.MorphAnalyzer()
russian_stopwords = set(stopwords.words('russian'))

def preprocess(text: str, config: str) -> list[str]:
    """
    очистка, токенизация, лемматизация и извлечение n-грамм.

    Что принимает:
        text (str): Исходный сырой текст из ячейки таблицы.
        config (str): Конфигурация обработки. Строго один символ из {'A', 'B', 'C', 'D'}.
            - A: без лемм, стоп-слова остаются, только униграммы.
            - B: леммы, стоп-слова остаются, только униграммы.
            - C: леммы, стоп-слова удаляются, только униграммы.
            - D: леммы, стоп-слова удаляются, униграммы + биграммы (через '_').

    Что возвращает:
        list[str]: Список токенов. Пустой запрос или пустая строка -> [].
        *Важно*: Возвращает list, а не set, сохраняя частоты для Задачи 4.
    """
    if not isinstance(text, str) or not text.strip():
        return []
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)  # Удаление URL
    text = re.sub(r'\S+@\S+', ' ', text)  # Удаление e-mail
    text = re.sub(r'\d+', ' ', text)  # Удаление чисел
    tokens = re.findall(r'[а-яёa-z]+', text.lower())

    if not tokens:
        return []

    # Конфигурация A: униграммы в исходной форме, стоп-слова на месте
    if config == 'A':
        return tokens

    # Лемматизация (нужна для B, C, D)
    lemmatized_tokens = [morph.parse(word)[0].normal_form for word in tokens]

    # Конфигурация B: леммы, стоп-слова на месте
    if config == 'B':
        return lemmatized_tokens

    # Фильтрация стоп-слов (нужна для C, D)
    filtered_tokens = [word for word in lemmatized_tokens if word not in russian_stopwords]

    # Конфигурация C: леммы, без стоп-слов
    if config == 'C':
        return filtered_tokens

    # Конфигурация D: леммы, без стоп-слов, униграммы + биграммы (через '_')
    if config == 'D':
        result = list(filtered_tokens)
        for i in range(len(filtered_tokens) - 1):
            bigram = f"{filtered_tokens[i]}_{filtered_tokens[i + 1]}"
            result.append(bigram)
        return result

    raise ValueError(f"Неверный конфиг: '{config}'. Допустимы только 'A', 'B', 'C', 'D'.")


def process_csv_file(input_path: str, output_path: str, text_column: str, config: str, delimiter: str = ','):
    """
    читает csvшник, применяет функцию `preprocess` к выбранной колонке и записывает результат в новый csvшник
    """
    with open(input_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        fieldnames = reader.fieldnames
        new_fieldnames = list(fieldnames) + ['processed_text']
        rows = list(reader)

    for row in rows:
        text_to_process = row[text_column]
        tokens_list = preprocess(text_to_process, config=config)
        row['processed_text'] = " ".join(tokens_list)

    with open(output_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(rows)
