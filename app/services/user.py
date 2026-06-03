from datetime import datetime, timedelta
import secrets
from typing import Annotated

from fastapi import Depends

from app.core.config import settings
from app.core.exceptions import DomainValidationError, EntityConflictError
from app.core.security import get_password_hash
from app.models import User, UserCreate, UserUpdate
from app.repositories import RoleRepository, UserRepository
from app.services.base import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate]):
    entity_name = 'User'

    def __init__(
        self,
        repository: Annotated[UserRepository, Depends(UserRepository)],
        role_repository: Annotated[RoleRepository, Depends(RoleRepository)],
    ) -> None:
        super().__init__(repository)
        self.role_repository = role_repository

    async def create(self, payload: UserCreate) -> User:
        existing_user = await self.repository.get_by_email(payload.email)
        if existing_user is not None:
            raise EntityConflictError('User with this email already exists')

        public_role = await self.role_repository.get_by_name(
            settings.rbac.public_role_name,
        )
        if public_role is None:
            raise DomainValidationError('Public role is not initialized')

        user_data = payload.model_dump(exclude={'password'})
        user_data['password_hash'] = get_password_hash(payload.password)
        user_data['verification_token'] = secrets.token_urlsafe(32)
        user_data['verification_token_expires_at'] = datetime.utcnow() + timedelta(
            hours=settings.auth.verification_token_ttl_hours,
        )
        user_data['is_verified'] = False
        user = User(**user_data)
        user.roles = [public_role]
        return await self.repository.save(user)

    async def update(self, entity_id: int, payload: UserUpdate) -> User:
        update_data = payload.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )
        entity = await self.get(entity_id)
        return await self.repository.update(entity, update_data)

    async def update_roles(self, entity_id: int, role_names: list[str]) -> User:
        unique_role_names = list(dict.fromkeys(role_names))
        if not unique_role_names:
            raise DomainValidationError('At least one role must be provided')

        user = await self.get(entity_id)
        roles = await self.role_repository.get_by_names(unique_role_names)
        if len(roles) != len(unique_role_names):
            raise DomainValidationError('One or more roles do not exist')

        user.roles = roles
        return await self.repository.save(user)
