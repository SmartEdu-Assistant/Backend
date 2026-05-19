from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import ORMBaseSchema, TimestampedModel

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.submission import Submission
    from app.models.test_case import TestCase


class AssignmentBase(SQLModel):
    title: str = Field(max_length=255)
    description: str
    language: str = Field(max_length=50)
    deadline: Optional[datetime] = None
    max_score: int
    reference_solution: Optional[str] = Field(default=None, max_length=500)
    course_id: int


class Assignment(AssignmentBase, TimestampedModel, table=True):
    __tablename__ = 'assignments'

    course_id: int = Field(foreign_key='courses.id')

    course: Optional['Course'] = Relationship(back_populates='assignments')
    test_cases: list['TestCase'] = Relationship(back_populates='assignment')
    submissions: list['Submission'] = Relationship(back_populates='assignment')


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    language: Optional[str] = Field(default=None, max_length=50)
    deadline: Optional[datetime] = None
    max_score: Optional[int] = None
    reference_solution: Optional[str] = Field(default=None, max_length=500)
    course_id: Optional[int] = None


class AssignmentDelete(SQLModel):
    id: int


class AssignmentPublic(AssignmentBase, ORMBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
