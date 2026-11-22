"""Day 13 - a small in-memory cache with TTL and a size limit.

Put this file at app/cache.py.
"""
import hashlib
import re
import time
from collections import OrderedDict
from threading import Lock


class TTLCache:
    def __init__(self, max_items: int = 256, ttl_seconds: float = 600):
        self.max_items = max_items
        self.ttl = ttl_seconds
        self._data = OrderedDict()  # key -> (expires_at, value)
        self._lock = Lock()
        self.hits = 0
        self.misses = 0

    @staticmethod
    def make_key(*parts) -> str:
        """Same question with different case or spacing gives the same key."""
        text = "|".join(re.sub(r"\s+", " ", str(p)).strip().lower() for p in parts)
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def get(self, key: str):
        with self._lock:
            item = self._data.get(key)
            if item is None or item[0] < time.monotonic():
                self._data.pop(key, None)
                self.misses += 1
                return None
            self._data.move_to_end(key)
            self.hits += 1
            return item[1]

    def set(self, key: str, value) -> None:
        with self._lock:
            self._data[key] = (time.monotonic() + self.ttl, value)
            self._data.move_to_end(key)
            while len(self._data) > self.max_items:
                self._data.popitem(last=False)

    def clear(self) -> None:
        with self._lock:
            self._data.clear()
            self.hits = self.misses = 0


# Shared instance used by /ask and /chat
answer_cache = TTLCache(max_items=256, ttl_seconds=600)
