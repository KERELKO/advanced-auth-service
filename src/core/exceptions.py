from dataclasses import dataclass


class ApplicationException(Exception):
    @property
    def msg(self) -> str:
        return self.__str__()


@dataclass(eq=False)
class ObjectDoesNotExist(ApplicationException):
    id: str

    @property
    def msg(self) -> str:
        return f'Object with id "{self.id}" does not exist'
