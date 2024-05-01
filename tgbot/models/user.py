import datetime

from sqlalchemy import BigInteger, Column, DateTime
from sqlalchemy.orm import relationship

from tgbot.models.base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    settings = relationship("Settings", back_populates="user")
    custom_personality = relationship(
        "CustomPersonality", back_populates="user")
