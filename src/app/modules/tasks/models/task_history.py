from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class TaskHistory(Base):
    __tablename__ = "task_histories"

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped["Task"] = relationship(back_populates="task_histories")
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    board_column_id: Mapped[int] = mapped_column(ForeignKey("board_columns.id"))
    previous_assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    new_assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    editor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, onupdate=func.now()
    )
