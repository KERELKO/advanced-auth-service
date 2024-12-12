import httpx
from loguru import logger

from src.core.config import Config
from src.core.constants import (
    GOOGLE_TOKEN_URL,
    GOOGLE_USER_INFO_URL,
)
from src.core.services.interfaces import AbstractOAuthService
from src.core.utils import to_dto
from src.modules.oauth.exceptions import OAuthException

from .dto import (
    GitHubUser,
    GoogleUser,
)


class GoogleOAuthService(AbstractOAuthService[GoogleUser]):
    def __init__(self, config: Config) -> None:
        self._config = config

    async def get_user(self, code: str) -> GoogleUser:
        token_data = {
            'code': code,
            'client_id': self._config.google_client_id,
            'client_secret': self._config.google_client_secret,
            'redirect_uri': self._config.redirect_uri,
            'grant_type': 'authorization_code',
        }
        logger.info(token_data)
        async with httpx.AsyncClient() as client:
            token_response = await client.post(GOOGLE_TOKEN_URL, json=token_data)
            tokens = token_response.json()
            if token_response.status_code != 200:
                msg = (
                    f'Error occured while fetching token: {token_response.status_code}'
                    f'Body: {tokens}'
                )
                logger.error(msg)
                raise OAuthException(msg)

            access_token = tokens.get('access_token')

            headers = {'Authorization': f'Bearer {access_token}'}
            user_info_response = await client.get(GOOGLE_USER_INFO_URL, headers=headers)
            if user_info_response.status_code != 200:
                msg = (
                    f'Error occured while fetching user data: {token_response.status_code}'
                    f'Body: {tokens}'
                )
                logger.error(msg)
                raise OAuthException(msg)

        user_info = user_info_response.json()
        logger.info(user_info)
        return to_dto(GoogleUser, user_info)


class GitHubOAuthService(AbstractOAuthService[GitHubUser]): ...
