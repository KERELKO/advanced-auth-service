from typing import Awaitable, Callable

from blacksheep import Request, Response


class JWTMiddleware:
    def __init__(self): ...

    async def __call__(
        self,
        request: Request,
        handler: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        # do something before passing the request to the next handler

        response = await handler(request)

        # do something after the following request handlers prepared the response
        return response
