from dataclasses import asdict

from src.core.dto.user import CreateUserDTO, UserDTO
from src.core.security import SecurityService
from src.core.storage.repositories.base import IUserRepository

from .dto import LoginUserDTO, RegisterUserDTO


class AuthService:
    def __init__(
        self,
        repository: IUserRepository,
        security_service: SecurityService,
    ) -> None:
        self.repo = repository
        self.__security_service = security_service

    async def login(self, dto: LoginUserDTO) -> UserDTO: ...

    async def register(self, dto: RegisterUserDTO) -> UserDTO:
        hashed_password = self.__security_service.get_password_hash(dto.password)
        data = asdict(dto)
        data.pop('password')
        data['hashed_password'] = hashed_password
        return await self.repo.add(CreateUserDTO(**data))
