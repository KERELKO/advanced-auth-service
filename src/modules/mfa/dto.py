from dataclasses import dataclass


@dataclass(frozen=True)
class Code:
    value: str
