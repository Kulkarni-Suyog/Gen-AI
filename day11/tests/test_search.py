"""Tests for vector-store chunk configuration and retrieval."""
from app import vectorstore

class FakeCollection:
    def count(self):
        return 2

    def query(self, query_embeddings, n_results):
        assert query_embeddings == [[0.1, 0.2]]
        assert n_results == 2
        return {
            "ids": [["1", "2"]],
            "documents": [["shampoo GST rate", "soap GST rate"]],
            "metadatas": [[{"record_id": "1"}, {"record_id": "2"}]],
            "distances": [[0.1, 0.2]],
        }

class FakeClient:
    def get_or_create_collection(self, **kwargs):
        return FakeCollection()

def test_config_a_creates_one_chunk_per_record():
    chunks = vectorstore._chunks_for_config(
        [{"item_or_topic": "Shampoo"}, {"item_or_topic": "Soap"}], "A"
    )
    assert len(chunks) == 2

def test_config_b_is_supported():
    chunks = vectorstore._chunks_for_config(
        [{"item_or_topic": "Shampoo"}], "B"
    )
    assert len(chunks) == 1

def test_unknown_config_is_rejected():
    import pytest
    with pytest.raises(ValueError, match="config must be"):
        vectorstore._chunks_for_config([], "C")

def test_search_chunks_returns_retrieved_records(monkeypatch):
    monkeypatch.setattr(vectorstore.chromadb, "PersistentClient", lambda **kwargs: FakeClient())
    monkeypatch.setattr(vectorstore, "embed_texts", lambda texts: [[0.1, 0.2]])
    hits = vectorstore.search_chunks("shampoo", top_k=2, config="A")
    assert len(hits) == 2
    assert hits[0]["metadata"]["record_id"] == "1"
    assert hits[1]["distance"] == 0.2
