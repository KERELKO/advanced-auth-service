from dataclasses import dataclass, field


@dataclass(eq=False, repr=False, slots=True)
class TokenPayload:
    user_id: int
    username: str
    permissions: set[str] = field(default_factory=set)
