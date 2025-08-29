"""Tests {{cookiecutter.project_title}}."""

from {{cookiecutter.project_name}}.exceptions import (
    BadLogLevelError,
    BadRequestError,
    ConflictError,
    DBConnectionError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
)


def test_exceptions() -> None:
    """Test ok."""
    test_model: BadRequestError = BadRequestError(detail={"message": "BadRequestError"})
    assert test_model.status_code == 400
    test_model: ForbiddenError = ForbiddenError(detail={"message": "forbidden"})
    assert test_model.status_code == 403
    test_model: NotFoundError = NotFoundError(detail={"message": "NotFoundError"})
    assert test_model.status_code == 404
    test_model: ConflictError = ConflictError(detail={"message": "ConflictError"})
    assert test_model.status_code == 409
    test_model: InternalServerError = InternalServerError(detail={"message": "InternalServerError"})
    assert test_model.status_code == 500
    test_model: BadLogLevelError = BadLogLevelError(log_level="OLOLOSH")
    assert test_model.status_code == 500
    test_model: DBConnectionError = DBConnectionError(exc="OLOLOSH")  # type: ignore[arg-type]
    assert test_model.status_code == 500
