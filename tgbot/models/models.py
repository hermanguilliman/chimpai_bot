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
    shared_token = mapped_column(String(36), unique=True, index=True)
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
    """Таблица общих настроек"""

    __tablename__ = "settings"

    id = mapped_column(Integer, primary_key=True, unique=True)
    user_id = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    user = relationship("Users", back_populates="settings")
    chat_settings = relationship(
        "ChatSettings", uselist=False, back_populates="settings"
    )


class ChatSettings(Base):
    """Таблица настроек чата"""

    __tablename__ = "chat_settings"

    id = mapped_column(Integer, primary_key=True, unique=True)
    settings_id = mapped_column(
        Integer,
        ForeignKey("settings.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    api_key = mapped_column(String(51), nullable=True)
    base_url = mapped_column(
        String(255),
        nullable=False,
        default="https://api.openai.com/v1",
        server_default="https://api.openai.com/v1",
    )
    personality_name = mapped_column(
        Text, nullable=True, default="🤵 Ассистент"
    )
    personality_text = mapped_column(
        Text,
        nullable=True,
        default="Действуй как личный ассистент пользователя",
    )
    export_format = mapped_column(
        String(10),
        nullable=False,
        default="markdown",
        server_default="markdown",
    )
    model = mapped_column(Text, default="gpt-4o-mini")
    max_tokens = mapped_column(Integer, default=1000)
    temperature = mapped_column(Text, default="0.7")
    settings = relationship("Settings", back_populates="chat_settings")


class Users(Base):
    """Таблица пользователей"""

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


if __name__ == "__main__":
    from eralchemy import render_er

    render_er(Base, "diagram.png")
