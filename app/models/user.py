from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseDeleteSchema, TimestampedModel, TimestampedPublicSchema
from app.models.rbac import Role, RolePublic, UserRoleLink

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.course import Course
    from app.models.grade import Grade


class CourseTeacherLink(SQLModel, table=True):
    __tablename__ = 'course_teacher_links'

    course_id: Optional[int] = Field(
        default=None,
        foreign_key='courses.id',
        primary_key=True,
    )
    user_id: Optional[int] = Field(
        default=None,
        foreign_key='users.id',
        primary_key=True,
    )


class UserStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    BLOCKED = 'BLOCKED'


class UserBase(SQLModel):
    email: str = Field(max_length=255)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    status: UserStatus = UserStatus.ACTIVE


class User(UserBase, TimestampedModel, table=True):
    __tablename__ = 'users'

    email: str = Field(index=True, unique=True, max_length=255)
    password_hash: str
    is_verified: bool = False

    roles: list[Role] = Relationship(
        back_populates='users',
        link_model=UserRoleLink,
    )
    courses: list['Course'] = Relationship(
        back_populates='teachers',
        link_model=CourseTeacherLink,
    )
    comments: list['Comment'] = Relationship(back_populates='author')
    grades: list['Grade'] = Relationship(back_populates='grader')

    @property
    def scopes(self) -> set[str]:
        return {
            permission.scope
            for role in self.roles
            for permission in role.permissions
        }


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)


class UserUpdate(SQLModel):
    email: Optional[str] = Field(default=None, max_length=255)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    status: Optional[UserStatus] = None
    is_verified: Optional[bool] = None


class UserDelete(BaseDeleteSchema):
    pass


class UserPublic(UserBase, TimestampedPublicSchema):
    is_verified: bool = False
    roles: list[RolePublic] = []
