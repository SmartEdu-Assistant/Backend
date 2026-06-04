import logging
from logging.config import dictConfig

from app.core.config import settings


def configure_logging() -> None:
    dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': settings.logging.format,
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                    'level': settings.logging.level,
                },
            },
            'root': {
                'handlers': ['console'],
                'level': settings.logging.level,
            },
            'loggers': {
                'app': {
                    'handlers': ['console'],
                    'level': settings.logging.level,
                    'propagate': False,
                },
            },
        },
    )


logger = logging.getLogger('app')
