from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import BaseTableModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.assignment import Assignment, TestCase
    from app.models.student import Student
    from app.models.user import User


class Submission(BaseTableModel, table=True):
    __tablename__ = 'submissions'

    assignment_id: int = Field(foreign_key='assignments.id')
    student_id: int = Field(foreign_key='students.id')
    file_path: str = Field(max_length=500)
    submitted_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    assignment: Optional['Assignment'] = Relationship(back_populates='submissions')
    student: Optional['Student'] = Relationship(back_populates='submissions')
    test_results: list['TestResult'] = Relationship(back_populates='submission')
    comments: list['Comment'] = Relationship(back_populates='submission')
    grades: list['Grade'] = Relationship(back_populates='submission')
    plagiarism_reports: list['PlagiarismReport'] = Relationship(
        back_populates='submission',
        sa_relationship_kwargs={
            'foreign_keys': '[PlagiarismReport.submission_id]',
        },
    )
    compared_reports: list['PlagiarismReport'] = Relationship(
        back_populates='compared_submission',
        sa_relationship_kwargs={
            'foreign_keys': '[PlagiarismReport.compared_with_id]',
        },
    )


class TestResult(BaseTableModel, table=True):
    __tablename__ = 'test_results'

    submission_id: int = Field(foreign_key='submissions.id')
    test_case_id: int = Field(foreign_key='test_cases.id')
    passed: bool
    execution_time_ms: Optional[int] = Field(default=None)
    error_message: Optional[str] = Field(default=None)

    submission: Optional[Submission] = Relationship(back_populates='test_results')
    test_case: Optional['TestCase'] = Relationship(back_populates='test_results')


class PlagiarismReport(TimestampedModel, table=True):
    __tablename__ = 'plagiarism_reports'

    submission_id: int = Field(foreign_key='submissions.id')
    compared_with_id: int = Field(foreign_key='submissions.id')
    similarity_percent: float
    detected_blocks: Optional[str] = Field(default=None)

    submission: Optional[Submission] = Relationship(
        back_populates='plagiarism_reports',
        sa_relationship_kwargs={'foreign_keys': '[PlagiarismReport.submission_id]'},
    )
    compared_submission: Optional[Submission] = Relationship(
        back_populates='compared_reports',
        sa_relationship_kwargs={'foreign_keys': '[PlagiarismReport.compared_with_id]'},
    )


class Comment(TimestampedModel, table=True):
    __tablename__ = 'comments'

    submission_id: int = Field(foreign_key='submissions.id')
    author_id: int = Field(foreign_key='users.id')
    content: str
    start_line_number: Optional[int] = Field(default=None)
    end_line_number: Optional[int] = Field(default=None)
    is_system_generated: bool = Field(default=False)

    submission: Optional[Submission] = Relationship(back_populates='comments')
    author: Optional['User'] = Relationship(back_populates='comments')


class Grade(BaseTableModel, table=True):
    __tablename__ = 'grades'

    submission_id: int = Field(foreign_key='submissions.id', unique=True)
    score: int
    max_score: int
    graded_by: int = Field(foreign_key='users.id')
    graded_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_published: bool = Field(default=False)

    submission: Optional[Submission] = Relationship(back_populates='grades')
    grader: Optional['User'] = Relationship(back_populates='grades')
