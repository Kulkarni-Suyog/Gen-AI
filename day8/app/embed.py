"""Sentence-transformers semantic embedding helpers."""
from functools import lru_cache
from typing import List

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(MODEL_NAME)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Encode texts using a semantic embedding model (not hashed n-grams)."""
    if not texts:
        return []
    model = get_model()
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return vectors.tolist()
