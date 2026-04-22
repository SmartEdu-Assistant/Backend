from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import TimestampedModel, UserRole, UserStatus

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.submission import Comment, Grade


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


class User(TimestampedModel, table=True):
    __tablename__ = 'users'

    email: str = Field(index=True, unique=True, max_length=255)
    password_hash: str = Field(max_length=255)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    role: UserRole = Field(default=UserRole.TEACHER, max_length=30)
    status: UserStatus = Field(default=UserStatus.ACTIVE, max_length=30)

    courses: list['Course'] = Relationship(
        back_populates='teachers',
        link_model=CourseTeacherLink,
    )
    comments: list['Comment'] = Relationship(back_populates='author')
    grades: list['Grade'] = Relationship(back_populates='grader')
