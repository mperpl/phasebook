from datetime import datetime
from typing import List, Optional
from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base
from database.models._mixins import TimestampMixin


class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), nullable=True
    )
    has_replies: Mapped[bool] = mapped_column(default=False, nullable=False)

    author: Mapped["User"] = relationship(back_populates="comments")  # type: ignore # noqa: F821
    post: Mapped["Post"] = relationship(back_populates="comments")  # type: ignore # noqa: F821
    
    replies: Mapped[List["Comment"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan", passive_deletes=True
    )
    parent: Mapped[Optional["Comment"]] = relationship(
        remote_side=[id], back_populates="replies"
    )