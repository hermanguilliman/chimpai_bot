import logging
import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 0.5):
        """
        Инициализация middleware
        :param rate_limit: минимальный интервал между сообщениями в секундах
        """
        super().__init__()
        self.rate_limit = rate_limit
        self.last_message: Dict[int, float] = {}  # user_id -> timestamp

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        # Получаем ID пользователя
        user_id = None
        if event.message:
            user_id = event.message.from_user.id
        elif event.callback_query:
            user_id = event.callback_query.from_user.id

        if user_id is None:
            return await handler(event, data)

        # Текущее время
        current_time = time.time()

        # Проверяем, есть ли пользователь в словаре и достаточно ли времени прошло
        if user_id in self.last_message:
            time_passed = current_time - self.last_message[user_id]

            if time_passed < self.rate_limit:
                # Слишком быстро, игнорируем
                logger.warning(
                    f"User {user_id} is throttled. "
                    f"Time passed: {time_passed:.2f} seconds"
                )
                if event.message:
                    await event.message.answer(
                        "<b>⚡️ Слишком много сообщений одновременно! Пожалуйста, подождите.</b>",
                        parse_mode="HTML",
                    )
                return None

        # Обновляем время последнего сообщения
        self.last_message[user_id] = current_time

        # Передаем управление следующему обработчику
        return await handler(event, data)
