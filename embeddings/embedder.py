"""
Embedding model choice & reasoning (full writeup in README):
TF-IDF + Truncated SVD (a.k.a. LSA - Latent Semantic Analysis) turns text
into dense, fixed-size vectors entirely locally -- no external embedding
API or pretrained-model download needed. Output is L2-normalized so cosine
similarity (via pgvector's vector_cosine_ops) reduces to a dot product.
"""
import joblib
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer

EMBEDDING_DIM = 50


def build_embedder(n_components=EMBEDDING_DIM):
    return Pipeline([
        ("tfidf", TfidfVectorizer(max_features=20000, stop_words=None)),
        ("svd", TruncatedSVD(n_components=n_components, random_state=42)),
        ("normalize", Normalizer(copy=False)),
    ])


def fit_and_save(texts, path):
    embedder = build_embedder()
    embedder.fit(texts)
    joblib.dump(embedder, path)
    return embedder


def load_embedder(path):
    return joblib.load(path)
