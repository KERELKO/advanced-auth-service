from dataclasses import dataclass
import os
from passlib.context import CryptContext
import secrets

from dotenv import load_dotenv


load_dotenv()


@dataclass(eq=False, repr=False, frozen=True, slots=True)
class AuthConfig:
    algorithms: tuple[str] = ('HS256',)
    refresh_token_expire_days: int = 7
    access_token_expire_minutes: int = 60
    crypto_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
    secret_key: str = os.getenv('SECRET_KEY', secrets.token_hex(32))

    default_permission_set: tuple[str, ...] = ('read_me', 'update_me', 'delete_me')
