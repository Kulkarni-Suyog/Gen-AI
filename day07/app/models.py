"""Record dataclass shared by ingest, search, RAG and the API."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields


@dataclass
class Record:
    id: int
    item_or_topic: str
    old_rule: str
    new_rule: str
    effective_from: str  # ISO date YYYY-MM-DD
    document: str
    source_url: str
    category: str = "General"
    topic: str = ""  # key used to find older/newer rules on the same subject
    doc_year: int = 0
    page: int | None = None
    verified: bool = True
    extra: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> "Record":
        names = {f.name for f in fields(cls)}
        clean = {k: v for k, v in d.items() if k in names}
        for required in ("id", "item_or_topic", "old_rule", "new_rule", "effective_from", "document", "source_url"):
            if clean.get(required) in (None, ""):
                raise ValueError(f"missing field: {required}")
        clean["id"] = int(clean["id"])
        if not clean.get("doc_year"):
            clean["doc_year"] = int(str(clean["effective_from"])[:4])
        if not clean.get("topic"):
            clean["topic"] = slugify(clean["item_or_topic"])
        return cls(**clean)

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def text(self) -> str:
        return (
            f"{self.item_or_topic}. Old rule: {self.old_rule}. "
            f"New rule: {self.new_rule}. Effective from {self.effective_from}."
        )


def slugify(text: str) -> str:
    out = "".join(c.lower() if c.isalnum() else "-" for c in text)
    return "-".join(p for p in out.split("-") if p)[:60]
