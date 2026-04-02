from datetime import datetime, timezone

from sqlalchemy import Integer, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    hashed_password: Mapped[str] = mapped_column(String(255))

    analysis: Mapped[list["Analysis"]] = relationship(back_populates="user")

class Analysis(Base):
    __tablename__ = "analysis"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    video_id: Mapped[str] = mapped_column(String(20))
    video_title: Mapped[str] = mapped_column(String(500), nullable=True)
    analyzed_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates="analysis")
    comments: Mapped[list["Comment"]] = relationship(back_populates="analysis")

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("analysis.id"))
    comment_text: Mapped[str] = mapped_column(Text)
    like_count: Mapped[int] = mapped_column(default=0)
    reply_count: Mapped[int] = mapped_column(default=0)
    category: Mapped[str] = mapped_column(String(20))
    summary: Mapped[str] = mapped_column(Text)
    importance: Mapped[str] = mapped_column(String(10))

    analysis: Mapped["Analysis"] = relationship(back_populates="comments")