from asyncio import sleep

from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from loguru import logger

from tgbot.misc.text_tools import split_text
from tgbot.models.models import Settings
from tgbot.services.neural import OpenAIService
from tgbot.services.repository import Repo


async def input_text_chat_handler(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
):
    prompt: str = message.text
    repo: Repo = manager.middleware_data.get("repo")
    openai: OpenAIService = manager.middleware_data.get("openai")
    settings: Settings = await repo.get_settings(message.from_user.id)

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

    if not settings.base_url:
        await message.answer(
            "<b>⚠️ Сначала нужно выбрать сервер API! </b>",
            parse_mode=ParseMode.HTML,
        )
        return

    # Получаем последние 10 сообщений из истории
    history = await repo.get_conversation_history(
        message.from_user.id, limit=15
    )

    # Добавляем запрос пользователя в историю
    await repo.add_message_to_history(
        user_id=message.from_user.id, role="user", content=prompt
    )

    await message.answer(
        "<b>⌛️ Запрос отправлен. Ожидание ответа...</b>",
        parse_mode=ParseMode.HTML,
    )

    async with ChatActionSender.typing(message.from_user.id, message.bot):
        logger.debug(f"Пользователь {message.from_user.id} отправил запрос")
        answer = await openai.get_answer(
            base_url=settings.base_url,
            api_key=settings.api_key,
            max_tokens=int(settings.max_tokens),
            model=settings.model,
            temperature=float(settings.temperature),
            prompt=prompt,
            person_text=settings.personality_text,
            history=history,
        )

        if answer:
            # Добавляем ответ бота в историю
            await repo.add_message_to_history(
                user_id=message.from_user.id, role="assistant", content=answer
            )

            text_chunks = split_text(answer, 4000)
            for chunk in text_chunks:
                try:
                    await message.reply(chunk, parse_mode=ParseMode.MARKDOWN)
                    await sleep(1)
                    logger.debug("Ответ от нейросети получен")
                except Exception:
                    await message.reply(chunk, parse_mode=ParseMode.HTML)
                    await sleep(1)
                    logger.debug("Ответ от нейросети получен")
        else:
            await message.answer(
                "<b>Что-то пошло не так, ответ от OpenAI не получен</b>",
                parse_mode=ParseMode.HTML,
            )
