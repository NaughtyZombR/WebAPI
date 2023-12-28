from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class BoardColumn(Base):
    __tablename__ = "board_columns"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)

    board_id: Mapped[int] = mapped_column(Integer, ForeignKey("boards.id"))
    board: Mapped["Board"] = relationship(back_populates="columns", lazy="selectin")

    tasks: Mapped[List["Task"]] = relationship(back_populates="board_column", lazy="selectin")

    created_at = mapped_column(
        DateTime(timezone=True), default=datetime.now, server_default=func.now()
    )
    updated_at = mapped_column(
        DateTime(timezone=True), default=datetime.now, onupdate=func.now()
    )
