import os
from dataclasses import dataclass
from typing import Literal

from dotenv import load_dotenv

from .auth import AuthConfig
from .oauth import OAuthConfig
from .storage import StorageConfig


load_dotenv()


@dataclass(eq=False, repr=False, frozen=True, slots=True)
class Config(AuthConfig, StorageConfig, OAuthConfig):
    env: Literal['dev', 'prod', 'stage'] = os.getenv('ENV', 'dev')  # type: ignore

    smtp_port: int = int(os.getenv('SMTP_PORT', 587))
    smtp_server: str = os.getenv('SMTP_SERVER', 'localhost')
    email_address: str = os.getenv('APP_EMAIL_ADDRESS', 'NOT SUPPORTED')
    email_password: str = os.getenv('APP_EMAIL_PASSWORD', 'NOT SUPPORTED')

    def __post_init__(self) -> None:
        for field_name in self.__slots__:
            if not getattr(self, field_name, None):
                raise TypeError(f'Empty value for {field_name}')


config = Config()
