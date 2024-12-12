# fmt: off
import typing as t
from abc import (
    ABC,
    abstractmethod,
)

from src.core.dto.users import ExternalUser


UT = t.TypeVar('UT', bound=ExternalUser)


class AbstractNotificationService(ABC):
    @abstractmethod
    async def send(
        self,
        message: str,
        subject: str,
        to: str,
    ) -> None:
        ...


class AbstractOAuthService(ABC, t.Generic[UT]):
    @abstractmethod
    async def get_user(self, code: str) -> UT:
        ...
