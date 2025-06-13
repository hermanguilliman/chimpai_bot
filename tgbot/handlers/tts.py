from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile, Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from loguru import logger

from tgbot.models.models import Settings
from tgbot.services.neural import OpenAIService
from tgbot.services.repository import Repo


async def tts_handler(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
):
    repo: Repo = manager.middleware_data.get("repo")
    openai: OpenAIService = manager.middleware_data.get("openai")
    settings: Settings = await repo.get_settings(message.from_user.id)
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

    if not settings.base_url:
        await message.answer(
            "<b>⚠️ Сначала нужно выбрать сервер API! </b>",
            parse_mode=ParseMode.HTML,
        )
        return

    await message.answer(
        "<b>⌛️ Запрос отправлен. Ожидание ответа...</b>",
        parse_mode=ParseMode.HTML,
    )

    async with ChatActionSender.record_voice(
        message.from_user.id, message.bot
    ):
        logger.debug("Запрос для TTS")
        response = await openai.create_speech(
            prompt=prompt,
            base_url=settings.base_url,
            api_key=settings.api_key,
            model=settings.tts_model,
            voice=settings.tts_voice,
            speed=float(settings.tts_speed),
        )

        if isinstance(response, bytes):
            """выдача успешного запроса"""
            await message.reply_voice(
                voice=BufferedInputFile(response, filename="voice.ogg"),
                parse_mode=ParseMode.HTML,
            )
            logger.debug("Голосовое сообщение от нейросети получено")
        else:
            await message.answer(
                "<b>Произошла ошибка генерации речи</b>",
                parse_mode=ParseMode.HTML,
            )
