from __future__ import annotations

from typing import Annotated, Generic, TypeVar

from fastapi import Depends
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies.db import get_session

ModelT = TypeVar('ModelT', bound=SQLModel)
SessionDep = Annotated[AsyncSession, Depends(get_session)]


class BaseRepository(Generic[ModelT]):
    model: type[ModelT]

    def __init__(self, session: SessionDep) -> None:
        self.session = session

    async def list(self) -> list[ModelT]:
        result = await self.session.exec(select(self.model))
        return list(result.all())

    async def get(self, entity_id: int) -> ModelT | None:
        return await self.session.get(self.model, entity_id)

    async def get_multi_by_ids(self, entity_ids: list[int]) -> list[ModelT]:
        if not entity_ids:
            return []

        statement = select(self.model).where(self.model.id.in_(entity_ids))
        result = await self.session.exec(statement)
        return list(result.all())

    async def create(self, payload: dict) -> ModelT:
        entity = self.model(**payload)
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def save(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update(self, entity: ModelT, payload: dict) -> ModelT:
        for field_name, value in payload.items():
            setattr(entity, field_name, value)
        return await self.save(entity)

    async def delete(self, entity: ModelT) -> None:
        await self.session.delete(entity)
        await self.session.commit()
