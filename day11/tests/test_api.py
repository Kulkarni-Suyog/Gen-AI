"""FastAPI endpoint tests. All external LLM calls are replaced with fakes."""
from fastapi.testclient import TestClient
from app import main

class ReadyCollection:
    def count(self):
        return 1

def client_with_fake_startup(monkeypatch):
    monkeypatch.setattr(main, "get_collection", lambda: ReadyCollection())
    return TestClient(main.app)

def test_health_endpoint(monkeypatch):
    with client_with_fake_startup(monkeypatch) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "day": 9}

def test_ask_endpoint_uses_fake_llm(monkeypatch):
    import sys
    import types
    from app import rag

    fake_llm = types.ModuleType("app.llm")
    fake_llm.generate_answer = lambda **kwargs: "The test LLM says the GST rate is 5%."
    monkeypatch.setitem(sys.modules, "app.llm", fake_llm)
    monkeypatch.setattr(
        rag,
        "search_chunks",
        lambda *args, **kwargs: [
            {
                "id": "4",
                "text": "Hair oil new GST rate 5%",
                "metadata": {
                    "record_id": "4",
                    "title": "Hair oil",
                    "source": "Test fixture",
                    "page": "1",
                    "source_url": "https://example.test/source",
                },
                "distance": 0.12,
            }
        ],
    )
    with client_with_fake_startup(monkeypatch) as client:
        response = client.post(
            "/ask",
            json={"question": "What is the GST rate on hair oil?", "top_k": 3, "config": "A"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "The test LLM says the GST rate is 5%."
    assert data["citations"][0]["record_id"] == "4"


def test_ask_endpoint_rejects_blank_question(monkeypatch):
    with client_with_fake_startup(monkeypatch) as client:
        response = client.post("/ask", json={"question": "   "})
    assert response.status_code == 400
    assert response.json()["detail"] == "Question cannot be empty"
