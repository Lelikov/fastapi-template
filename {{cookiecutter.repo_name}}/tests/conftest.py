"""Conftest."""
import asyncio
import os
import unittest
import unittest.mock
from collections.abc import Callable, Generator
from contextlib import contextmanager
from copy import deepcopy
from typing import Final, Iterator

import pytest
from fastapi import APIRouter, FastAPI
from httpx import AsyncClient, ASGITransport


pytest_plugins = [
    "tests.fixtures.base",
    {%- if cookiecutter.is_service_with_database %}
    "tests.fixtures.db"
    {%- endif %}
]

SETTINGS: Final[dict] = {
    "LOG_LEVEL": "DEBUG",
}


@pytest.fixture()
def test_client() -> Callable:
    """Test fastapi client."""

    @contextmanager
    def client(routers: list[APIRouter], dependencies: dict | None = None) -> Generator:
        app = FastAPI()
        for router in routers:
            app.include_router(router)
        client = AsyncClient(base_url="https://url", transport=ASGITransport(app=app))
        dependencies = dependencies or {}
        for key, value in dependencies.items():
            app.dependency_overrides[key] = value
        yield client

    return client


@contextmanager
def patch_settings_context(**items: str) -> Generator:
    """Just mock VcenterAdapterSettings with items or default values."""
    settings: dict = deepcopy(SETTINGS)

    settings.update(**items)

    with unittest.mock.patch.dict(os.environ, settings):
        yield


@pytest.fixture(scope="session", name="patch_settings")
def _patch_settings() -> Generator:
    """Patch settings fixture."""
    with patch_settings_context():
        yield


@pytest.fixture()
def non_mocked_hosts() -> list:
    """Httpx-mock ignore this hostnames."""
    return ["https://url"]


@pytest.fixture(scope="session")
def event_loop() -> Iterator:
    """Override asyncio event_loop fixture with different scope."""
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    yield loop
    loop.close()
