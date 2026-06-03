from typing import Annotated

from fastapi import Depends

from app.schemas.pagination import PaginationParams


PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]

__all__ = ['PaginationDep']
