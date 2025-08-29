"""Config."""

from typing import Final

from loguru import logger
from pydantic import {% if cookiecutter.is_service_with_database -%} Field, PostgresDsn,{% endif %}field_validator
from pydantic_settings import BaseSettings

from {{cookiecutter.project_name}}.exceptions import BadLogLevelError


SENSITIVE_VARIABLES: Final[tuple[str, ...]] = ("token", "_dsn", "password", "username")


class Settings(BaseSettings):
    """{{cookiecutter.project_title}} Settings."""

    log_level: str = "DEBUG"
    {%- if cookiecutter.is_service_with_database %}
    postgres_dsn: str = Field("postgresql://{{cookiecutter.project_name}}:{{cookiecutter.project_name}}@0.0.0.0:5432/{{cookiecutter.project_name}}")
    postgres_pool_min_size: int = 5
    postgres_pool_max_size: int = 20
    {%- endif %}

    def __str__(self) -> str:
        values: list[str] = []
        for variable, value_map in self.model_json_schema().get("properties", {}).items():
            if isinstance(value_map, dict):
                is_need_to_masked = value_map.get("mask") or self._get_is_need_to_masked(variable)
                fmt_value = "***" if is_need_to_masked else getattr(self, variable)
                values.append(f"{variable}: {fmt_value}")
        return ", ".join(values)

    @staticmethod
    def _get_is_need_to_masked(variable: str) -> bool:
        return any(char in variable for char in SENSITIVE_VARIABLES)

    @field_validator("log_level")
    def _validate_log_level(cls, value: str) -> str:  # pylint: disable=no-self-use,no-self-argument  #noqa: N805
        if value not in logger._core.levels:  # type: ignore[attr-defined]  # pylint: disable=protected-access  #noqa: SLF001
            raise BadLogLevelError(value)
        return value

    def __repr__(self) -> str:
        return self.__str__()
