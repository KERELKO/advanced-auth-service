from dataclasses import asdict
from blacksheep import FromJSON, FromServices

from src.core.dto import UserOutDTO
from src.modules.authentication.dto import RegisterUserDTO
from src.modules.authentication.schemas import LoginUserSchema, LogoutUserSchema, RegisterUserSchema
from src.modules.authentication.service import AuthService


async def login_user(input: FromJSON[LoginUserSchema], service: FromServices[AuthService]): ...


async def logout_user(input: FromJSON[LogoutUserSchema], service: FromServices[AuthService]): ...


async def register_user(
    input: FromJSON[RegisterUserSchema],
    service: FromServices[AuthService],
):
    new_user = await service.value.register(RegisterUserDTO(**asdict(input.value)))
    return UserOutDTO(id=new_user.id, email=new_user.email, username=new_user.username)
