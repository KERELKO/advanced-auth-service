from dataclasses import dataclass, field


@dataclass(eq=False)
class Token:
    value: str
    type: str = 'bearer'


@dataclass(eq=False, repr=False, slots=True)
class TokenPayload:
    user_id: int
    username: str
    permissions: set[str] = field(default_factory=set)
