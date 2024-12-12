import os
from dataclasses import dataclass


@dataclass(eq=False, repr=False, frozen=True)
class StorageConfig:
    postgres_dialect: str = 'postgresql+asyncpg'

    postgres_host: str = os.getenv('POSTGRES_HOST', 'postgres')
    postgres_port: int = int(os.getenv('POSTGRES_PORT', 5432))
    postgres_user: str = os.getenv('POSTGRES_USER', 'postgres')
    postgres_password: str = os.getenv('POSTGRES_PASSWORD', 'postgres')
    postgres_db: str = os.getenv('POSTGRES_DB', 'postgres')

    redis_host: str = os.getenv('REDIS_HOST', 'rediska')
    redis_port: int = int(os.getenv('REDIS_PORT', 6379))

    @property
    def postgres_connection_string(self) -> str:
        user_pwd = f'{self.postgres_user}:{self.postgres_password}'
        host_port = f'{self.postgres_host}:{self.postgres_port}'
        connection_string = f'{self.postgres_dialect}://{user_pwd}@{host_port}/{self.postgres_db}'
        return connection_string

    @property
    def redis_url(self) -> str:
        return f'redis://{self.redis_host}:{self.redis_port}'
