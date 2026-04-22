from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlmodel import SQLModel

from app.core.exceptions import EntityNotFoundError
from app.repositories.base import BaseRepository


ModelT = TypeVar('ModelT', bound=SQLModel)
CreateSchemaT = TypeVar('CreateSchemaT', bound=BaseModel)
UpdateSchemaT = TypeVar('UpdateSchemaT', bound=BaseModel)


class BaseService(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    entity_name: str

    def __init__(self, repository: BaseRepository[ModelT]) -> None:
        self.repository = repository

    async def list(self) -> list[ModelT]:
        return await self.repository.list()

    async def get(self, entity_id: int) -> ModelT:
        entity = await self.repository.get(entity_id)
        if entity is None:
            raise EntityNotFoundError(self.entity_name, entity_id)
        return entity

    async def create(self, payload: CreateSchemaT) -> ModelT:
        return await self.repository.create(payload.model_dump(exclude_none=True))

    async def update(self, entity_id: int, payload: UpdateSchemaT) -> ModelT:
        entity = await self.get(entity_id)
        update_data = payload.model_dump(exclude_unset=True, exclude_none=True)
        return await self.repository.update(entity, update_data)

    async def delete(self, entity_id: int) -> None:
        entity = await self.get(entity_id)
        await self.repository.delete(entity)
