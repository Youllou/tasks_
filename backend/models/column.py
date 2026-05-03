import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Column(Base):
    __tablename__ = "columns"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str] = mapped_column(String(20), nullable=False, default="#8b8b9a")
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_inbox: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="columns")  # noqa: F821
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="column")  # noqa: F821

    __table_args__ = (
        # Partial unique index: enforces only one inbox column per user at the DB level
        Index(
            "uix_columns_user_inbox",
            "user_id",
            unique=True,
            postgresql_where=text("is_inbox = true"),
        ),
    )