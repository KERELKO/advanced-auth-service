from pathlib import Path
import pyotp
import qrcode

from src.core.exceptions import ObjectDoesNotExist
from src.core.storages.repositories.base import AbstractCodeRepository
from src.modules.mfa.exceptions import CodeExpiredException


class MFAService:
    def __init__(
        self,
        code_repository: AbstractCodeRepository,
        issuer: str = 'KERELKO: Advanced Auth Service',
        interval: int = 30,
    ) -> None:
        self.issuer = issuer
        self.interval = interval
        self.code_repository = code_repository

    async def check_storage_code(self, user_id: int, code: str) -> bool:
        try:
            storage_code = await self.code_repository.get(user_id)
        except ObjectDoesNotExist as e:
            raise CodeExpiredException(e)
        return storage_code == code

    def generate_otp_uri(
        self,
        mfa_key: str,
        name: str,
        filepath: Path | None = None,
    ) -> str:
        """Generate and return OTP uri for the secret key.
        * Can be saved to file as `qrcode` if `filepath` provided
        """
        totp = self.__totp_factory(mfa_key)
        otp_uri = totp.provisioning_uri(name=name, issuer_name=self.issuer)
        if filepath:
            with open(filepath, '+wb') as file:
                qr = qrcode.make(otp_uri)
                qr.save(file)
        return otp_uri

    def generate_secret(self) -> str:
        secret = pyotp.random_base32()
        return secret

    def generate_one_time_password(self, mfa_key: str) -> str:
        return self.__totp_factory(mfa_key).now()

    def verify_mfa_code(self, mfa_key: str, code: str) -> bool:
        totp = self.__totp_factory(mfa_key)
        return totp.verify(code)

    def __totp_factory(self, mfa_key: str) -> pyotp.TOTP:
        return pyotp.TOTP(mfa_key, interval=self.interval, issuer=self.issuer)
