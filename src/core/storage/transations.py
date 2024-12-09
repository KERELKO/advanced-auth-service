import typing as t


class Transaction(t.Protocol):
    async def __aenter__(self) -> None: ...

    async def __aexit__(self, *args) -> None:
        await self.rollback()

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
