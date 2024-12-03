from src.core.dto import UpdateUserDTO, UserDTO

from .abstract import AbstractUserRepository


class SQLAlchemyUserRepository(AbstractUserRepository):
    async def get(self, id: int) -> UserDTO: ...

    async def update(self, id: int, data: UpdateUserDTO) -> UserDTO: ...

    async def remove(self, id: int) -> UserDTO: ...
