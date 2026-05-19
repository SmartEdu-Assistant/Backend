from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import ORMBaseSchema, TimestampedModel

if TYPE_CHECKING:
    from app.models.group import Group
    from app.models.submission import Submission


class StudentBase(SQLModel):
    full_name: str = Field(max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    group_id: int


class Student(StudentBase, TimestampedModel, table=True):
    __tablename__ = 'students'

    group_id: int = Field(foreign_key='groups.id')

    group: Optional['Group'] = Relationship(back_populates='students')
    submissions: list['Submission'] = Relationship(back_populates='student')


class StudentCreate(StudentBase):
    pass


class StudentUpdate(SQLModel):
    full_name: Optional[str] = Field(default=None, max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    group_id: Optional[int] = None


class StudentDelete(SQLModel):
    id: int


class StudentPublic(StudentBase, ORMBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
