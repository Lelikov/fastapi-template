"""DB adapter interface."""
from contextlib import AbstractAsyncContextManager

import typing

from sqlalchemy.ext.asyncio import AsyncSession


class DbSessionInterface(typing.Protocol):
    """DB with retries interface."""

    def begin(self) -> AbstractAsyncContextManager[AsyncSession]:
        """Transaction."""


class DbAdapterInterface(typing.Protocol):
    """DB adapter interface."""

    async def execute(self, query: str, values: dict | None = None) -> typing.Any:
        """Execute."""

    async def fetch_val(self, query: str, values: dict | None = None) -> typing.Any:
        """Fetch_val."""

    async def fetch_one(self, query: str, values: dict | None = None) -> None | typing.Mapping:
        """Fetch_one."""

    async def fetch_all(self, query: str, values: dict | None = None) -> typing.Sequence[typing.Mapping]:
        """Fetch_all."""

    def transaction(self) -> AbstractAsyncContextManager:
        """Transaction."""
