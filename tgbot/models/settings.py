from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship

from tgbot.models.base import Base


class Settings(Base):
    __tablename__ = "settings"

    id = mapped_column(Integer, primary_key=True, unique=True)
    api_key = mapped_column(String(51), nullable=True)
    personality_name = mapped_column(
        Text, nullable=True, default="🤵 Ассистент"
    )
    personality_text = mapped_column(
        Text,
        nullable=True,
        default="Действуй как личный ассистент пользователя",
    )
    max_tokens = mapped_column(Integer, default=1000)
    model = mapped_column(Text, default="gpt-4o-mini")
    temperature = mapped_column(Text, default="0.7")
    tts_model = mapped_column(String, nullable=True, default="tts-1-hd")
    tts_speed = mapped_column(String, nullable=True, default="1.0")
    tts_voice = mapped_column(String, nullable=True, default="alloy")
    user_id = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    user = relationship("Users", back_populates="settings")

    def __str__(self):
        return f"""
        MaxTokens: {self.max_tokens}
        Model: {self.model}
        Temperature: {self.temperature}
        """

    def __repr__(self):
        return f"""
        MaxTokens: {self.max_tokens}
        Model: {self.model}
        Temperature: {self.temperature}
        """
