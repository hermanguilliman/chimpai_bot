from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from tgbot.models.base import Base


class AISettings(Base):
    __tablename__ = "ai_settings"

    id = Column(Integer, primary_key=True, unique=True)
    max_tokens = Column(Integer(), default=256)
    model = Column(Text(), default='text-davinci-003')
    temperature = Column(Text(), default='0.7')
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