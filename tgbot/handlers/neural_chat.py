from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from loguru import logger

from tgbot.models.personality import Personality
from tgbot.models.settings import Settings
from tgbot.services.repository import Repo
from tgbot.services.openai import OpenAIService


async def neural_handler(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
):
    repo: Repo = manager.middleware_data.get("repo")
    openai: OpenAIService = manager.middleware_data.get("openai")
    settings: Settings = await repo.get_settings(message.from_user.id)
    personality: Personality = await repo.get_personality(message.from_user.id)
    prompt: str = message.text

    if settings is None:
        await message.answer(
            "<b>⚠️ Настройки не найдены. Попробуйте выполнить /start </b>",
            parse_mode=ParseMode.HTML,
        )
        return
    if not settings.api_key:
        await message.answer(
            "<b>⚠️ Сначала нужно установить api ключ! </b>",
            parse_mode=ParseMode.HTML,
        )
        return

    if message.reply_to_message:
        prompt = f"{message.text}:\n{message.reply_to_message.text}"

    await message.answer(
        "<b>⌛️ Запрос отправлен. Ожидание ответа...</b>",
        parse_mode=ParseMode.HTML,
    )

    async with ChatActionSender.typing(message.from_user.id, message.bot):
        logger.debug("Создаём запрос к нейросети")
        ai_text_answer = await openai.get_answer(
            api_key=settings.api_key,
            max_tokens=int(settings.max_tokens),
            model=settings.model,
            temperature=float(settings.temperature),
            prompt=prompt,
            personality=personality,
        )

        if ai_text_answer:
            """выдача успешного запроса"""
            await message.reply(
                ai_text_answer, parse_mode=ParseMode.HTML
            )
            logger.debug("Ответ от нейросети получен")
        else:
            await message.answer(
                "<b>Что-то пошло не так, ответ от OpenAI не получен</b>",
                parse_mode=ParseMode.HTML,
            )
