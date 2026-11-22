"""Day 13 - per-request latency + token logging, and a /metrics endpoint.

Put this file at app/observability.py. In app/main.py:

    from app import observability
    observability.install(app)

In app/llm.py, after each provider call, report the tokens:

    from app.observability import record_tokens
    record_tokens(prompt_tokens, completion_tokens)
"""
import contextvars
import json
import logging
import time
import uuid
from collections import deque

from fastapi import FastAPI, Request

log = logging.getLogger("gstsaral.requests")
if not log.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(_handler)
log.setLevel(logging.INFO)

SKIP_PATHS = {"/health", "/metrics", "/docs", "/openapi.json", "/redoc"}

# A mutable dict per request. Endpoints run in a thread pool, so we mutate this
# shared dict instead of setting a new context value.
_stats = contextvars.ContextVar("req_stats", default=None)
_history = deque(maxlen=1000)


def estimate_tokens(text: str) -> int:
    """Rough fallback (about 4 characters per token) when the provider gives no usage."""
    return max(1, len(text or "") // 4)


def record_tokens(prompt_tokens: int, completion_tokens: int) -> None:
    stats = _stats.get()
    if stats is not None:
        stats["prompt_tokens"] += int(prompt_tokens)
        stats["completion_tokens"] += int(completion_tokens)


def mark_cache_hit() -> None:
    stats = _stats.get()
    if stats is not None:
        stats["cache_hit"] = True


def reset() -> None:
    _history.clear()


def _percentile(sorted_values, pct):
    if not sorted_values:
        return 0.0
    index = min(len(sorted_values) - 1, round(pct / 100 * (len(sorted_values) - 1)))
    return round(sorted_values[index], 1)


def summary() -> dict:
    rows = list(_history)
    latencies = sorted(r["latency_ms"] for r in rows)
    hits = sum(1 for r in rows if r["cache_hit"])
    return {
        "requests": len(rows),
        "p50_ms": _percentile(latencies, 50),
        "p95_ms": _percentile(latencies, 95),
        "prompt_tokens": sum(r["prompt_tokens"] for r in rows),
        "completion_tokens": sum(r["completion_tokens"] for r in rows),
        "cache_hit_rate": round(hits / len(rows), 3) if rows else 0.0,
        "errors": sum(1 for r in rows if r["status"] >= 400),
    }


def install(app: FastAPI) -> None:
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        stats = {"prompt_tokens": 0, "completion_tokens": 0, "cache_hit": False}
        token = _stats.set(stats)
        start = time.perf_counter()
        status = 500
        try:
            response = await call_next(request)
            status = response.status_code
            response.headers["X-Latency-ms"] = str(
                round((time.perf_counter() - start) * 1000, 1)
            )
            return response
        finally:
            row = {
                "id": uuid.uuid4().hex[:8],
                "path": request.url.path,
                "method": request.method,
                "status": status,
                "latency_ms": round((time.perf_counter() - start) * 1000, 1),
                **stats,
            }
            if request.url.path not in SKIP_PATHS:
                _history.append(row)
                log.info(json.dumps(row))
            _stats.reset(token)

    @app.get("/metrics")
    def metrics():
        return summary()
