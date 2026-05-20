from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class BaseTableModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)


class ORMBaseSchema(SQLModel):
    model_config = ConfigDict(from_attributes=True)


class TimestampedModel(BaseTableModel):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={'onupdate': datetime.utcnow},
    )


class BaseDeleteSchema(BaseTableModel):
    pass


class BasePublicSchema(BaseTableModel, ORMBaseSchema):
    pass


class TimestampedPublicSchema(TimestampedModel, ORMBaseSchema):
    pass
