import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tgbot.models.base import Base

if TYPE_CHECKING:
    from tgbot.models.personality import CustomPersonality


class Users(Base):
    __tablename__ = "users"

    id = mapped_column(BigInteger, primary_key=True, unique=True)
    created_at = mapped_column(DateTime, default=datetime.datetime.now())
    settings = relationship("Settings", back_populates="user")
    custom_personality: Mapped[list["CustomPersonality"]] = relationship(
        back_populates="user"
    )
