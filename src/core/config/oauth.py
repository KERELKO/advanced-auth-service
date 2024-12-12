from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(eq=False, repr=False, frozen=True)
class OAuthConfig:
    google_client_id: str = os.getenv('GOOGLE_CLIENT_ID', '')
    google_client_secret: str = os.getenv('GOOGLE_CLIENT_SECRET', '')

    github_client_id: str = os.getenv('GITHUB_CLIENT_ID', '')
    github_client_secret: str = os.getenv('GITHUB_CLIENT_SECRET', '')

    redirect_uri: str = os.getenv('OAUTH_REDIRECT_URI', '')
