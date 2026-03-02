from typing import List, Optional
from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base
# TRUNCATE TABLE 
#     users, 
#     oauth_accounts, 
#     oauth_providers, 
#     posts, 
#     comments 
# RESTART IDENTITY CASCADE;

# INSERT INTO oauth_providers (provider) VALUES ('google'), ('facebook'), ('github');

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[Optional[str]] = mapped_column(String(32), unique=True, index=True, nullable=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=True)
    bio: Mapped[str] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
 
    oauth_accounts: Mapped[List["OAuthAccount"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
    posts: Mapped[List["Post"]] = relationship(
        back_populates="author", cascade="all, delete-orphan", passive_deletes=True
    )
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="author", cascade="all, delete-orphan", passive_deletes=True
    )


class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    provider_id: Mapped[int] = mapped_column(
        ForeignKey("oauth_providers.id", ondelete="CASCADE"), nullable=False
    )
    provider_user_id: Mapped[str] = mapped_column(String(255), nullable=False)

    provider: Mapped["OAuthProvider"] = relationship(back_populates="oauth_accounts")
    user: Mapped["User"] = relationship(back_populates="oauth_accounts")

    __table_args__ = (
        UniqueConstraint("provider_id", "provider_user_id", name="uq_provider_user"),
    )


class OAuthProvider(Base):
    __tablename__ = "oauth_providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider: Mapped[str] = mapped_column(String(16), nullable=False)
    
    oauth_accounts: Mapped[List["OAuthAccount"]] = relationship(
        back_populates="provider", cascade="all, delete-orphan", passive_deletes=True
    )


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="post", cascade="all, delete-orphan", passive_deletes=True
    )


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"), nullable=True
    )

    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")
    
    replies: Mapped[List["Comment"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan", passive_deletes=True
    )
    parent: Mapped[Optional["Comment"]] = relationship(
        remote_side=[id], back_populates="replies"
    )