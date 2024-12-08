from dataclasses import dataclass, field
import typing as t


class ApplicationException(Exception):
    @property
    def msg(self) -> str:
        return self.__str__()


@dataclass(eq=False)
class ObjectDoesNotExist(ApplicationException):
    id: t.Any

    @property
    def msg(self) -> str:
        return f'Object does not exist: {self.id}'


@dataclass(eq=False)
class ObjectAlreadyExistsException(ApplicationException):
    filters: dict[str, t.Any]

    @property
    def msg(self) -> str:
        return f'Object already exists: {self.filters}'


@dataclass(eq=False)
class NotFoundByFilters(ObjectDoesNotExist):
    id: int = -1
    filters: dict[str, t.Any] = field(kw_only=True)

    @property
    def msg(self) -> str:
        return f'Failed to find object with filters: {self.filters}'


@dataclass(eq=False)
class AccessDenied(ApplicationException):
    permission_codenames: list[str]
    user_id: int | None = None

    @property
    def msg(self) -> str:
        return f'Access denied: required permission: {self.permission_codenames}'


@dataclass(eq=False)
class InvalidTokenException(ApplicationException):
    token: str

    @property
    def msg(self) -> str:
        return 'Token is invalid'
