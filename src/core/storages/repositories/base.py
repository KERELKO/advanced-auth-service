# fmt: off
import abc
from src.core.dto import users, permissions
from src.modules.mfa.dto import AddMFACode


class IUserRepository:
    async def exists(self, user_id: int) -> bool:
        ...

    async def add(self, dto: users.AddUserDTO) -> users.UserDTO:
        ...

    async def get(self, id: int) -> users.UserDTO:
        ...

    async def get_by_username(self, username: str) -> users.UserDTO:
        ...

    async def update(self, user_id: int, dto: users.UpdateUserDTO) -> users.UserDTO:
        ...


class IPermissionRepository:
    async def get_by_codename(self, codename: str) -> permissions.PermissionDTO:
        ...

    async def get(self, id: int) -> permissions.PermissionDTO:
        ...

    async def get_by_user_id(self, user_id: int) -> list[permissions.PermissionDTO]:
        ...

    async def add(self, dto: permissions.AddPermissionDTO) -> permissions.PermissionDTO:
        ...


class AbstractCodeRepository(abc.ABC):
    @abc.abstractmethod
    async def get(self, user_id: int) -> AddMFACode:
        ...

    @abc.abstractmethod
    async def set(self, dto: AddMFACode, ttl: int):
        ...
