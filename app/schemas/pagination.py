from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel, Field


ItemT = TypeVar('ItemT')


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


class Page(BaseModel, Generic[ItemT]):
    items: list[ItemT]
    total: int
    page: int
    size: int
    pages: int

    @classmethod
    def create(
        cls,
        *,
        items: list[ItemT],
        total: int,
        params: PaginationParams,
    ) -> 'Page[ItemT]':
        return cls(
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            pages=ceil(total / params.size) if total else 0,
        )
