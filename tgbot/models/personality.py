from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from tgbot.models.base import Base


class Personality(Base):
    __tablename__ = "personality"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(Text(), nullable=True)
    text = Column(Text(), nullable=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    user = relationship("Users", back_populates="personality")

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"
