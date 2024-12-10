from dataclasses import asdict

import sqlalchemy as sa
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.dto.permissions import (
    AddPermissionDTO,
    PermissionDTO,
)
from src.core.dto.users import (
    AddUserDTO,
    UpdateUserDTO,
    UserDTO,
)
from src.core.exceptions import (
    NotFoundByFilters,
    ObjectAlreadyExistsException,
    ObjectDoesNotExist,
)
from src.core.storages.db import Database
from src.core.storages.orm.models import (
    PermissionORM,
    UserORM,
)
from src.core.storages.orm.models.permissions import permission_user_table
from src.core.utils import to_dto


class SQLAlchemyUserRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def get(self, id: int) -> UserDTO:
        async with self.db.session_factory() as session:
            user = await self.__get_unique_user_by_id(id, session)
            if not user:
                raise ObjectDoesNotExist(id=id)
            return to_dto(UserDTO, user.to_dict())

    async def exists(self, user_id: int) -> bool:
        async with self.db.session_factory() as session:
            stmt = sa.select(UserORM).where(UserORM.id == user_id).limit(1)
            result = (await session.execute(stmt)).scalar_one_or_none()
            return True if result else False

    async def add(self, dto: AddUserDTO) -> UserDTO:
        async with self.db.session_factory() as session:
            stmt = sa.select(UserORM).where(UserORM.username == dto.username).limit(1)
            exists = (await session.execute(stmt)).scalar_one_or_none()
            if exists is not None:
                raise ObjectAlreadyExistsException({'username': dto.username})

            if dto.permissions:
                fetch_permissions_stmt = sa.select(PermissionORM).where(
                    PermissionORM.codename.in_(dto.permissions),
                )
                _permissions = (await session.execute(fetch_permissions_stmt)).scalars().all()
                if len(_permissions) != len(dto.permissions):
                    logger.warning(
                        'Some permissions do not exist: '
                        f'Stored permissions: {[p.codename for p in _permissions]}, '
                        f'Requested permissions: {[dto.permissions]}'
                    )
                dto.permissions = _permissions or None  # type: ignore

            values = {k: v for k, v in asdict(dto).items() if v is not None}
            user_orm = UserORM(**values)

            new_user = await session.merge(user_orm)
            await session.commit()
            logger.info(f'Added user: id={new_user.id}')
            return to_dto(UserDTO, new_user.to_dict())

    async def get_by_username(self, username: str) -> UserDTO:
        stmt = self.__construct_user_select().where(UserORM.username == username)
        async with self.db.session_factory() as session:
            user = (await session.execute(stmt)).unique().scalar_one_or_none()
            if not user:
                raise NotFoundByFilters(filters={'username': username})
            return to_dto(UserDTO, user.to_dict())

    # TODO: optimize
    async def update(self, user_id: int, dto: UpdateUserDTO) -> UserDTO:
        async with self.db.session_factory() as session:
            user = await self.__get_unique_user_by_id(user_id, session)
            if not user:
                raise ObjectDoesNotExist(id=user_id)

            if dto.permissions:
                fetch_permissions_stmt = sa.select(PermissionORM).where(
                    PermissionORM.codename.in_(dto.permissions),
                )
                permissions = (await session.execute(fetch_permissions_stmt)).scalars().all()
                if not user.permissions:
                    user.permissions = list(permissions)
                else:
                    user.permissions = list(set(user.permissions) | set(permissions))
                dto.permissions = None

            values = {k: v for k, v in asdict(dto).items() if v is not None}
            for field, value in values.items():
                if hasattr(user, field):
                    setattr(user, field, value)

            user_dto = to_dto(UserDTO, user.to_dict())
            await session.commit()
            logger.info(f'Updated user: id={user_dto.id}')
            return user_dto

    async def __get_unique_user_by_id(self, user_id: int, session: AsyncSession) -> UserORM | None:
        stmt = self.__construct_user_select().where(UserORM.id == user_id)
        return (await session.execute(stmt)).unique().scalar_one_or_none()

    def __construct_user_select(self, join_permissions: bool = True) -> sa.Select:
        stmt = sa.select(UserORM)
        return stmt.options(joinedload(UserORM.permissions)) if join_permissions else stmt


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

    async def get_by_user_id(self, user_id: int) -> list[PermissionDTO]:
        stmt = (
            sa.select(PermissionORM)
            .join(permission_user_table, onclause=permission_user_table.c['user_id'] == user_id)
            .distinct()
        )
        async with self.db.session_factory() as session:
            permissions = (await session.execute(stmt)).scalars().all()
            return [to_dto(PermissionDTO, p.to_dict()) for p in permissions]

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
            logger.info(f'Added permission: id={permission.id}, codename={permission.codename}')
            return to_dto(PermissionDTO, permission.to_dict())
