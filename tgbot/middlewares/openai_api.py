from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from tgbot.services.openai import OpenAIService


class OpenAIMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, openai):
        super().__init__()
        self.openai = openai
  
  
    async def pre_process(self, obj, data, *args):
        data["openai"] = OpenAIService(self.openai)

    async def post_process(self, obj, data, *args):
        del data["openai"]
