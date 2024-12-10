# fmt: off
from dataclasses import dataclass

from src.core.exceptions import ApplicationException


class MFAException(ApplicationException):
    ...


@dataclass(eq=False, repr=False)
class InvalidCodeException(MFAException):
    code: str

    @property
    def msg(self) -> str:
        return f'Invalid code: {self.code}'


@dataclass(eq=False, repr=False)
class InvalidSecretKeyException(MFAException):
    secret: str | None

    @property
    def msg(self) -> str:
        return f'Invalid MFA secret key: {self.secret}'
