import app.models  # noqa: F401
from sqlmodel import SQLModel

metadata = SQLModel.metadata

__all__ = ['metadata']
