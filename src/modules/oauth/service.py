from src.core.services.interfaces import AbstractOAuthService

from .dto import GitHubUser, GoogleUser


class GoogleOAuthService(AbstractOAuthService[GoogleUser]): ...


class GitHubOAuthService(AbstractOAuthService[GitHubUser]): ...
