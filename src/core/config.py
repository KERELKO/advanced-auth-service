from dataclasses import dataclass
import os
from typing import Literal
from passlib.context import CryptContext  # type: ignore
import secrets

from dotenv import load_dotenv


load_dotenv()


@dataclass(eq=False, repr=False, frozen=True, slots=True)
class Config:
    env: Literal['dev', 'prod', 'stage'] = os.getenv('ENV', 'dev')  # type: ignore

    postgres_dialect: str = 'postgresql+asyncpg'

    postgres_host: str = os.getenv('POSTGRES_HOST', 'postgres')
    postgres_port: int = int(os.getenv('POSTGRES_PORT', 5432))
    postgres_user: str = os.getenv('POSTGRES_USER', 'postgres')
    postgres_password: str = os.getenv('POSTGRES_PASSWORD', 'postgres')
    postgres_db: str = os.getenv('POSTGRES_DB', 'postgres')

    redis_host: str = os.getenv('REDIS_HOST', 'rediska')
    redis_port: int = int(os.getenv('REDIS_PORT', 6379))

    smtp_port: int = int(os.getenv('SMTP_PORT', 587))
    smtp_server: str = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    email_address: str = os.getenv('APP_EMAIL_ADDRESS', 'NOT SUPPORTED')
    email_password: str = os.getenv('APP_EMAIL_PASSWORD', 'NOT SUPPORTED')

    algorithms: tuple[str] = ('HS256',)
    refresh_token_expire_days: int = 7
    access_token_expire_minutes: int = 60
    crypto_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
    secret_key: str = os.getenv('SECRET_KEY', secrets.token_hex(32))

    default_permission_set: tuple[str, ...] = ('read_me', 'update_me', 'delete_me')

    @property
    def postgres_connection_string(self) -> str:
        user_pwd = f'{self.postgres_user}:{self.postgres_password}'
        host_port = f'{self.postgres_host}:{self.postgres_port}'
        connection_string = f'{self.postgres_dialect}://{user_pwd}@{host_port}/{self.postgres_db}'
        return connection_string

    @property
    def redis_url(self) -> str:
        return f'redis://{self.redis_host}:{self.redis_port}'

    def __post_init__(self) -> None:
        for field_name in self.__slots__:
            if not getattr(self, field_name, None):
                raise TypeError(f'Empty value for {field_name}')


config = Config()
