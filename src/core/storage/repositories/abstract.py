from abc import ABC, abstractmethod

from src.core.dto import CreateUserDTO, UserDTO


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get(self, id: int) -> UserDTO: ...

    @abstractmethod
    async def add(self, data: CreateUserDTO) -> UserDTO: ...
