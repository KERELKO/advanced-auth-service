import pyotp

from src.modules.mfa.dto import Code


class MFAService:
    def __init__(
        self,
        issuer: str,
        interval: int = 30,
    ) -> None:
        self.issuer = issuer
        self.interval = interval

    def generate_secret(self) -> str:
        secret = pyotp.random_base32()
        return secret

    def generate_one_time_password(self, mfa_key: str) -> Code:
        return Code(value=self.__totp_factory(mfa_key).now(), ttl=self.interval)

    def verify_mfa_code(self, mfa_key: str, code: str) -> bool:
        totp = self.__totp_factory(mfa_key)
        return totp.verify(code)

    def __totp_factory(self, mfa_key: str) -> pyotp.TOTP:
        return pyotp.TOTP(mfa_key, interval=self.interval, issuer=self.issuer)
