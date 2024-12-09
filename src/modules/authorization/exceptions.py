from dataclasses import dataclass
from src.core.exceptions import ApplicationException


class AuthorizationServiceException(ApplicationException): ...


@dataclass(eq=False)
class AccessDenied(AuthorizationServiceException):
    permission_codenames: list[str]
    user_id: int | None = None

    @property
    def msg(self) -> str:
        return f'Access denied: required permission: {self.permission_codenames}'
