from typing import Any


class AppError(Exception):
    status_code = 500
    error_code = 'internal_error'
    message = 'Internal server error'

    def __init__(
        self,
        message: str | None = None,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message or self.message
        self.details = details
        super().__init__(self.message)


class EntityNotFoundError(AppError):
    status_code = 404
    error_code = 'entity_not_found'

    def __init__(self, entity_name: str, entity_id: int) -> None:
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(
            f'{entity_name} with id={entity_id} was not found',
            details={'entity_name': entity_name, 'entity_id': entity_id},
        )


class DomainValidationError(AppError):
    status_code = 400
    error_code = 'domain_validation_error'


class EntityConflictError(AppError):
    status_code = 409
    error_code = 'entity_conflict'


class AuthenticationError(AppError):
    status_code = 401
    error_code = 'authentication_error'
    message = 'Authentication failed'


class AuthorizationError(AppError):
    status_code = 403
    error_code = 'authorization_error'
    message = 'Access denied'
