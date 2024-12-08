from src.core.config import Config
from src.core.dto.permissions import PermissionDTO
from src.core.storage.repositories.base import IPermissionRepository, IUserRepository
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
        return set(user.permissions) <= permissions

    async def get_user_permissions(self, user_id: int) -> list[PermissionDTO]:
        user = await self.user_repository.get(id=user_id) or not_found(id=user_id)
        return user.permissions
