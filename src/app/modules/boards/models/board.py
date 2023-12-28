from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, DateTime, func, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Board(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)

    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    owner: Mapped["User"] = relationship(back_populates="boards", lazy="selectin")

    columns: Mapped[List["BoardColumn"]] = relationship(back_populates="board", lazy="selectin")

    created_at = mapped_column(
        DateTime(timezone=True), default=datetime.now, server_default=func.now()
    )
    updated_at = mapped_column(
        DateTime(timezone=True), default=datetime.now, onupdate=func.now()
    )
