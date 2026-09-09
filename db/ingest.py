"""
Run this once (offline) to populate the knowledge_base table:
    python db/ingest.py

Steps: load cleaned data -> derive category/info_type metadata ->
fit+save the embedder -> compute embeddings -> create schema -> insert rows.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db.connection import get_connection
from embeddings.embedder import fit_and_save

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_base.json")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")
EMBEDDER_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "embedder.joblib")

GREETING_PATTERN = re.compile(
    r"^\s*(hi|hello|hey|hii+|yo|sup|wassup|greetings|good (morning|afternoon|evening))\b",
    re.IGNORECASE,
)


def categorize(prompt: str) -> str:
    """Heuristic category, derived from observed content patterns (this
    dataset has no pre-existing categories -- see README for reasoning)."""
    if GREETING_PATTERN.search(prompt):
        return "greeting"
    if "?" in prompt:
        return "question"
    return "statement"


def info_type(response_length: int) -> str:
    return "quick" if response_length < 200 else "detailed"


def main():
    with open(DATA_PATH, encoding="utf-8") as f:
        entries = json.load(f)

    for e in entries:
        # category now comes directly from data/generate_kb.py's authored labels
        e["prompt_length"] = len(e["prompt"])
        e["response_length"] = len(e["response"])
        e["info_type"] = info_type(e["response_length"])

    cat_counts = {}
    for e in entries:
        cat_counts[e["category"]] = cat_counts.get(e["category"], 0) + 1
    print("Category distribution:", cat_counts)

    print(f"Fitting embedder on {len(entries)} prompts...")
    embedder = fit_and_save([e["prompt"] for e in entries], EMBEDDER_PATH)
    embeddings = embedder.transform([e["prompt"] for e in entries])
    print(f"Saved embedder -> {EMBEDDER_PATH}")

    conn = get_connection()
    cur = conn.cursor()

    with open(SCHEMA_PATH) as f:
        cur.execute(f.read())
    conn.commit()
    print("Schema ensured.")

    cur.execute("TRUNCATE TABLE knowledge_base RESTART IDENTITY;")
    for e, vec in zip(entries, embeddings):
        cur.execute(
            """
            INSERT INTO knowledge_base
                (prompt, response, category, info_type, prompt_length, response_length, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                e["prompt"], e["response"], e["category"], e["info_type"],
                e["prompt_length"], e["response_length"], vec.tolist(),
            ),
        )
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM knowledge_base;")
    total = cur.fetchone()[0]
    print(f"Inserted. Total rows in knowledge_base: {total}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
