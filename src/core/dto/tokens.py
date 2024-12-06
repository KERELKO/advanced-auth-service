from dataclasses import dataclass, field


@dataclass(eq=False)
class Token:
    value: str
    type: str = 'bearer'


@dataclass(eq=False, slots=True)
class TokenPayload:
    sub: str
    user_id: int
    exp: int
    permissions: list[str] = field(default_factory=list)
