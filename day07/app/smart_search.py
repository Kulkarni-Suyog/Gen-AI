"""TF-IDF + cosine ranking over GSTSaral records (powers /search)."""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.embed import _stem
from app.records import load_records

STOP = None


class SmartSearch:
    def __init__(self, records: list[dict] | None = None):
        self.records = records if records is not None else load_records()
        self.vec = TfidfVectorizer(preprocessor=lambda t: _stem(t), stop_words=STOP, ngram_range=(1, 2), sublinear_tf=True)
        docs = [self._doc(r) for r in self.records]
        self.matrix = self.vec.fit_transform(docs)

    @staticmethod
    def _doc(r: dict) -> str:
        return f"{r['item_or_topic']} {r.get('category', '')} {r['old_rule']} {r['new_rule']}"

    def rank(self, query: str, k: int = 5) -> list[dict]:
        if not query.strip():
            return []
        q = self.vec.transform([query])
        sims = cosine_similarity(q, self.matrix).ravel()
        order = sims.argsort()[::-1][:k]
        return [{**self.records[i], "score": round(float(sims[i]), 4)} for i in order if sims[i] > 0]


_default: SmartSearch | None = None


def smart_search(query: str, k: int = 5) -> list[dict]:
    global _default
    if _default is None:
        _default = SmartSearch()
    return _default.rank(query, k)
