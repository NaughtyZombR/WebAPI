from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)

    board_column_id: Mapped[int] = mapped_column(ForeignKey("board_columns.id"))
    board_column: Mapped["BoardColumn"] = relationship(back_populates="tasks")

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    task_histories: Mapped[List["TaskHistory"]] = relationship(back_populates="task")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, onupdate=func.now()
    )
