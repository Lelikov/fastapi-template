"""DB controller."""
import contextlib
import typing

from loguru import logger

from {{cookiecutter.project_name}}.adapters.db.interfaces import DbAdapterInterface
from {{cookiecutter.project_name}}.exceptions import DatabaseError


class DbController:
    """DB controller."""

    def __init__(self, db_adapter: DbAdapterInterface) -> None:
        self.db_adapter: typing.Final[DbAdapterInterface] = db_adapter

    async def get_id(self, *, item_id: int) -> int:
        query: str = "SELECT * FROM table WHERE id = :id"
        logger.debug(f"Get item: {item_id = }")
        item = await self.db_adapter.fetch_one(query, {"id": item_id})

        if not item:
            raise DatabaseError(f"Item not found for id: {item_id}.")

        return item["id"]

    @contextlib.asynccontextmanager
    async def transaction(self) -> typing.AsyncGenerator["DbController", None]:
        """Transaction."""

        async with self.db_adapter.transaction() as transaction:
            yield DbController(transaction)
