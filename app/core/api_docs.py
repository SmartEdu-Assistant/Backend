from collections.abc import Mapping

from app.schemas.errors import ErrorResponse, ValidationErrorResponse


def combine_responses(*response_sets: Mapping[int, dict]) -> dict[int, dict]:
    combined: dict[int, dict] = {}
    for response_set in response_sets:
        combined.update(response_set)
    return combined


SERVER_ERROR_RESPONSES = {
    429: {'model': ErrorResponse, 'description': 'Too many requests'},
    500: {'model': ErrorResponse, 'description': 'Internal server error'},
}

VALIDATION_ERROR_RESPONSES = {
    422: {'model': ValidationErrorResponse, 'description': 'Request validation error'},
}

AUTH_ERROR_RESPONSES = {
    401: {'model': ErrorResponse, 'description': 'Authentication failed'},
    403: {'model': ErrorResponse, 'description': 'Access denied'},
}

NOT_FOUND_ERROR_RESPONSES = {
    404: {'model': ErrorResponse, 'description': 'Entity was not found'},
}

CONFLICT_ERROR_RESPONSES = {
    409: {'model': ErrorResponse, 'description': 'Entity conflict'},
}

BAD_REQUEST_ERROR_RESPONSES = {
    400: {'model': ErrorResponse, 'description': 'Domain validation failed'},
}
