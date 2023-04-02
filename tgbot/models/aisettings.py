from sqlalchemy import Column, Integer, Text, ForeignKey, String
from sqlalchemy.orm import relationship
from tgbot.models.base import Base


class AISettings(Base):
    __tablename__ = "ai_settings"

    id = Column(Integer, primary_key=True, unique=True)
    api_key = Column(String(51), nullable=True)
    max_tokens = Column(Integer(), default=256)
    model = Column(Text(), default='gpt-3.5-turbo')
    temperature = Column(Text(), default='0.7')
    personality_name = Column(Text(), nullable=True)
    personality_text = Column(Text(), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
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