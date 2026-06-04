from typing import Any

from sqlmodel import SQLModel


class ErrorResponse(SQLModel):
    error_code: str
    message: str
    details: dict[str, Any] | None = None


class ValidationErrorItem(SQLModel):
    field: str
    message: str


class ValidationErrorResponse(SQLModel):
    error_code: str
    message: str
    details: list[ValidationErrorItem]
