from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.rate_limit.default_limit],
    enabled=settings.rate_limit.enabled,
    headers_enabled=True,
)
