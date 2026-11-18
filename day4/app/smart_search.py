"""TF-IDF and cosine-similarity search for GSTSaral records."""
from __future__ import annotations

from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

TEXT_FIELDS = ("item_or_topic", "old_rule", "new_rule", "effective_from", "document")


def _record_text(record: dict[str, Any]) -> str:
    return " ".join(str(record.get(field, "")) for field in TEXT_FIELDS)


def smart_search(records: list[dict[str, Any]], query: str, limit: int = 5) -> list[dict[str, Any]]:
    """Return the most relevant records, with a similarity score."""
    query = query.strip()
    if not query or not records:
        return []

    documents = [_record_text(record) for record in records]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    try:
        matrix = vectorizer.fit_transform(documents + [query])
    except ValueError:
        return []

    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    ranked_indices = scores.argsort()[::-1][:max(1, limit)]
    results = []
    for index in ranked_indices:
        score = float(scores[index])
        if score <= 0:
            continue
        item = dict(records[int(index)])
        item["record_id"] = int(index) + 1
        item["similarity"] = round(score, 4)
        results.append(item)
    return results
