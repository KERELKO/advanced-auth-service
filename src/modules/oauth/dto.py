from src.core.dto.users import AddUserDTO, ExternalUser


class GitHubUser(ExternalUser):
    login: str
    name: str
    email: str | None = None

    def as_add_user_dto(self) -> AddUserDTO:
        return AddUserDTO(
            username=self.login,
            email=self.email,
            oauth_provider='github',
            oauth_provider_id=self.id,
        )


class GoogleUser(ExternalUser):
    email: str
    name: str
    given_name: str

    def as_add_user_dto(self) -> AddUserDTO:
        return AddUserDTO(
            username=self.given_name,
            email=self.email,
            oauth_provider_id=self.id,
            oauth_provider='google',
        )
