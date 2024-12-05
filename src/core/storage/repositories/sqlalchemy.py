from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.dto import CreateUserDTO, UserDTO
from src.core.exceptions import ObjectDoesNotExist
from src.core.storage.orm.models.user import UserORM
from src.core.utils import to_dto

from .abstract import AbstractUserRepository


class SQLAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    async def get(self, id: int) -> UserDTO:
        async with self.session_factory() as session:
            user: UserORM | None = await session.get(UserORM, ident=id)
            if not user:
                raise ObjectDoesNotExist(id=id)
            return to_dto(UserDTO, user.to_dict())

    async def add(self, data: CreateUserDTO) -> UserDTO:
        async with self.session_factory() as session:
            new_user = UserORM(**asdict(data))
            session.add(new_user)
            await session.commit()
            return to_dto(UserDTO, new_user.to_dict())
