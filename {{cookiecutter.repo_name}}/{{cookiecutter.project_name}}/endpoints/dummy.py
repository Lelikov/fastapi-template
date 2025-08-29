from typing import Final

from fastapi import APIRouter


class DummyEndpoint:
    def __init__(self) -> None:
        self.router: Final[APIRouter] = APIRouter()
        self.router.add_api_route(
            "/dummy",
            self.__call__,
            methods=["GET"],
            status_code=200,
            name="Dummy endpoint",
        )

    async def __call__(self) -> None:
        return None
