from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskHistorySchemaBase(BaseModel):
    task_id: int
    previous_assignee_id: int
    new_assignee_id: int


class TaskHistorySchemaCreate(TaskHistorySchemaBase):
    pass


class TaskHistorySchemaUpdate(BaseModel):
    task_id: Optional[int] = None
    previous_assignee_id: Optional[int] = None
    new_assignee_id: Optional[int] = None


class TaskHistorySchema(TaskHistorySchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
