from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseDeleteSchema, TimestampedModel, TimestampedPublicSchema

if TYPE_CHECKING:
    from app.models.submission import Submission


class PlagiarismReportBase(SQLModel):
    submission_id: int
    compared_with_id: int
    similarity_percent: float
    detected_blocks: Optional[str] = None


class PlagiarismReport(PlagiarismReportBase, TimestampedModel, table=True):
    __tablename__ = 'plagiarism_reports'

    submission_id: int = Field(foreign_key='submissions.id')
    compared_with_id: int = Field(foreign_key='submissions.id')

    submission: Optional['Submission'] = Relationship(back_populates='plagiarism_reports')
    compared_submission: Optional['Submission'] = Relationship(back_populates='compared_reports')


class PlagiarismReportCreate(PlagiarismReportBase):
    pass


class PlagiarismReportUpdate(SQLModel):
    submission_id: Optional[int] = None
    compared_with_id: Optional[int] = None
    similarity_percent: Optional[float] = None
    detected_blocks: Optional[str] = None


class PlagiarismReportDelete(BaseDeleteSchema):
    pass


class PlagiarismReportPublic(PlagiarismReportBase, TimestampedPublicSchema):
    pass
