from abc import ABC, abstractmethod


class AbstractNotificationService(ABC):
    @abstractmethod
    async def send(
        self,
        message: str,
        subject: str,
        to: str,
    ) -> None: ...
