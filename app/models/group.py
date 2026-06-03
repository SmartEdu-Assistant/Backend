from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseDeleteSchema, TimestampedModel, TimestampedPublicSchema

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.student import Student


class GroupBase(SQLModel):
    name: str = Field(max_length=100)
    semester: str = Field(max_length=50)
    year: int
    course_id: int


class Group(GroupBase, TimestampedModel, table=True):
    __tablename__ = 'groups'

    course_id: int = Field(foreign_key='courses.id')

    course: 'Course' = Relationship(back_populates='groups')
    students: list['Student'] = Relationship(back_populates='group')


class GroupCreate(GroupBase):
    pass


class GroupUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=100)
    semester: Optional[str] = Field(default=None, max_length=50)
    year: Optional[int] = None
    course_id: Optional[int] = None


class GroupDelete(BaseDeleteSchema):
    pass


class GroupPublic(GroupBase, TimestampedPublicSchema):
    pass
