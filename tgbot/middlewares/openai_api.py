from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from openai import AsyncOpenAI

from tgbot.services.neural import NeuralChatService


class OpenAIMiddleware(BaseMiddleware):
    def __init__(self, openai: AsyncOpenAI):
        self.openai = openai

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["openai"] = NeuralChatService(self.openai)
        return await handler(event, data)
