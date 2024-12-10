import typing as t
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Code:
    value: str
    ttl: int


@dataclass
class MFARequired:
    user_id: str
    method: t.Literal['otp', 'sms'] = 'otp'
