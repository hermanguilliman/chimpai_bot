import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from tgbot.models.base import Base


class ConversationHistory(Base):
    __tablename__ = "conversation_history"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    role = mapped_column(String, nullable=False)
    content = mapped_column(String, nullable=False)
    created_at = mapped_column(DateTime, default=datetime.datetime.now)

    user = relationship("Users", back_populates="conversation_history")
