from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseTableModel, ORMBaseSchema

if TYPE_CHECKING:
    from app.models.submission import Submission
    from app.models.user import User


class GradeBase(SQLModel):
    submission_id: int
    score: int
    max_score: int
    graded_by: int
    is_published: bool = False


class Grade(GradeBase, BaseTableModel, table=True):
    __tablename__ = 'grades'

    submission_id: int = Field(foreign_key='submissions.id', unique=True)
    graded_by: int = Field(foreign_key='users.id')
    graded_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    submission: Optional['Submission'] = Relationship(back_populates='grades')
    grader: Optional['User'] = Relationship(back_populates='grades')


class GradeCreate(GradeBase):
    pass


class GradeUpdate(SQLModel):
    submission_id: Optional[int] = None
    score: Optional[int] = None
    max_score: Optional[int] = None
    graded_by: Optional[int] = None
    is_published: Optional[bool] = None


class GradeDelete(SQLModel):
    id: int


class GradePublic(GradeBase, ORMBaseSchema):
    id: int
    graded_at: datetime
