import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ConversationHistory(Base):
    __tablename__ = "conversation_history"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    role = mapped_column(String, nullable=False)
    content = mapped_column(String, nullable=False)
    created_at = mapped_column(DateTime, default=datetime.datetime.now)

    user = relationship("Users", back_populates="conversation_history")


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


class BaseUrl(Base):
    __tablename__ = "base_urls"
    """Таблица для хранения стандартных адресов API"""

    id = mapped_column(Integer, primary_key=True, unique=True)
    name = mapped_column(Text, unique=True)
    url = mapped_column(Text, unique=True, nullable=False)

    def __repr__(self):
        return f"<BaseUrl(id={self.id}, name='{self.name}', url='{self.url}')>"


class Settings(Base):
    __tablename__ = "settings"

    id = mapped_column(Integer, primary_key=True, unique=True)
    api_key = mapped_column(String(51), nullable=True)
    base_url = mapped_column(
        String(255), nullable=False, server_default="https://api.openai.com/v1"
    )
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


class Users(Base):
    __tablename__ = "users"

    id = mapped_column(BigInteger, primary_key=True, unique=True)
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    settings = relationship("Settings", back_populates="user")
    conversation_history = relationship(
        "ConversationHistory", back_populates="user"
    )
    custom_personality: Mapped[list["CustomPersonality"]] = relationship(
        back_populates="user"
    )
