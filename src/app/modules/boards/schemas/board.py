from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BoardSchemaBase(BaseModel):
    title: str
    owner_id: int


class BoardSchemaCreate(BaseModel):
    title: str


class BoardSchemaUpdate(BoardSchemaBase):
    title: Optional[str] = None
    owner_id: Optional[int] = None


class BoardSchema(BoardSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
