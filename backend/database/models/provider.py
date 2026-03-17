from typing import List
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base


class OAuthProvider(Base):
    __tablename__ = "oauth_providers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    provider: Mapped[str] = mapped_column(String(16), nullable=False, unique=True)
    
    __table_args__ = (UniqueConstraint("provider", name="uq_oauth_providers_provider"),)

    oauth_accounts: Mapped[List["OAuthAccount"]] = relationship(back_populates="provider", cascade="all, delete-orphan", passive_deletes=True)  # noqa: F821 # type: ignore

