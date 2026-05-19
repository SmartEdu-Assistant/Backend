from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import ORMBaseSchema, TimestampedModel
from app.models.user import CourseTeacherLink, User

if TYPE_CHECKING:
    from app.models.assignment import Assignment
    from app.models.group import Group


class CourseBase(SQLModel):
    title: str = Field(max_length=255)
    description: Optional[str] = None
    is_active: bool = True


class Course(CourseBase, TimestampedModel, table=True):
    __tablename__ = 'courses'

    teachers: list[User] = Relationship(
        back_populates='courses',
        link_model=CourseTeacherLink,
    )
    groups: list['Group'] = Relationship(back_populates='course')
    assignments: list['Assignment'] = Relationship(back_populates='course')


class CourseCreate(CourseBase):
    teacher_ids: list[int] = Field(default_factory=list)


class CourseUpdate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    teacher_ids: Optional[list[int]] = None


class CourseDelete(SQLModel):
    id: int


class CoursePublic(CourseBase, ORMBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
