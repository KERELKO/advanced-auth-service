from dataclasses import dataclass

from src.core.exceptions import ApplicationException


@dataclass(eq=False, repr=False)
class InvalidCodeException(ApplicationException):
    code: str

    @property
    def msg(self) -> str:
        return f'Invalid code: {self.code}'
