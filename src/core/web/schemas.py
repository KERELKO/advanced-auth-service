from dataclasses import dataclass


@dataclass(eq=False, repr=False, slots=True)
class Token:
    value: str
    type: str = 'Bearer'
