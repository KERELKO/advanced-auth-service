from dataclasses import asdict
from blacksheep import FromJSON, FromServices, Response, json

from loguru import logger
from src.core.dto import UserOutDTO
from src.core.utils import to_dto
from src.modules.authentication.dto import RegisterUserDTO
from src.modules.authentication.schemas import LoginUserSchema, LogoutUserSchema, RegisterUserSchema
from src.modules.authentication.service import AuthService


async def login_user(input: FromJSON[LoginUserSchema], service: FromServices[AuthService]): ...


async def logout_user(input: FromJSON[LogoutUserSchema], service: FromServices[AuthService]): ...


async def register_user(
    input: FromJSON[RegisterUserSchema],
    service: FromServices[AuthService],
) -> Response:
    new_user = await service.value.register(RegisterUserDTO(**asdict(input.value)))
    logger.info(f'Registered new user {new_user.username}:{new_user.id}')
    return json(to_dto(UserOutDTO, asdict(new_user)), status=201)
