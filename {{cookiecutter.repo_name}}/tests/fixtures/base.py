"""Base fixtures."""

from collections.abc import AsyncIterator

import pytest
from bakery.testbakery import BakeryMock

from tests.conftest import patch_settings_context


@pytest.fixture()
async def bakery_test(bakery_mock: BakeryMock) -> AsyncIterator[BakeryMock]:
    """Patch bakery_mock."""
    with patch_settings_context():
        yield bakery_mock
