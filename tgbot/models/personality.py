from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from tgbot.models.base import Base


class CustomPersonality(Base):
    """ Таблица для хранения пользовательских личностей """
    __tablename__ = "custom_personality"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(Text())
    text = Column(Text())
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    user = relationship("Users", back_populates="custom_personality")

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class BasicPersonality(Base):
    """Таблица для хранения стандартных личностей"""
    __tablename__ = "basic_personality"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(Text(), unique=True)
    text = Column(Text())

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"
