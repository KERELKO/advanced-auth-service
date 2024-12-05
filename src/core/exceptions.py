from dataclasses import dataclass
import typing as t


class ApplicationException(Exception):
    @property
    def msg(self) -> str:
        return self.__str__()


@dataclass(eq=False)
class ObjectDoesNotExist(ApplicationException):
    id: int

    @property
    def msg(self) -> str:
        return f'Object with id "{self.id}" does not exist'


@dataclass(eq=False)
class NotFoundByFilters(ObjectDoesNotExist):
    filters: dict[str, t.Any]
    id: int = -1

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
