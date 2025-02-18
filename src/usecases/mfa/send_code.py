from dataclasses import dataclass
import datetime

from src.core.dto.users import UserDTO
from src.core.services.notifications import EmailNotificationService
from src.core.storages.repositories.base import AbstractCodeRepository
from src.modules.mfa.service import MFAService
from src.modules.mfa.dto import AddMFACode, MFACode
from src.modules.mfa.exceptions import MFAException

from .. import UseCase


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
