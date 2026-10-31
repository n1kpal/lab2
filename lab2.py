import pandas as pd

from reading_files import reading_files
from task5 import allConfigs
from serch import evaluate, write_errors

# Собирает DataFrame для serch.evaluate и serch.write_errors
def build_dataframes(docs_dict: dict, queries_dict: dict, relevance_dict: dict):
    docs_df = pd.DataFrame([{"document_id": did, "title": d["title"]} for did, d in docs_dict.items()])
    queries_df = pd.DataFrame([{"query_id": qid, "query": q["query"]} for qid, q in queries_dict.items()])
    dev_df = pd.DataFrame([{"query_id": qid, "relevant_document_id": did} for qid, dids in relevance_dict.items() for did in dids])
    return docs_df, queries_df, dev_df


# Загрузка и исследование корпуса
docs_dict, queries_dict, relevance_dict = reading_files("db/documents.csv", "db/queries.csv", "db/dev_relevance.csv",)

# Адаптация к существующим модулям:
docs_for_search = {did: f"{d['title']} {d['section']} {d['text']}" for did, d in docs_dict.items()}
queries_for_search = {qid: q["query"] for qid, q in queries_dict.items()}
docs_df, queries_df, dev_df = build_dataframes(docs_dict, queries_dict, relevance_dict)

# Прогон 4 конфигураций TF-IDF
all_results = allConfigs(docs_for_search, queries_for_search, searcher="tfidf")

# Метрики на 8 открытых запросах
print("\nМетрики на 8 открытых запросах")
metrics_df, places, relevance = evaluate(all_results, dev_df)
print(metrics_df.to_string(index=False))
metrics_df.to_csv("output/experiment_metrics.csv", index=False, encoding="utf-8-sig")

# Выбор лучшей конфигурации
best_cfg = metrics_df.sort_values(["mrr_at_5", "hit_at_5"], ascending=False).iloc[0]["configuration"]
print(f"\nЛучшая конфигурация: {best_cfg}")

# TOP-5 для всех 30 запросов (лучшая конфигурация)
rows = []
for qid, results in all_results[best_cfg].items():
    for rank, (doc_id, score) in enumerate(results[:5], start=1):
        rows.append({"query_id": qid, "rank": rank, "document_id": doc_id, "score": score})
pd.DataFrame(rows).to_csv("output/search_results.csv", index=False, encoding="utf-8-sig")

# Разбор ошибок (serch.write_errors)
write_errors("output/error_analysis.txt", all_results, places, relevance, queries_df, docs_df,)

# Baseline для сравнения
print("\nBaseline для сравнения")
baseline_results = allConfigs(docs_for_search, queries_for_search, searcher="baseline")
baseline_metrics, _, _ = evaluate(baseline_results, dev_df)
print(baseline_metrics.to_string(index=False))
