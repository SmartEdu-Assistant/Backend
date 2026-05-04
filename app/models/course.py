from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import TimestampedModel
from app.models.user import CourseTeacherLink, User

if TYPE_CHECKING:
    from app.models.assignment import Assignment
    from app.models.student import Group


class Course(TimestampedModel, table=True):
    __tablename__ = 'courses'

    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)

    teachers: list[User] = Relationship(
        back_populates='courses',
        link_model=CourseTeacherLink,
    )
    groups: list['Group'] = Relationship(back_populates='course')
    assignments: list['Assignment'] = Relationship(back_populates='course')
