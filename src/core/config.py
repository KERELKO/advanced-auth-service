from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(eq=False, repr=False, frozen=True, slots=True)
class Config:
    # 'dev', 'prod', 'stage'
    env: str = os.getenv('ENV', 'dev')

    postgres_host: str = os.getenv('POSTGRES_HOST', 'postgres')
    postgres_port: int = int(os.getenv('POSTGRES_PORT', 5432))
    postgres_user: str = os.getenv('POSTGRES_USER', 'postgres')
    postgres_password: str = os.getenv('POSTGRES_PASSWORD', 'postgres')
    postgres_db: str = os.getenv('POSTGRES_DB', 'auth-db')


config = Config()
