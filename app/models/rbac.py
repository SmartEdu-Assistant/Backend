from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import TimestampedModel, TimestampedPublicSchema

if TYPE_CHECKING:
    from app.models.user import User


class UserRoleLink(SQLModel, table=True):
    __tablename__ = 'user_role_links'

    user_id: Optional[int] = Field(
        default=None,
        foreign_key='users.id',
        primary_key=True,
    )
    role_id: Optional[int] = Field(
        default=None,
        foreign_key='roles.id',
        primary_key=True,
    )


class RolePermissionLink(SQLModel, table=True):
    __tablename__ = 'role_permission_links'

    role_id: Optional[int] = Field(
        default=None,
        foreign_key='roles.id',
        primary_key=True,
    )
    permission_id: Optional[int] = Field(
        default=None,
        foreign_key='permissions.id',
        primary_key=True,
    )


class Permission(TimestampedModel, table=True):
    __tablename__ = 'permissions'

    subject: str = Field(max_length=100)
    action: str = Field(max_length=100)
    scope: str = Field(unique=True, index=True, max_length=255)

    roles: list['Role'] = Relationship(
        back_populates='permissions',
        link_model=RolePermissionLink,
    )


class PermissionPublic(TimestampedPublicSchema):
    subject: str
    action: str
    scope: str


class Role(TimestampedModel, table=True):
    __tablename__ = 'roles'

    name: str = Field(unique=True, index=True, max_length=100)
    description: str | None = Field(default=None, max_length=255)

    users: list['User'] = Relationship(
        back_populates='roles',
        link_model=UserRoleLink,
    )
    permissions: list[Permission] = Relationship(
        back_populates='roles',
        link_model=RolePermissionLink,
    )


class RolePublic(TimestampedPublicSchema):
    name: str
    description: str | None = None
