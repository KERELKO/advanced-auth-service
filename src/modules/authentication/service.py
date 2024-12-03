from src.core.dto import UserDTO
from src.core.storage.repositories.abstract import AbstractUserRepository

from .dto import LoginUserDTO, LogoutUserDTO, RegisterUserDTO


class AuthService:
    def __init__(self, repository: AbstractUserRepository) -> None:
        self.repo = repository

    async def login(self, data: LoginUserDTO) -> UserDTO: ...

    async def logout(self, data: LogoutUserDTO) -> UserDTO: ...

    async def register(self, data: RegisterUserDTO) -> UserDTO: ...
