"""
Query processing pipeline for semantic search:
1. Embed the user's query with the same fitted embedder used at ingest time.
2. Run cosine-similarity search against pgvector (`<=>` operator = cosine distance).
3. Apply a similarity threshold to drop irrelevant matches.
4. Boost results that also share exact keyword overlap with the query
   (simple hybrid semantic + exact-match ranking).
5. Log every query + top result for basic analytics.
"""
import json
import os
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db.connection import get_connection
from embeddings.embedder import load_embedder

EMBEDDER_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "embedder.joblib")
LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "search_log.jsonl")

SIMILARITY_THRESHOLD = 0.25  # cosine similarity below this is considered irrelevant
EXACT_MATCH_BOOST = 0.05     # added to score per shared keyword with the query

_embedder = None


def _get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = load_embedder(EMBEDDER_PATH)
    return _embedder


def _keyword_overlap_boost(query: str, text: str) -> float:
    query_words = set(w.lower() for w in query.split() if len(w) > 3)
    text_words = set(w.lower() for w in text.split() if len(w) > 3)
    overlap = len(query_words & text_words)
    return overlap * EXACT_MATCH_BOOST


def search(query: str, top_k=3, category=None):
    embedder = _get_embedder()
    query_vec = embedder.transform([query])[0].tolist()

    conn = get_connection()
    cur = conn.cursor()

    sql = """
        SELECT id, prompt, response, category, info_type,
               1 - (embedding <=> %s::vector) AS similarity
        FROM knowledge_base
    """
    params = [query_vec]
    if category:
        sql += " WHERE category = %s"
        params.append(category)
    sql += " ORDER BY embedding <=> %s::vector LIMIT %s"
    params += [query_vec, top_k * 3]  # over-fetch, then re-rank with hybrid boost

    start = time.perf_counter()
    cur.execute(sql, params)
    rows = cur.fetchall()
    elapsed_ms = (time.perf_counter() - start) * 1000

    results = []
    for id_, prompt, response, cat, info_type, similarity in rows:
        boost = _keyword_overlap_boost(query, prompt)
        final_score = similarity + boost
        if similarity >= SIMILARITY_THRESHOLD:
            results.append({
                "id": id_, "prompt": prompt, "response": response,
                "category": cat, "info_type": info_type,
                "similarity": round(similarity, 4), "final_score": round(final_score, 4),
            })

    results.sort(key=lambda r: r["final_score"], reverse=True)
    results = results[:top_k]

    cur.close()
    conn.close()

    _log_query(query, results, elapsed_ms)
    return results, elapsed_ms


def _log_query(query, results, elapsed_ms):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "elapsed_ms": round(elapsed_ms, 2),
        "top_result_id": results[0]["id"] if results else None,
        "top_similarity": results[0]["similarity"] if results else None,
        "num_results": len(results),
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
