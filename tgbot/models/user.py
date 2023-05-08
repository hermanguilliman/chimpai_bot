import datetime
from sqlalchemy import Column, Integer, BigInteger, Text, ForeignKey, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from tgbot.models.base import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, unique=True)
    full_name = Column(Text(250))
    registration_date = Column(DateTime, default=datetime.datetime.now())
    language_code = Column(Text(3))
    settings = relationship("Settings", back_populates="user")
    personality = relationship("Personality", back_populates="user")

    def is_new_user(self) -> bool:
        return self.registration_date >= (datetime.datetime.now() - datetime.timedelta(minutes=1))

    def __str__(self):
        return f"UserID: {self.id} User: {self.full_name} Join date: {self.registration_date}"

    def __repr__(self):
        return f"UserID: {self.id} User: {self.full_name} Join date: {self.registration_date}"