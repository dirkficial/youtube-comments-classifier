from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(datetime.UTC))
    hashed_password: Mapped[str] = mapped_column(String(255))

    analysis: Mapped[list["Analysis"]] = relationship(back_popualtes="user")

class Analysis(Base):
    __tablename__ = "analysis"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    video_id: Mapped[str] = mapped_column(String(20))
    video_title: Mapped[str] = mapped_column(String(500), nullable=True)
    analyzed_at: Mapped[datetime] = mapped_column(default=datetime.now(datetime.UTC))

    user: Mapped["User"] = relationship(back_populates="analysis")
    comments: Mapped[list["Comment"]] = relationship(back_populates="analysis")

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("analyses.id"))
    comment_text: Mapped[str] = mapped_column(Text)
    like_count: Mapped[int] = mapped_column(default=0)
    reply_count: Mapped[int] = mapped_column(default=0)
    category: Mapped[str] = mapped_column(String(20))
    summary: Mapped[str] = mapped_column(Text)
    importance: Mapped[str] = mapped_column(String(10))

    analysis: Mapped["Analysis"] = relationship(back_populates="comments")