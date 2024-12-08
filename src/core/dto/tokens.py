from dataclasses import dataclass, field


@dataclass
class Token:
    value: str
    type: str = 'bearer'

    def __eq__(self, other: 'Token') -> bool:
        return self.value == other.value


@dataclass(eq=False, slots=True)
class TokenPayload:
    sub: str
    user_id: int
    exp: int
    permissions: list[str] = field(default_factory=list)
