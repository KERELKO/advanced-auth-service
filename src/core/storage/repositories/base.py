import typing as t

from src.core.dto import users, permissions

CT = t.TypeVar('CT')
T = t.TypeVar('T')


class IUserRepository:
    async def add(self, dto: users.CreateUserDTO) -> users.UserDTO: ...

    async def get(self, id: int) -> users.UserDTO: ...


class IPermissionRepository:
    async def get_by_codename(self, codename: str) -> permissions.PermissionDTO: ...

    async def add(self, dto: permissions.CreatePermissionDTO) -> permissions.PermissionDTO: ...

    async def get(self, id: int) -> permissions.PermissionDTO: ...
