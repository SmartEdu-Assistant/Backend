from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseDeleteSchema, TimestampedModel, TimestampedPublicSchema

if TYPE_CHECKING:
    from app.models.submission import Submission
    from app.models.user import User


class GradeBase(SQLModel):
    submission_id: int
    score: int
    max_score: int
    graded_by: int
    is_published: bool = False


class Grade(GradeBase, TimestampedModel, table=True):
    __tablename__ = 'grades'

    submission_id: int = Field(foreign_key='submissions.id', unique=True)
    graded_by: int = Field(foreign_key='users.id')

    submission: 'Submission' = Relationship(back_populates='grades')
    grader: 'User' = Relationship(back_populates='grades')


class GradeCreate(GradeBase):
    pass


class GradeUpdate(SQLModel):
    submission_id: Optional[int] = None
    score: Optional[int] = None
    max_score: Optional[int] = None
    graded_by: Optional[int] = None
    is_published: Optional[bool] = None


class GradeDelete(BaseDeleteSchema):
    pass


class GradePublic(GradeBase, TimestampedPublicSchema):
    pass
