
# app/models.py

from dataclasses import dataclass, asdict


@dataclass
class Record:

    item_or_topic: str
    old_rule: str
    new_rule: str
    effective_from: str
    document: str
    source_url: str

    def to_dict(self):
        return asdict(self)
