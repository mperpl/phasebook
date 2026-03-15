from enum import Enum
from sqlalchemy import CheckConstraint, ForeignKey, Enum as sqlEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models._mixins import TimestampMixin
from database.models.base import Base


class FriendshipStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"


class Friendship(Base, TimestampMixin):
    __tablename__ = "friendship"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=True)
    status: Mapped[FriendshipStatus] = mapped_column(sqlEnum(FriendshipStatus), default=FriendshipStatus.PENDING, nullable=False)
    action_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
 
    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_id], back_populates="sent_requests")  # noqa: F821 # type: ignore
    receiver: Mapped["User"] = relationship("User", foreign_keys=[receiver_id], back_populates="received_requests")  # noqa: F821 # type: ignore

    __table_args__ = (
        UniqueConstraint("sender_id", "receiver_id", name="uq_friendship_sender_receiver"),
        CheckConstraint("sender_id != receiver_id", name="check_no_self_friend"),
    )