-- Schema design reasoning (see README for full explanation):
-- - `embedding VECTOR(256)`: dense embedding column, dimension matches the
--   TF-IDF+SVD embedder's output size (see embeddings/embedder.py).
-- - `category` / `info_type`: metadata columns for filtering, derived
--   heuristically from content patterns during ingestion (see db/ingest.py).
-- - B-tree indexes on category/info_type support fast metadata filtering;
--   the vector index (HNSW, created separately after data load -- see
--   db/create_vector_index.py) supports fast approximate similarity search.
-- - Storing prompt_length/response_length as columns (not computed at query
--   time) makes length-based filtering/sorting cheap.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS knowledge_base (
    id              SERIAL PRIMARY KEY,
    prompt          TEXT NOT NULL,
    response        TEXT NOT NULL,
    category        VARCHAR(50)  NOT NULL,
    info_type       VARCHAR(20)  NOT NULL,
    prompt_length   INT NOT NULL,
    response_length INT NOT NULL,
    embedding       VECTOR(50),
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_kb_category  ON knowledge_base (category);
CREATE INDEX IF NOT EXISTS idx_kb_info_type ON knowledge_base (info_type);

-- Vector index (HNSW) is created separately in db/create_vector_index.py,
-- AFTER data is loaded -- ivfflat's clustering step in particular needs
-- representative data present to build a good index.
