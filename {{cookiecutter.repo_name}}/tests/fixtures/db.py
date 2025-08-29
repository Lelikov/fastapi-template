"""DB fixture."""
import pytest
import typing
from databases import Database

from {{cookiecutter.project_name}}.adapters.db.adapter import DBWithRetries
from {{cookiecutter.project_name}}.config import Settings


async def clear_database(database: DBWithRetries) -> None:
    # await database.execute("DELETE FROM table")
    pass

@pytest.fixture(name="connected_database", scope="session")
async def connected_database_fixture() -> typing.AsyncGenerator[DBWithRetries, None]:
    settings: Settings = Settings()
    database_no_retries: Database = Database(
        url=settings.postgres_dsn,
        min_size=settings.postgres_pool_min_size,
        max_size=settings.postgres_pool_max_size,
        force_rollback=True,
    )

    try:
        await database_no_retries.connect()
        _database: DBWithRetries = DBWithRetries(database=database_no_retries)
        await clear_database(_database)
        yield _database
    finally:
        await database_no_retries.disconnect()


@pytest.fixture(name="db_adapter")
async def database_fixture(connected_database: DBWithRetries) -> typing.AsyncGenerator[DBWithRetries, None]:
    """Database fixture."""
    async with connected_database.transaction(force_rollback=True):
        yield connected_database
