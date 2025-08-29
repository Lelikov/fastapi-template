"""DB adapter tests."""
from {{cookiecutter.project_name}}.adapters.db.adapter import DBWithRetries


async def _test_db_adapter_simple(db_adapter: DBWithRetries) -> None:
    """Simple db adapter test."""
    await db_adapter.execute("SELECT 1")
