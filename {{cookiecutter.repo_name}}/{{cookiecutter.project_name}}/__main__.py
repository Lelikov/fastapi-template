"""{{cookiecutter.project_title}} entrypoint service file."""
import sys

from bakery import bake
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from loguru import logger

from {{cookiecutter.project_name}}.config import Settings
from {{cookiecutter.project_name}}.containers import {{cookiecutter.pascal_case_project_name}}Container
from {{cookiecutter.project_name}}.exceptions import http_exception_handler, validation_exception_handler


async def startup() -> None:
    """Global initialization."""
    await bake({{cookiecutter.pascal_case_project_name}}Container.config)
    settings: Settings = {{cookiecutter.pascal_case_project_name}}Container.config()
    logger.remove()
    logger.add(sys.stdout, level=settings.log_level)
    logger.info(f"Settings: {settings}")

    await {{cookiecutter.pascal_case_project_name}}Container.aopen()
    for kwargs in {{cookiecutter.pascal_case_project_name}}Container.endpoint_includes():  # type: ignore[operator]
        APP.include_router(**kwargs)


async def shutdown() -> None:
    """Global shutdown."""
    await {{cookiecutter.pascal_case_project_name}}Container.aclose()


_API_VERSION = "v1"
_API_PREFIX = f"/api/{_API_VERSION}"

APP: FastAPI = FastAPI(
    title="{{cookiecutter.project_title}}",
    description="{{cookiecutter.project_title}} self-service",
    docs_url="/api/v1/doc",
    on_startup=[startup],
    on_shutdown=[shutdown],
    exception_handlers={
        RequestValidationError: validation_exception_handler,
        StarletteHTTPException: http_exception_handler,
    },
)
