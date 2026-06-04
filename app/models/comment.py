from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseDeleteSchema, TimestampedModel, TimestampedPublicSchema

if TYPE_CHECKING:
    from app.models.submission import Submission
    from app.models.user import User


class CommentBase(SQLModel):
    submission_id: int
    author_id: int
    content: str
    start_line_number: Optional[int] = None
    end_line_number: Optional[int] = None
    is_system_generated: bool = False


class Comment(CommentBase, TimestampedModel, table=True):
    __tablename__ = 'comments'

    submission_id: int = Field(foreign_key='submissions.id')
    author_id: int = Field(foreign_key='users.id')

    submission: 'Submission' = Relationship(back_populates='comments')
    author: 'User' = Relationship(back_populates='comments')


class CommentCreate(CommentBase):
    pass


class CommentUpdate(SQLModel):
    submission_id: Optional[int] = None
    author_id: Optional[int] = None
    content: Optional[str] = None
    start_line_number: Optional[int] = None
    end_line_number: Optional[int] = None
    is_system_generated: Optional[bool] = None


class CommentDelete(BaseDeleteSchema):
    pass


class CommentPublic(CommentBase, TimestampedPublicSchema):
    pass
