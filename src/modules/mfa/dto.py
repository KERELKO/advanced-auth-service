import typing as t
from dataclasses import dataclass

from src.core.dto.users import UserDTO


@dataclass(frozen=True, slots=True)
class AddMFACode:
    user_id: int
    expires_at: int
    code: str


@dataclass(slots=True, eq=False)
class MFARequired:
    user: UserDTO
    mfa_type: t.Literal['sms', 'otp', 'all', 'code'] = 'otp'


@dataclass(slots=True, eq=False)
class MFACode:
    user_id: int
    code: str
    mfa_type: t.Literal['sms', 'otp', 'all', 'code'] = 'otp'


@dataclass(slots=True, eq=False)
class UpdateUserMFA:
    user_id: int
    mfa_enabled: bool
    mfa_secret: str | None = None
    mfa_type: t.Literal['sms', 'otp', 'all', 'code'] = 'otp'
