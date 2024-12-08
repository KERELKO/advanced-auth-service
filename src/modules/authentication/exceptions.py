# fmt: off
from src.core.exceptions import ApplicationException


class AuthServiceException(ApplicationException):
    ...


class IncorrectPasswordException(AuthServiceException):
    ...


class TokenExpiredException(AuthServiceException):
    ...
