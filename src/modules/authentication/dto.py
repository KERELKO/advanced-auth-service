from dataclasses import dataclass


@dataclass(eq=False, repr=False, slots=True)
class LoginUserDTO:
    username: str
    password: str


@dataclass(eq=False, repr=False, slots=True)
class LogoutUserDTO:
    id: int
    username: str


@dataclass(eq=False, repr=False, slots=True)
class RegisterUserDTO:
    username: str
    password_1: str
    password_2: str

    email: str | None = None
    phone: str | None = None


@dataclass(eq=False, repr=False, slots=True)
class UserDTO:
    id: int
    username: str
    email: str | None = None
    phone: str | None = None
