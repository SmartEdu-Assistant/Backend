from typing import Annotated

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes

from app.core.config import settings
from app.core.exceptions import AuthenticationError, AuthorizationError
from app.models import User
from app.services.auth import AuthService


bearer_scheme = HTTPBearer(
    bearerFormat='JWT',
    description='Paste access token returned by /auth/login',
    auto_error=False,
)


async def get_current_user(
    security_scopes: SecurityScopes,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    auth_service: Annotated[AuthService, Depends(AuthService)],
) -> User:
    if credentials is None or not credentials.credentials:
        raise AuthenticationError('Not authenticated')

    token = credentials.credentials
    user = await auth_service.get_user_by_access_token(token)
    if any(role.name == settings.rbac.admin_role_name for role in user.roles):
        return user

    missing_scopes = [
        scope
        for scope in security_scopes.scopes
        if scope not in user.scopes
    ]
    if missing_scopes:
        raise AuthorizationError(
            f'Missing required scopes: {", ".join(missing_scopes)}',
            details={'missing_scopes': missing_scopes},
        )
    return user
