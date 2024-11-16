from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tgbot.models.base import Base

if TYPE_CHECKING:
    from tgbot.models.user import Users


class CustomPersonality(Base):
    """Таблица для хранения пользовательских личностей"""

    __tablename__ = "custom_personality"

    id = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str]
    text: Mapped[str]
    user_id = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    user: Mapped["Users"] = relationship(back_populates="custom_personality")

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class BasicPersonality(Base):
    """Таблица для хранения стандартных личностей"""

    __tablename__ = "basic_personality"

    id = mapped_column(Integer, primary_key=True, unique=True)
    name = mapped_column(Text, unique=True)
    text: Mapped[str]

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"
