"""Data models used by GSTSaral."""

from dataclasses import asdict, dataclass


@dataclass
class Record:
    item_or_topic: str
    old_rule: str
    new_rule: str
    effective_from: str
    document: str
    source_url: str

    def to_dict(self) -> dict:
        """Convert this record into a JSON-serializable dictionary."""
        return asdict(self)
