from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[Optional[str]] = mapped_column(String(32), unique=True, index=True, nullable=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=True)
    bio: Mapped[str] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
 
    oauth_accounts: Mapped[List["OAuthAccount"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
    posts: Mapped[List["Post"]] = relationship(  # noqa: F821 # type: ignore
        back_populates="author", cascade="all, delete-orphan", passive_deletes=True
    )
    comments: Mapped[List["Comment"]] = relationship(  # noqa: F821 # type: ignore
        back_populates="author", cascade="all, delete-orphan", passive_deletes=True
    )


class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    provider_id: Mapped[int] = mapped_column(
        ForeignKey("oauth_providers.id", ondelete="CASCADE"), nullable=False
    )
    provider_user_id: Mapped[str] = mapped_column(String(255), nullable=False)

    provider: Mapped["OAuthProvider"] = relationship(back_populates="oauth_accounts")  # type: ignore # noqa: F821
    user: Mapped["User"] = relationship(back_populates="oauth_accounts")

    __table_args__ = (
        UniqueConstraint("provider_id", "provider_user_id", name="uq_provider_user"),
    )



