from datetime import date
from sqlalchemy import CheckConstraint, Date, Text, func
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
    date_applied: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    status: Mapped[str] = mapped_column(Text)

    # Can be null
    date_interview: Mapped[date | None]

    __table_args__ = (
        CheckConstraint(status.in_(STATUS), name="check_status_validity"),
    )