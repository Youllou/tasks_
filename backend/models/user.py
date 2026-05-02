import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    github_id: Mapped[str | None] = mapped_column(String, nullable=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user", cascade="all, delete-orphan")  # noqa: F821
    tags: Mapped[list["Tag"]] = relationship("Tag", back_populates="user", cascade="all, delete-orphan")  # noqa: F821
    projects: Mapped[list["Project"]] = relationship("Project", back_populates="user", cascade="all, delete-orphan")  # noqa: F821