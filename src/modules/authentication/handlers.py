from blacksheep import FromServices

from src.modules.authentication.dto import LoginUserDTO, LogoutUserDTO, RegisterUserDTO
from src.modules.authentication.service import AuthService


async def login(input: LoginUserDTO, service: FromServices[AuthService]): ...


async def logout(input: LogoutUserDTO, service: FromServices[AuthService]): ...


async def register(input: RegisterUserDTO, service: FromServices[AuthService]): ...
