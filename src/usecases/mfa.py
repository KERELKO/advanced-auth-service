from dataclasses import dataclass
import datetime

from src.core.dto.tokens import Token
from src.core.dto.users import UpdateUserDTO, UserDTO
from src.core.services.notifications import EmailNotificationService
from src.core.storages.repositories.base import AbstractCodeRepository, IUserRepository
from src.modules.authentication import AuthenticationService
from src.modules.mfa.service import MFAService
from src.modules.mfa.dto import AddMFACode, MFACode, UpdateUserMFA
from src.modules.mfa.exceptions import InvalidCodeException, MFAException

from . import UseCase


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


@dataclass(eq=False, repr=False, slots=True)
class SendMFACode(UseCase[UserDTO, MFACode]):
    code_repository: AbstractCodeRepository
    notification_service: EmailNotificationService
    mfa_service: MFAService

    async def __call__(self, dto: UserDTO) -> MFACode:
        # TODO
        # Better to separate notifications services
        # to handle sending codes by phone number or email, etc.
        if dto.mfa_type != 'code':
            raise MFAException('Cannot send MFA code if "mfa_type" is not "code"')

        if not dto.mfa_secret:
            raise MFAException(
                'User enabled MFA, but setup is incorrect: "mfa_secret" is not provided'
            )

        if not dto.email:
            raise MFAException('User enabled MFA, but setup is incorrect: "email" is not provided')

        code = self.mfa_service.generate_one_time_password(dto.mfa_secret)
        code_expires_at = int(
            (datetime.datetime.now() + datetime.timedelta(seconds=15 * 60)).timestamp()
        )

        await self.code_repository.set(
            AddMFACode(dto.id, expires_at=code_expires_at, code=code), ttl=15 * 60
        )

        message = f'Your verification code: {code}'

        await self.notification_service.send(message=message, to=dto.email, subject=dto.username)

        return MFACode(user_id=dto.id, code=code, mfa_type=dto.mfa_type)


@dataclass(eq=False, repr=False, slots=True)
class LoginUserMFA(UseCase[MFACode, tuple[Token, Token]]):
    authentication_service: AuthenticationService
    user_repository: IUserRepository
    mfa_service: MFAService

    async def __call__(self, dto: MFACode) -> tuple[Token, Token]:
        user = await self.user_repository.get(id=dto.user_id)

        if user.mfa_type != dto.mfa_type:
            raise MFAException("MFA types din't match")

        if user.mfa_type == 'code':
            if not await self.mfa_service.check_storage_code(user.id, dto.code):
                raise InvalidCodeException(dto.code)

        elif user.mfa_type == 'otp':
            if not user.mfa_secret:
                raise MFAException(
                    'User enabled MFA, but setup is incorrect: "mfa_secret" is not provided'
                )
            if not self.mfa_service.verify_mfa_code(user.mfa_secret, dto.code):
                raise InvalidCodeException(dto.code)

        return await self.authentication_service.login(user)
