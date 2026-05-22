from app import models
from sqlmodel import SQLModel


registered_models = models
metadata = SQLModel.metadata

__all__ = ['metadata']
