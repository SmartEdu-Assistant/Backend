from typing import Annotated

from fastapi import Depends

from app.core.security import get_password_hash
from app.models import User, UserCreate, UserUpdate
from app.repositories import UserRepository
from app.services.base import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate]):
    entity_name = 'User'

    def __init__(
        self,
        repository: Annotated[UserRepository, Depends(UserRepository)],
    ) -> None:
        super().__init__(repository)

    async def create(self, payload: UserCreate) -> User:
        user_data = payload.model_dump(exclude={'password'})
        user_data['password_hash'] = get_password_hash(payload.password)
        return await self.repository.create(user_data)

    async def update(self, entity_id: int, payload: UserUpdate) -> User:
        update_data = payload.model_dump(
            exclude_unset=True,
            exclude_none=True,
            exclude={'password'},
        )
        if payload.password is not None:
            update_data['password_hash'] = get_password_hash(payload.password)
        entity = await self.get(entity_id)
        return await self.repository.update(entity, update_data)
