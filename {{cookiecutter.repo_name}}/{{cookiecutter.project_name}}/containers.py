"""{{cookiecutter.project_title}} container worker."""

from typing import Final

from bakery import Bakery, Cake
{%- if cookiecutter.is_service_with_database %}
from databases import Database
from {{cookiecutter.project_name}}.adapters.db.adapter import DBWithRetries
from {{cookiecutter.project_name}}.controllers.db.controller import DbController
{%- endif %}

from {{cookiecutter.project_name}}.config import Settings
from {{cookiecutter.project_name}}.endpoints.dummy import DummyEndpoint
from {{cookiecutter.project_name}}.endpoints.healthchecks import HealthCheckEndpoint


DUMMY_TAG: Final[str] = "Dummy"


class {{cookiecutter.pascal_case_project_name}}Container(Bakery):
    """Main {{cookiecutter.pascal_case_project_name}} container."""

    config: Settings = Cake(Settings)

    {%- if cookiecutter.is_service_with_database %}
    _database_no_retries: Database = Cake(
        Cake(
            Database,
            url=config.postgres_dsn,
            min_size=config.postgres_pool_min_size,
            max_size=config.postgres_pool_max_size,
        ),
    )

    database: DBWithRetries = Cake(DBWithRetries, _database_no_retries)

    db_controller: DbController = Cake(DbController, db_adapter=database)
    {%- endif %}

    _health_endpoint: HealthCheckEndpoint = Cake(HealthCheckEndpoint)
    _dummy_endpoint: DummyEndpoint = Cake(DummyEndpoint)

    endpoint_includes: list = Cake(
        [
            {"router": _health_endpoint.router, "prefix": "/check"},
            {"router": _dummy_endpoint.router, "tags": [DUMMY_TAG]},
        ],
    )
