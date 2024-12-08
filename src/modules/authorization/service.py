from loguru import logger

from src.core.config import Config
from src.core.dto.permissions import AddPermissionDTO, PermissionDTO
from src.core.dto.users import (
    UpdateUserDTO,
    UserDTO,
)
from src.core.storage.repositories.base import (
    IPermissionRepository,
    IUserRepository,
)
from src.core.utils import not_found


class AuthorizationService:
    def __init__(
        self,
        config: Config,
        user_repository: IUserRepository,
        permission_repository: IPermissionRepository,
    ) -> None:
        self._config = config
        self.user_repository = user_repository
        self.permission_repository = permission_repository

    async def has_permissions(self, user_id: int, permissions: set[str]) -> bool:
        """Check if user with specific id has set of required permissions
        * `permissions: set[str]` - permissions codenames
        """
        user = await self.user_repository.get(id=user_id) or not_found(id=user_id)
        user_permissions = {p.codename for p in user.permissions}
        if bool(user_permissions) and user_permissions <= permissions:
            logger.info(f'User with id "{user_id}" has required permissions from the set')
            return True
        else:
            logger.info(f'Lack for permissions for the user with id "{user_id}"')
            return False

    async def get_user_permissions(self, user_id: int) -> list[PermissionDTO]:
        user = await self.user_repository.get(id=user_id) or not_found(id=user_id)
        logger.info(f'Retieved user permissions: {[p.codename for p in user.permissions]}')
        return user.permissions

    async def register_permission(self, dto: AddPermissionDTO) -> PermissionDTO:
        permission = await self.permission_repository.add(dto)
        logger.info(f'Registed new permission: id={permission.id}, codename={permission.codename}')
        return permission

    async def grant_permissions(self, user_id: int, permissions: set[str]) -> UserDTO:
        if await self.user_repository.exists(user_id) is False:
            not_found(id=user_id)
        dto = UpdateUserDTO(permissions=list(permissions))
        updated_user = await self.user_repository.update(user_id, dto=dto)
        logger.info(f'Granted permissions for the user with id "{user_id}"')
        return updated_user
