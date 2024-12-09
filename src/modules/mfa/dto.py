from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Code:
    value: str
    ttl: int
