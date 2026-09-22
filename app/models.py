from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    amount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    note: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )