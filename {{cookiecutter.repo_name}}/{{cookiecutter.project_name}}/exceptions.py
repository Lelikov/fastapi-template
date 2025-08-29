"""{{cookiecutter.project_title}} error models."""

from enum import IntEnum
from typing import Final

from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel


BODY_ERRORS: Final[dict] = {}
# pylint: disable=invalid-name


class ErrorModel(BaseModel):
    """{{cookiecutter.project_title}} error response.
    """

    type: str = "https://confluence.com/Responses"
    detail: str
    error_code: int


class ErrCode(IntEnum):
    """Internal error codes."""

    BadRequest = 1
    BadLogLevelError = 2
    DBConnectionError = 3


class BadRequestError(HTTPException):
    """400."""

    def __init__(self, detail: dict) -> None:
        super().__init__(status_code=400, detail=detail)



class ForbiddenError(HTTPException):
    """403."""

    def __init__(self, detail: dict) -> None:
        super().__init__(status_code=403, detail=detail)


class NotFoundError(HTTPException):
    """404."""

    def __init__(self, detail: dict) -> None:
        super().__init__(status_code=404, detail=detail)


class ConflictError(HTTPException):
    """409."""

    def __init__(self, detail: dict) -> None:
        super().__init__(status_code=409, detail=detail)


class InternalServerError(HTTPException):
    """500."""

    def __init__(self, detail: dict) -> None:
        super().__init__(status_code=500, detail=detail)


class BadLogLevelError(InternalServerError):
    """500."""

    def __init__(self, log_level: str) -> None:
        super().__init__(
            detail={
                "detail": f"Incorrect logging level: {log_level}",
                "error_code": ErrCode.BadLogLevelError,
            },
        )


class DBConnectionError(InternalServerError):
    """500."""

    def __init__(self, exc: Exception) -> None:
        super().__init__(
            detail={
                "detail": f"Database connection problem. Exception: {exc}",
                "error_code": ErrCode.DBConnectionError,
            },
        )

class {{cookiecutter.pascal_case_project_name}}Error(Exception):
    """Base exception for {{cookiecutter.project_title}}"""

    default_message = "An error occurred in the {{cookiecutter.project_title}}."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)

{%- if cookiecutter.is_service_with_database %}
class DatabaseError({{cookiecutter.pascal_case_project_name}}Error):
    """Database error."""

    default_message = "An error occurred during the database operation."
{%- endif %}

def _make_detail(loc: tuple[str], err_msg: str) -> str:
    return " ".join(str(location) for location in loc) + " " + err_msg


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:  # pragma: no cover
    """{{cookiecutter.project_title}} request validation handler."""
    err = ErrorModel(detail="", error_code=0)
    for err_detail in exc.errors():
        loc = err_detail["loc"]
        if (err_detail["type"] == "value_error.missing") and loc in BODY_ERRORS:
            err.detail = _make_detail(loc, err_detail["msg"])  # type: ignore[attr-defined]
            err.error_code = int(BODY_ERRORS[loc])
            break
    else:
        err.detail = "\n".join(
            _make_detail(loc=err_detail["loc"], err_msg=err_detail["msg"])  # type: ignore[attr-defined]
            for err_detail in exc.errors()
        )
        err.error_code = int(ErrCode.BadRequest)

    logger.error(
        f"{request.url.path} validation error: {err.detail}, error_code: {err.error_code}",
    )

    return JSONResponse(status_code=400, content=err.dict())


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:  # pragma: no cover
    """HTTP exception handling and return valid JSON format response It's interesting case 'cause exc.detail type is.

    Any, and not str as mypy states.
    """
    if isinstance(exc.detail, str):
        err = ErrorModel(detail=exc.detail, error_code=0, type="")
    else:
        err = ErrorModel(**exc.detail)  # type: ignore[attr-defined]

    logger.error(
        f"{request.url.path} response error: {err.detail}, error_code: {err.error_code}",
    )

    return JSONResponse(status_code=exc.status_code, content=err.dict())
