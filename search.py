def relevant_place(results, relevant_ids):
    # место (с 1) первого релевантного документа в топ-5, 0 - если его там нет
    for place, (doc_id, _) in enumerate(results[:K], start=1):
        if doc_id in relevant_ids:
            return place
    return 0


def evaluate(all_results, dev):
    relevance = {}
    for qid, did in zip(dev["query_id"].astype(str), dev["relevant_document_id"].astype(str)):
        relevance.setdefault(qid, set()).add(did)

    rows, places = [], {}
    for cfg in CONFIGS:
        places[cfg] = {}
        for qid, rel in relevance.items():  # только 8 размеченных запросов
            places[cfg][qid] = relevant_place(all_results[cfg].get(qid, []), rel)
        p = list(places[cfg].values())
        rows.append({
            "configuration": cfg,
            "hit_at_5": sum(1 for x in p if x > 0) / len(p),
            "mrr_at_5": sum(1 / x for x in p if x > 0) / len(p),
        })
    return pd.DataFrame(rows), places, relevance


def write_errors(path, all_results, places, relevance, queries, docs):
    qtext = dict(zip(queries["query_id"].astype(str), queries["query"]))
    title = dict(zip(docs["document_id"].astype(str), docs["title"]))
    with open(path, "w", encoding="utf-8") as f:
        for cfg in CONFIGS:
            for qid, place in places[cfg].items():
                if place == 1:
                    continue  # ошибка = релевантный документ не на первом месте
                f.write(f"Конфигурация {cfg}, запрос {qid}: {qtext.get(qid)}\n")
                f.write("  Эталон: " + ", ".join(f"{d} ({title.get(d)})" for d in relevance[qid]) + "\n")
                f.write(f"  Место эталона в топ-5: {place if place else 'не найден'}\n")
                for i, (d, s) in enumerate(all_results[cfg][qid], start=1):
                    mark = "  <-- релевантный" if d in relevance[qid] else ""
                    f.write(f"    {i}. {d} ({title.get(d)}) score={s:.4f}{mark}\n")
                f.write("  Причина: \n\n")