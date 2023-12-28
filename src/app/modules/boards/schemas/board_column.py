from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BoardColumnSchemaBase(BaseModel):
    title: str
    board_id: int


class BoardColumnSchemaCreate(BoardColumnSchemaBase):
    pass


class BoardColumnSchemaUpdate(BoardColumnSchemaBase):
    title: Optional[str] = None
    board_id: Optional[int] = None


class BoardColumnSchema(BoardColumnSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
