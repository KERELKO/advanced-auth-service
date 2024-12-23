from loguru import logger

from src.core.config import Config
from src.core.dto.permissions import AddPermissionDTO, PermissionDTO
from src.core.dto.users import (
    UpdateUserDTO,
    UserDTO,
)
from src.core.storages.repositories.base import (
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
        self.default_permission_set = list(config.default_permission_set)
        self.user_repository = user_repository
        self.permission_repository = permission_repository

    async def has_permissions(self, user_id: int, permissions: set[str]) -> bool:
        """Check if user with specific id has set of required permissions
        * `permissions: set[str]` - permissions codenames
        """
        user = await self.user_repository.get(id=user_id) or not_found(id=user_id)
        user_permissions = {p.codename for p in user.permissions}
        if bool(user_permissions) and user_permissions <= permissions:
            logger.info(
                f'User with id={user_id} has sufficient permissions. '
                f'Required: {permissions}, Provided: {user_permissions}'
            )
            return True
        else:
            logger.warning(
                f'User with id={user_id} lacks sufficient permissions. '
                f'Required: {permissions}, Provided: {user_permissions}'
            )
            return False

    async def get_user_permissions(self, user_id: int) -> list[PermissionDTO]:
        """Return all permissions for the specific user"""
        user = await self.user_repository.get(id=user_id) or not_found(id=user_id)
        logger.info(f'User permission set (id={user_id}): {[p.codename for p in user.permissions]}')
        return user.permissions

    async def register_permission(self, dto: AddPermissionDTO) -> PermissionDTO:
        """Register new permission"""
        permission = await self.permission_repository.add(dto)
        logger.info(f'Registed new permission: id={permission.id}, codename={permission.codename}')
        return permission

    async def grant_permissions(self, user_id: int, permissions: set[str]) -> UserDTO:
        """Grant permissions for the user"""
        if await self.user_repository.exists(user_id) is False:
            not_found(id=user_id)
        dto = UpdateUserDTO(permissions=list(permissions))
        updated_user = await self.user_repository.update(user_id, dto=dto)
        logger.info(f'Granted permissions for the user: id={user_id}, permissions={permissions}')
        return updated_user
