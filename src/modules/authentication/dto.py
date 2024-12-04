from dataclasses import dataclass


@dataclass(eq=False, repr=False, slots=True)
class LoginUserDTO:
    username: str
    password: str


@dataclass(eq=False, repr=False, slots=True)
class RegisterUserDTO:
    username: str
    password: str

    email: str | None = None
