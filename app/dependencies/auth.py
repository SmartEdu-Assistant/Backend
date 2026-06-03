from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from app.core.config import settings
from app.core.rbac import SCOPE_DESCRIPTIONS
from app.models import User
from app.services.auth import AuthService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{settings.app.api_v1_prefix}/auth/login',
    scopes=SCOPE_DESCRIPTIONS,
)


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(AuthService)],
) -> User:
    user = await auth_service.get_user_by_access_token(token)
    if any(role.name == settings.rbac.admin_role_name for role in user.roles):
        return user

    missing_scopes = [
        scope
        for scope in security_scopes.scopes
        if scope not in user.scopes
    ]
    if missing_scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Missing required scopes: {", ".join(missing_scopes)}',
        )
    return user
