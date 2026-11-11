"""Day 4 S2 - rank GSTSaral records with TF-IDF + cosine similarity."""

import re

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STOP = set(ENGLISH_STOP_WORDS)


def tokenize(text):
    """lowercase words, drop stop words, strip a plural 's' (notebooks -> notebook)."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w
            for w in words if w not in STOP]


FIELDS = ("item_or_topic", "category", "old_rule", "new_rule")


def _text(record):
    return " ".join(str(record.get(f, "")) for f in FIELDS)


class SmartSearch:
    def __init__(self, records):
        self.records = records
        self.vectorizer = TfidfVectorizer(
            tokenizer=tokenize, lowercase=False, token_pattern=None, ngram_range=(1, 2)
        )
        self.matrix = None
        if records:
            self.matrix = self.vectorizer.fit_transform([_text(r) for r in records])

    def search(self, query, top_k=5):
        """Return [(record, score)] best first; zero-score hits are dropped."""
        query = (query or "").strip()
        if not query or self.matrix is None:
            return []
        scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix)[0]
        ranked = sorted(zip(self.records, scores), key=lambda x: x[1], reverse=True)
        return [(r, round(float(s), 4)) for r, s in ranked[:top_k] if s > 0]
