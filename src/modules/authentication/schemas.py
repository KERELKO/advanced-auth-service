from dataclasses import dataclass


@dataclass(eq=False, repr=False, slots=True)
class LoginUserSchema:
    username: str
    password: str


@dataclass(eq=False, repr=False, slots=True)
class LogoutUserSchema:
    id: int
    username: str


@dataclass(eq=False, repr=False, slots=True)
class RegisterUserSchema:
    username: str
    password: str

    email: str | None = None
