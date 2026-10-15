from typing import Optional
from datetime import datetime
from sqlalchemy import CheckConstraint, Date, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

STATUS = ("applied", "interview")
ALLOWED_KEYS = ("company", "title", "date_applied", "status", "date_interview")

class Base(DeclarativeBase):
    pass

class Application(Base):
    __tablename__ = "applications"

    # Columns
    # Implicit not null
    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text)

    # Default value is generated automatically by the DB (server-side) (date)
    date_applied: Mapped[Date] = mapped_column(Date, server_default=func.current_date())
    status: Mapped[str] = mapped_column(Text)

    # Optional = can be null
    date_interview: Mapped[Optional[Date]]

    __table_args__ = (
        CheckConstraint(f"status in {str(STATUS)}", name="check_status_validity"),
    )