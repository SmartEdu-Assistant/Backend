from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseDeleteSchema, TimestampedModel, TimestampedPublicSchema

if TYPE_CHECKING:
    from app.models.assignment import Assignment
    from app.models.comment import Comment
    from app.models.grade import Grade
    from app.models.plagiarism_report import PlagiarismReport
    from app.models.student import Student
    from app.models.test_result import TestResult


class SubmissionBase(SQLModel):
    assignment_id: int
    student_id: int
    file_path: str = Field(max_length=500)


class Submission(SubmissionBase, TimestampedModel, table=True):
    __tablename__ = 'submissions'

    assignment_id: int = Field(foreign_key='assignments.id')
    student_id: int = Field(foreign_key='students.id')

    assignment: 'Assignment' = Relationship(back_populates='submissions')
    student: 'Student' = Relationship(back_populates='submissions')
    test_results: list['TestResult'] = Relationship(back_populates='submission')
    comments: list['Comment'] = Relationship(back_populates='submission')
    grades: list['Grade'] = Relationship(back_populates='submission')
    plagiarism_reports: list['PlagiarismReport'] = Relationship(
        back_populates='submission',
        sa_relationship_kwargs={'foreign_keys': '[PlagiarismReport.submission_id]'},
    )
    compared_reports: list['PlagiarismReport'] = Relationship(
        back_populates='compared_submission',
        sa_relationship_kwargs={'foreign_keys': '[PlagiarismReport.compared_with_id]'},
    )


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionUpdate(SQLModel):
    assignment_id: Optional[int] = None
    student_id: Optional[int] = None
    file_path: Optional[str] = Field(default=None, max_length=500)


class SubmissionDelete(BaseDeleteSchema):
    pass


class SubmissionPublic(SubmissionBase, TimestampedPublicSchema):
    pass
