from dataclasses import dataclass
import os
from passlib.context import CryptContext  # type: ignore
import secrets

from dotenv import load_dotenv


load_dotenv()


@dataclass(eq=False, repr=False, frozen=True, slots=True)
class Config:
    # 'dev', 'prod', 'stage'
    env: str = os.getenv('ENV', 'dev')

    postgres_dialect: str = 'postgresql+asyncpg'

    postgres_host: str = os.getenv('POSTGRES_HOST', 'postgres')
    postgres_port: int = int(os.getenv('POSTGRES_PORT', 5432))
    postgres_user: str = os.getenv('POSTGRES_USER', 'admin')
    postgres_password: str = os.getenv('POSTGRES_PASSWORD', 'admin')
    postgres_db: str = os.getenv('POSTGRES_DB', 'auth-db')

    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30
    crypto_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
    secret_key: str = os.getenv('SECRET_KEY', secrets.token_hex(32))

    @property
    def postgres_connection_string(self) -> str:
        user_pwd = f'{self.postgres_user}:{self.postgres_password}'
        host_port = f'{self.postgres_host}:{self.postgres_port}'
        connection_string = f'{self.postgres_dialect}://{user_pwd}@{host_port}/{self.postgres_db}'
        return connection_string


config = Config()
