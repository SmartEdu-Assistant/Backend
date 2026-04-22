from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import TimestampedModel

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.submission import Submission, TestResult


class Assignment(TimestampedModel, table=True):
    __tablename__ = 'assignments'

    title: str = Field(max_length=255)
    description: str
    language: str = Field(max_length=50)
    deadline: Optional[datetime] = Field(default=None)
    max_score: int
    reference_solution: Optional[str] = Field(default=None, max_length=500)
    course_id: int = Field(foreign_key='courses.id')

    course: Optional['Course'] = Relationship(back_populates='assignments')
    test_cases: list['TestCase'] = Relationship(back_populates='assignment')
    submissions: list['Submission'] = Relationship(back_populates='assignment')


class TestCase(TimestampedModel, table=True):
    __tablename__ = 'test_cases'

    assignment_id: int = Field(foreign_key='assignments.id')
    input_data: str
    expected_output: str
    weight: int

    assignment: Optional[Assignment] = Relationship(back_populates='test_cases')
    test_results: list['TestResult'] = Relationship(back_populates='test_case')
