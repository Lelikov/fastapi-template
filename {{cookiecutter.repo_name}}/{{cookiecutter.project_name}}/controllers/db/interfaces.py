from contextlib import AbstractAsyncContextManager
from typing import Protocol


class DbControllerProtocol(Protocol):
    """DB controller interface."""

    def transaction(self) -> AbstractAsyncContextManager["DbControllerProtocol"]:
        """Transaction."""

    async def get_id(self, *, item_id: int) -> int:
        """Get item id."""
