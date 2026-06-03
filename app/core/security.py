from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings

password_hasher = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def create_jwt_token(
    *,
    subject: str,
    expires_delta: timedelta,
    token_type: str,
) -> tuple[str, str, datetime]:
    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + expires_delta
    token_id = str(uuid4())
    payload = {
        'iat': int(issued_at.timestamp()),
        'exp': int(expires_at.timestamp()),
        'sub': subject,
        'jti': token_id,
        'token_type': token_type,
    }
    token = jwt.encode(
        payload=payload,
        key=settings.auth.secret_key,
        algorithm=settings.auth.algorithm,
    )
    return token, token_id, expires_at


def decode_jwt_token(token: str) -> dict:
    try:
        return jwt.decode(
            jwt=token,
            key=settings.auth.secret_key,
            algorithms=[settings.auth.algorithm],
            options={'require': ['iat', 'exp', 'sub', 'jti']},
        )
    except InvalidTokenError as exc:
        raise ValueError(str(exc)) from exc
