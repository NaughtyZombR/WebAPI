from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskSchemaBase(BaseModel):
    title: str
    # author_id: int
    assignee_id: int
    board_column_id: int


class TaskSchemaCreate(TaskSchemaBase):
    pass


class TaskSchemaUpdate(TaskSchemaBase):
    title: Optional[str] = None
    # author_id: Optional[int] = None
    assignee_id: Optional[int] = None
    board_column_id: Optional[int] = None


class TaskSchema(TaskSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    author_id: int
    id: int
    created_at: datetime
    updated_at: datetime
