from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import ORMBaseSchema, TimestampedModel

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.course import Course
    from app.models.grade import Grade


class UserRole(str, Enum):
    ADMIN = 'ADMIN'
    TEACHER = 'TEACHER'


class UserStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    BLOCKED = 'BLOCKED'


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


class UserBase(SQLModel):
    email: str = Field(max_length=255)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    role: UserRole = UserRole.TEACHER
    status: UserStatus = UserStatus.ACTIVE


class User(UserBase, TimestampedModel, table=True):
    __tablename__ = 'users'

    email: str = Field(index=True, unique=True, max_length=255)
    password_hash: str

    courses: list['Course'] = Relationship(
        back_populates='teachers',
        link_model=CourseTeacherLink,
    )
    comments: list['Comment'] = Relationship(back_populates='author')
    grades: list['Grade'] = Relationship(back_populates='grader')


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)


class UserUpdate(SQLModel):
    email: Optional[str] = Field(default=None, max_length=255)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=255)


class UserDelete(SQLModel):
    id: int


class UserPublic(UserBase, ORMBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
