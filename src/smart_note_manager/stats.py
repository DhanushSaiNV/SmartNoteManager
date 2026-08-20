from dataclasses import dataclass, field

@dataclass
class Stats:
    total_notes: int = 0
    tags_used: list[str] = field(default_factory=list)
    oldest_note: dict = field(default_factory=dict)

