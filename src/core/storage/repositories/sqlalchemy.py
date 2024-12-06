from dataclasses import asdict

import sqlalchemy as sa

from src.core.dto.permissions import AddPermissionDTO, PermissionDTO
from src.core.dto.users import AddUserDTO, UserDTO
from src.core.exceptions import NotFoundByFilters, ObjectDoesNotExist
from src.core.storage.orm.config import Database
from src.core.storage.orm.models import UserORM, PermissionORM
from src.core.utils import to_dto


class SQLAlchemyUserRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def get(self, id: int) -> UserDTO:
        async with self.db.session_factory() as session:
            user: UserORM | None = await session.get(UserORM, ident=id)
            if not user:
                raise ObjectDoesNotExist(id=id)
            return to_dto(UserDTO, user.to_dict())

    async def add(self, data: AddUserDTO) -> UserDTO:
        async with self.db.session_factory() as session:
            new_user = UserORM(**asdict(data))
            session.add(new_user)
            await session.commit()
            return to_dto(UserDTO, new_user.to_dict())

    async def get_by_username(self, username: str) -> UserDTO:
        stmt = sa.select(UserORM).where(UserORM.username == username)
        async with self.db.session_factory() as session:
            user = (await session.execute(stmt)).scalar_one_or_none()
            if not user:
                raise NotFoundByFilters(filters={'username': username})
            return to_dto(UserDTO, user.to_dict())


class SQLAlchemyPermissionRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def get_by_codename(self, codename: str) -> PermissionDTO:
        async with self.db.session_factory() as session:
            stmt = sa.select(PermissionORM).where(PermissionORM.codename == codename)
            permission = (await session.execute(stmt)).scalar_one_or_none()
            if not permission:
                raise NotFoundByFilters(filters={'codename': codename})
            return to_dto(PermissionDTO, permission.to_dict())

    async def get(self, id: int) -> PermissionDTO:
        async with self.db.session_factory() as session:
            permission: PermissionORM | None = await session.get(PermissionORM, ident=id)
            if not permission:
                raise ObjectDoesNotExist(id=id)
            return to_dto(PermissionDTO, permission.to_dict())

    async def add(self, data: AddPermissionDTO) -> PermissionDTO:
        async with self.db.session_factory() as session:
            permission = PermissionORM(**asdict(data))
            session.add(permission)
            await session.commit()
            return to_dto(PermissionDTO, permission.to_dict())
