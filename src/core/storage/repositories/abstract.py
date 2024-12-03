from abc import ABC, abstractmethod

from src.core.dto import UpdateUserDTO, UserDTO


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get(self, id: int) -> UserDTO: ...

    @abstractmethod
    async def update(self, id: int, data: UpdateUserDTO) -> UserDTO: ...

    @abstractmethod
    async def remove(self, id: int) -> UserDTO: ...
