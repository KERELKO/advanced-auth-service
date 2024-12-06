from loguru import logger
import pytest

from src.modules.authentication.dto import LoginUserDTO, RegisterUserDTO
from src.modules.authentication.service import AuthenticationService
from tests import _container as container


async def test_can_register_and_login_user(register_user_dto: RegisterUserDTO) -> None:
    service = container.resolve(AuthenticationService)

    user_dto = await service.register(register_user_dto)
    logger.info(user_dto)
    assert user_dto.username == register_user_dto.username

    user_login_dto = LoginUserDTO(
        username=user_dto.username, password=register_user_dto.password,
    )

    access_token, refresh_token = await service.login(user_login_dto)
    logger.info(f'Tokens: {access_token}\n{refresh_token}')

    assert access_token.type == 'bearer'

    decoded_access_token = service._decode_token(access_token.value)
    logger.info(f'Decoded access token: {decoded_access_token}')

    assert decoded_access_token.username == register_user_dto.username
    assert decoded_access_token.exp

