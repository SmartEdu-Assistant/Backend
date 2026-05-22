from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseDeleteSchema, TimestampedModel, TimestampedPublicSchema

if TYPE_CHECKING:
    from app.models.assignment import Assignment
    from app.models.test_result import TestResult


class TestCaseBase(SQLModel):
    assignment_id: int
    input_data: str
    expected_output: str
    weight: int


class TestCase(TestCaseBase, TimestampedModel, table=True):
    __tablename__ = 'test_cases'

    assignment_id: int = Field(foreign_key='assignments.id')

    assignment: Optional['Assignment'] = Relationship(back_populates='test_cases')
    test_results: list['TestResult'] = Relationship(back_populates='test_case')


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseUpdate(SQLModel):
    assignment_id: Optional[int] = None
    input_data: Optional[str] = None
    expected_output: Optional[str] = None
    weight: Optional[int] = None


class TestCaseDelete(BaseDeleteSchema):
    pass


class TestCasePublic(TestCaseBase, TimestampedPublicSchema):
    pass
