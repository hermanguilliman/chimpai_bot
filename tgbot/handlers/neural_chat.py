from asyncio import sleep
from html import escape

from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from loguru import logger

from tgbot.misc.text_tools import split_text
from tgbot.models.models import Settings
from tgbot.services.neural import NeuralChatService
from tgbot.services.repository.history import ConversationHistoryService
from tgbot.services.repository.settings import SettingsService


async def input_text_chat_handler(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
):
    prompt: str = message.text
    settings_service: SettingsService = manager.middleware_data.get(
        "settings_service"
    )
    conversation_service: ConversationHistoryService = (
        manager.middleware_data.get("conversation_service")
    )
    openai: NeuralChatService = manager.middleware_data.get("openai")
    settings: Settings = await settings_service.get_settings(
        message.from_user.id
    )

    if settings is None:
        await message.answer(
            "<b>⚠️ Настройки не найдены. Попробуйте выполнить /start </b>",
            parse_mode=ParseMode.HTML,
        )
        return

    if not settings.chat_settings.api_key:
        await message.answer(
            "<b>⚠️ Сначала нужно установить api ключ! </b>",
            parse_mode=ParseMode.HTML,
        )
        return

    if not settings.chat_settings.base_url:
        await message.answer(
            "<b>⚠️ Сначала нужно выбрать сервер API! </b>",
            parse_mode=ParseMode.HTML,
        )
        return

    # Получаем последние 10 сообщений из истории
    history = await conversation_service.get_conversation_history(
        message.from_user.id, limit=15
    )

    # Добавляем запрос пользователя в историю
    await conversation_service.add_message_to_history(
        user_id=message.from_user.id, role="user", content=prompt
    )

    await message.answer(
        "<b>⌛️ Запрос отправлен. Ожидание ответа...</b>",
        parse_mode=ParseMode.HTML,
    )

    async with ChatActionSender.typing(message.from_user.id, message.bot):
        logger.debug(f"Пользователь {message.from_user.id} отправил запрос")
        answer = await openai.get_answer(
            base_url=settings.chat_settings.base_url,
            api_key=settings.chat_settings.api_key,
            max_tokens=int(settings.chat_settings.max_tokens),
            model=settings.chat_settings.model,
            temperature=float(settings.chat_settings.temperature),
            prompt=prompt,
            person_text=settings.chat_settings.personality_text,
            history=history,
        )

        if answer:
            # Добавляем ответ бота в историю
            await conversation_service.add_message_to_history(
                user_id=message.from_user.id, role="assistant", content=answer
            )

            text_chunks = split_text(answer, 4000)
            for chunk in text_chunks:
                try:
                    await message.reply(
                        escape(chunk), parse_mode=ParseMode.HTML
                    )
                    await sleep(1)
                except Exception as e:
                    logger.critical(f"Неожиданная ошибка: {e}")
                logger.debug("Сообщение с ответом отправлено")
        else:
            await message.answer(
                "<b>Что-то пошло не так, ответ не получен</b>",
                parse_mode=ParseMode.HTML,
            )
