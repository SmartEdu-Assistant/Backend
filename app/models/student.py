from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import TimestampedModel

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.submission import Submission


class Group(TimestampedModel, table=True):
    __tablename__ = 'groups'

    name: str = Field(max_length=100)
    semester: str = Field(max_length=50)
    year: int
    course_id: int = Field(foreign_key='courses.id')

    course: Optional['Course'] = Relationship(back_populates='groups')
    students: list['Student'] = Relationship(back_populates='group')


class Student(TimestampedModel, table=True):
    __tablename__ = 'students'

    full_name: str = Field(max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    group_id: int = Field(foreign_key='groups.id')

    group: Optional[Group] = Relationship(back_populates='students')
    submissions: list['Submission'] = Relationship(back_populates='student')
