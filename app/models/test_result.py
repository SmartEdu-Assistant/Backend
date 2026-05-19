from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseTableModel, ORMBaseSchema

if TYPE_CHECKING:
    from app.models.submission import Submission
    from app.models.test_case import TestCase


class TestResultBase(SQLModel):
    submission_id: int
    test_case_id: int
    passed: bool
    execution_time_ms: Optional[int] = None
    error_message: Optional[str] = None


class TestResult(TestResultBase, BaseTableModel, table=True):
    __tablename__ = 'test_results'

    submission_id: int = Field(foreign_key='submissions.id')
    test_case_id: int = Field(foreign_key='test_cases.id')

    submission: Optional['Submission'] = Relationship(back_populates='test_results')
    test_case: Optional['TestCase'] = Relationship(back_populates='test_results')


class TestResultCreate(TestResultBase):
    pass


class TestResultUpdate(SQLModel):
    submission_id: Optional[int] = None
    test_case_id: Optional[int] = None
    passed: Optional[bool] = None
    execution_time_ms: Optional[int] = None
    error_message: Optional[str] = None


class TestResultDelete(SQLModel):
    id: int


class TestResultPublic(TestResultBase, ORMBaseSchema):
    id: int
