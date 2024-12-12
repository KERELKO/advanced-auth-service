# fmt: off
from . import UseCase


class OAuthRegisterUser(UseCase[str, str]):
    async def __call__(self, dto: str) -> str:
        ...


class OAuthLogin(UseCase[str, str]):
    async def __call__(self, dto: str) -> str:
        ...
