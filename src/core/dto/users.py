from abc import abstractmethod
import datetime
from dataclasses import (
    dataclass,
    field,
)

from src.core.constants import OAuthProvider, MFAType
from src.core.dto.permissions import PermissionDTO


@dataclass(repr=True, slots=True, eq=False)
class UserDTO:
    id: int
    username: str
    email: str | None = None
    permissions: list[PermissionDTO] = field(default_factory=list)
    hashed_password: str | None = None

    mfa_enabled: bool = False
    mfa_secret: str | None = None
    mfa_type: MFAType | None = None

    oauth_provider: OAuthProvider | None = None
    oauth_provider_id: str | None = None

    updated_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __eq__(self, other: 'UserDTO') -> bool:
        return self.id == other.id


@dataclass(eq=False, repr=False, slots=True)
class AddUserDTO:
    username: str
    email: str | None = None
    hashed_password: str | None = None
    permissions: list[str] | None = None

    mfa_enabled: bool = False
    mfa_secret: str | None = None
    mfa_type: MFAType | None = None

    oauth_provider: OAuthProvider | None = None
    oauth_provider_id: str | None = None


@dataclass(eq=False, slots=True)
class UpdateUserDTO:
    username: str | None = None
    email: str | None = None

    permissions: list[str] | None = None
    hashed_password: str | None = None

    mfa_enabled: bool = False
    mfa_secret: str | None = None
    mfa_type: MFAType | None = None

    oauth_provider: OAuthProvider | None = None
    oauth_provider_id: str | None = None


@dataclass
class ExternalUser:
    id: str

    @abstractmethod
    def as_add_user_dto(self) -> AddUserDTO: ...
