from src.core.config import Config


class SecurityService:
    def __init__(self, config: Config) -> None:
        self._config = config
        self.context = config.crypto_context

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.context.hash(password)
