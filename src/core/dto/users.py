from dataclasses import dataclass, field
import datetime


@dataclass(eq=False, repr=False, slots=True)
class UserDTO:
    id: int
    username: str
    email: str | None = None
    permissions: list[str] = field(default_factory=list)
    hashed_password: str | None = None

    mfa_enabled: bool = False
    mfa_secret: str | None = None

    oauth_provider: str | None = None
    oauth_provider_id: str | None = None

    updated_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)


@dataclass(eq=False, repr=False, slots=True)
class AddUserDTO:
    username: str
    email: str | None = None
    hashed_password: str | None = None


@dataclass(eq=False, repr=False, slots=True)
class UserOutDTO:
    id: int
    username: str
    email: str | None


@dataclass(eq=False, repr=False, slots=True)
class UpdateUserDTO:
    username: str | None = None
    email: str | None = None
    permissions: set[str] = field(default_factory=set)
