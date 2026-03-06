from typing import List
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base
from database.models._mixins import TimestampMixin


class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_public: Mapped[bool] = mapped_column(nullable=False)

    author: Mapped["User"] = relationship(back_populates="posts")  # type: ignore # noqa: F821
    comments: Mapped[List["Comment"]] = relationship(  # type: ignore # noqa: F821
        back_populates="post", cascade="all, delete-orphan", passive_deletes=True
    )

