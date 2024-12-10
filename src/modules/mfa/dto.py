from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MFACode:
    user_id: int
    expires_at: int
    code: str
