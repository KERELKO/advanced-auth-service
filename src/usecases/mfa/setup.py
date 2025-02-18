from dataclasses import dataclass

from src.core.dto.users import UpdateUserDTO, UserDTO
from src.core.storages.repositories.base import IUserRepository
from src.modules.mfa.service import MFAService
from src.modules.mfa.dto import UpdateUserMFA

from .. import UseCase


@dataclass(eq=False, repr=False, slots=True)
class SetupUserMFA(UseCase[UpdateUserMFA, UserDTO]):
    user_repository: IUserRepository
    mfa_service: MFAService

    async def __call__(self, dto: UpdateUserMFA) -> UserDTO:
        user = await self.user_repository.get(dto.user_id)

        user.mfa_enabled = dto.mfa_enabled
        user.mfa_type = dto.mfa_type
        if not user.mfa_secret:
            user.mfa_secret = self.mfa_service.generate_secret()

        update_dto = UpdateUserDTO(
            mfa_enabled=user.mfa_enabled,
            mfa_secret=user.mfa_secret,
            mfa_type=user.mfa_type,
        )
        updated_user = await self.user_repository.update(dto.user_id, update_dto)

        return updated_user
