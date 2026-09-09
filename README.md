# Intelligent Customer Assistant System

RAG-based customer service chatbot: PostgreSQL + pgvector for the knowledge
base, TF-IDF+SVD for embeddings, LangChain + Groq for generation, Streamlit
for the chat UI.

## Important note on the knowledge base data

The dataset originally provided for this assignment (`dataset_assignment.xlsx`,
9117 prompt/response rows) turned out, on inspection, to be a generic
public chatbot-interaction dataset -- not customer-service content, and
containing a meaningful amount of unsafe material (explicit content, and
at least one self-harm-related entry) mixed in among ordinary rows. Both
issues made it unsuitable to use directly, and keyword-based filtering
could not reliably guarantee everything unsafe was caught given how varied
and multilingual the raw data was.

**Decision: the knowledge base was rebuilt from scratch** as 85 originally
written, safe, on-topic customer-service FAQ entries covering exactly what
the brief specifies -- account/login, orders/shipping, payments/billing,
returns/refunds, technical troubleshooting, product info, and
contact/escalation (see `data/generate_kb.py`). This changes nothing about
the technical pipeline the assignment asks for (embeddings, pgvector,
RAG, Streamlit) -- only the data source.

## Architecture

```
User question (Streamlit chat input)
        |
        v
rag/chain.py -- answer()
        |
        +--> rag/retriever.py -- search()
        |         1. embed query with the saved TF-IDF+SVD embedder
        |         2. cosine similarity search in PostgreSQL/pgvector
        |         3. filter by similarity threshold (0.25)
        |         4. re-rank with a keyword-overlap boost (hybrid search)
        |         5. log query + top result to search_log.jsonl
        |
        +--> ChatGroq (openai/gpt-oss-120b via LangChain)
                  system prompt + retrieved context + user question
                  -> generated answer
```

## Database schema & indexing (reasoning)

See `db/schema.sql` for the DDL. Key decisions:
- `embedding VECTOR(50)`: dimension matches the embedder's output (50 --
  chosen because TruncatedSVD's component count must stay well under the
  corpus size; 85 documents comfortably supports 50 components without
  overfitting the decomposition).
- `category` / `info_type` columns (not just embeddings) support fast
  exact-match metadata filtering alongside semantic search.
- B-tree indexes on `category` / `info_type` for that filtering.
- **HNSW** was chosen as the production vector index over IVFFlat: HNSW
  doesn't need a training/clustering step (unlike IVFFlat's `lists`
  parameter, which needs tuning to the data size) and generally gives
  better recall at similar speed. See benchmark below for what this
  actually measured at this dataset's scale.

## Embedding model choice (reasoning)

**TF-IDF + Truncated SVD (LSA)**, entirely local -- no external embedding
API or pretrained-model download required (both are blocked in the
development sandbox this was built in, and requiring students' own API
keys just for embeddings would add unnecessary cost/complexity). Output
vectors are L2-normalized so cosine similarity reduces to a dot product.
Real semantic search test (see below) confirms this works well at this
knowledge base's scale and vocabulary.

Trade-off: TF-IDF+SVD captures lexical/topical similarity well but not
deep semantic paraphrase understanding the way a neural embedding model
(e.g. `text-embedding-3-small`, `nomic-embed-text`) would. For this
FAQ-matching use case (where user questions tend to share vocabulary with
their matching FAQ entry) it performs well in practice -- see example
queries below.

## Search quality (real test results)

```
Query: "gimana cara reset password saya?"
  [0.976] Saya lupa password, bagaimana cara reset?

Query: "aplikasi saya sering force close"
  [0.962] Aplikasi sering force close, apa solusinya?

Query: "saya mau retur barang yang rusak"
  [0.699] Bagaimana jika barang yang diterima tidak sesuai deskripsi?
```

## Benchmark: HNSW vs IVFFlat vs no index

Run yourself: `python benchmarks/benchmark_search.py`

```
Strategy                         Avg (ms)   Worst (ms)
No index (sequential scan)          0.172        2.818
HNSW                                0.150        0.378
IVFFlat (lists=10)                  0.171        0.429
```

Honest interpretation: at only 85 rows, average-case latency is similar
across all three -- HNSW/IVFFlat are *approximate* indexes designed to pay
off at large scale (thousands-millions of rows), and their benefit here is
modest. The one real signal: HNSW noticeably reduces **worst-case**
latency (0.38ms vs 2.8ms), suggesting more consistent tail latency even at
small scale. At production scale with a much larger knowledge base, the
gap between indexed and sequential-scan search would widen substantially.

## Setup

1. Install PostgreSQL 16 and the pgvector extension:
   ```
   sudo apt install postgresql-16 postgresql-16-pgvector
   sudo service postgresql start
   sudo -u postgres psql -c "CREATE USER icas_user WITH PASSWORD 'icas_dev_password';"
   sudo -u postgres psql -c "CREATE DATABASE customer_assistant OWNER icas_user;"
   sudo -u postgres psql -d customer_assistant -c "CREATE EXTENSION vector;"
   ```
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`, fill in `GROQ_API_KEY` (get one free at
   console.groq.com/keys). `DATABASE_URL` is already filled in to match
   step 1 above.
4. Ingest the knowledge base (creates schema, generates embeddings, loads
   data -- safe to re-run):
   ```
   python db/ingest.py
   ```
5. Run the chatbot:
   ```
   streamlit run app.py
   ```

## Testing

- `python benchmarks/benchmark_search.py` -- index performance comparison
- Retrieval logic (embedding, similarity search, threshold, hybrid
  ranking) can be exercised directly via `rag/retriever.py`'s `search()`
  function without needing a Groq API key, since it's pure
  Python + PostgreSQL with no LLM call involved.
- The RAG generation step (`rag/chain.py`) does need a real `GROQ_API_KEY`
  to actually produce answers -- that part could not be verified from the
  development sandbox this was built in (no network access to Groq's
  API there), so test it yourself once your key is set.

## Part 4: Video presentation

Not something code can produce for you -- record a short screen capture
of `streamlit run app.py` in action, and narrate: what the system does,
the architecture above, the retrieval-then-generation workflow, and a
couple of live example questions.
