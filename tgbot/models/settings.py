from sqlalchemy import Column, Integer, Text, ForeignKey, String
from sqlalchemy.orm import relationship
from tgbot.models.base import Base


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, unique=True)
    api_key = Column(String(51), nullable=True)
    max_tokens = Column(Integer(), default=256)
    model = Column(Text(), default='gpt-3.5-turbo')
    temperature = Column(Text(), default='0.7')
    tts_model = Column(String(), nullable=True, default='tts-1-hd')
    tts_speed = Column(String(), nullable=True, default='1.0')
    tts_voice = Column(String(), nullable=True, default='alloy')
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user = relationship("Users", back_populates="settings")

    def __str__(self):
        return f'''
        MaxTokens: {self.max_tokens}
        Model: {self.model}
        Temperature: {self.temperature}
        '''

    def __repr__(self):
        return f'''
        MaxTokens: {self.max_tokens}
        Model: {self.model}
        Temperature: {self.temperature}
        '''