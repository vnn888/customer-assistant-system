"""
Simple benchmarking comparing vector search strategies, as required by the
brief. Creates each index type, times N repeated queries, then moves on.

Honest note on interpreting results at this scale: HNSW/IVFFlat are
*approximate* nearest-neighbor indexes designed to pay off at large scale
(thousands-millions of vectors). With only ~85 rows, a brute-force
sequential scan can legitimately be just as fast or faster -- the ANN
indexes carry setup/traversal overhead that only pays off once a table is
too large to scan every row per query. This script reports what actually
happens at this dataset's scale rather than assuming index > no-index.
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db.connection import get_connection
from embeddings.embedder import load_embedder

EMBEDDER_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "embedder.joblib")
TEST_QUERIES = [
    "gimana cara reset password saya?",
    "berapa lama pengiriman ke luar kota?",
    "aplikasi saya sering force close",
    "saya mau retur barang yang rusak",
    "metode pembayaran apa saja yang ada?",
    "cara menghubungi customer service",
    "apakah produk yang dijual asli?",
    "bagaimana kebijakan privasi data saya?",
]
REPEATS = 20  # per query, to get a stable average


def time_queries(conn, query_vectors):
    cur = conn.cursor()
    times = []
    for vec in query_vectors:
        for _ in range(REPEATS):
            start = time.perf_counter()
            cur.execute(
                "SELECT id FROM knowledge_base ORDER BY embedding <=> %s::vector LIMIT 3",
                (vec,),
            )
            cur.fetchall()
            times.append((time.perf_counter() - start) * 1000)
    cur.close()
    return sum(times) / len(times), max(times)


def main():
    embedder = load_embedder(EMBEDDER_PATH)
    query_vectors = [embedder.transform([q])[0].tolist() for q in TEST_QUERIES]

    conn = get_connection()
    cur = conn.cursor()

    results = {}

    # 1. No index (drop any vector index, forces sequential scan)
    cur.execute("DROP INDEX IF EXISTS idx_kb_embedding_hnsw;")
    cur.execute("DROP INDEX IF EXISTS idx_kb_embedding_ivfflat;")
    conn.commit()
    avg, worst = time_queries(conn, query_vectors)
    results["No index (sequential scan)"] = (avg, worst)

    # 2. HNSW
    cur.execute("CREATE INDEX idx_kb_embedding_hnsw ON knowledge_base USING hnsw (embedding vector_cosine_ops);")
    conn.commit()
    avg, worst = time_queries(conn, query_vectors)
    results["HNSW"] = (avg, worst)
    cur.execute("DROP INDEX idx_kb_embedding_hnsw;")
    conn.commit()

    # 3. IVFFlat (lists=10, reasonable for a small table)
    cur.execute("CREATE INDEX idx_kb_embedding_ivfflat ON knowledge_base USING ivfflat (embedding vector_cosine_ops) WITH (lists = 10);")
    conn.commit()
    avg, worst = time_queries(conn, query_vectors)
    results["IVFFlat (lists=10)"] = (avg, worst)

    # Keep HNSW as the final production index (best balance of speed/recall
    # generally; see README for reasoning), IVFFlat index left for reference.
    cur.execute("DROP INDEX IF EXISTS idx_kb_embedding_ivfflat;")
    cur.execute("CREATE INDEX idx_kb_embedding_hnsw ON knowledge_base USING hnsw (embedding vector_cosine_ops);")
    conn.commit()

    cur.close()
    conn.close()

    print(f"\nBenchmark: {len(TEST_QUERIES)} queries x {REPEATS} repeats each, knowledge_base has 85 rows\n")
    print(f"{'Strategy':<30} {'Avg (ms)':>10} {'Worst (ms)':>12}")
    for name, (avg, worst) in results.items():
        print(f"{name:<30} {avg:>10.3f} {worst:>12.3f}")


if __name__ == "__main__":
    main()
