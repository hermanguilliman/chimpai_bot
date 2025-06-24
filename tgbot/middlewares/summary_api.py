from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from tgbot.api.yandex_summary import YandexSummaryAPI
from tgbot.services.summary import SummaryChatService


class SummaryMiddleware(BaseMiddleware):
    def __init__(self, yandex_api: YandexSummaryAPI):
        self.yandex_api = yandex_api

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["summary"] = SummaryChatService(self.yandex_api)
        return await handler(event, data)
