"""Offline, deterministic text embeddings (hashed word n-grams, L2-normalised).

No model download needed, so tests and Docker builds work without internet.
Swap `embed_texts` for a sentence-transformers model later if you want better semantics.
"""

from __future__ import annotations

import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, HashingVectorizer

DIM = 4096
EXTRA_STOP = {"gst", "rate", "rates", "tax", "taxes", "taxed", "taxable", "india", "indian", "applicable", "apply", "applies", "need", "pay", "much", "new", "old", "rule", "effective", "current", "now", "still"}
STOP = list(ENGLISH_STOP_WORDS | EXTRA_STOP)

_vec = HashingVectorizer(
    n_features=DIM,
    ngram_range=(1, 2),
    alternate_sign=False,
    norm="l2",
    stop_words=STOP,
    lowercase=True,
)


SYNONYMS = {
    "tv": "television", "tvs": "television", "ac": "air-conditioning", "acs": "air-conditioning",
    "cycle": "bicycle", "cycles": "bicycle", "diaper": "napkins diapers", "diapers": "napkins diapers",
    "notebook": "exercise books notebooks", "notebooks": "exercise books notebooks", "copy": "exercise books notebooks",
    "pencil": "pencils", "shampoo": "hair oil shampoo", "ghee": "butter ghee", "milk": "uht milk",
    "chapati": "roti chapathi", "chapatti": "roti chapathi", "bread": "roti paratha indian breads",
    "utensil": "kitchenware utensils", "utensils": "kitchenware utensils", "bhujia": "namkeen bhujia",
}


def _stem(text: str) -> str:
    """Tiny plural stemmer so 'soaps' matches 'soap'."""
    out = []
    for w in text.lower().split():
        w = w.strip(".,?!:;()'\"")
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        out.append(SYNONYMS.get(w, w))
    return " ".join(out)


def embed_texts(texts: list[str]) -> list[list[float]]:
    mat = _vec.transform([_stem(t) for t in texts])
    return mat.toarray().astype(np.float32).tolist()


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]
