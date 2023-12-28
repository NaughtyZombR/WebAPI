from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class TaskHistory(Base):
    __tablename__ = "task_histories"

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped["Task"] = relationship(back_populates="task_histories")
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    board_column_id: Mapped[int] = mapped_column(Integer)
    previous_assignee_id: Mapped[int] = mapped_column(Integer)
    new_assignee_id: Mapped[int] = mapped_column(Integer)
    editor_id: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, onupdate=func.now()
    )
