from aiogram.enums import ParseMode
from aiogram.types import Message, BufferedInputFile
from aiogram.utils.chat_action import ChatActionSender
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from loguru import logger

from tgbot.models.settings import Settings
from tgbot.services.repository import Repo
from tgbot.services.openai import OpenAIService


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


    await message.answer(
        "<b>⌛️ Запрос отправлен. Ожидание ответа...</b>",
        parse_mode=ParseMode.HTML,
    )

    async with ChatActionSender.record_voice(message.from_user.id, message.bot):
        logger.debug("Запрос для TTS")
        response = await openai.create_speech(
            model=settings.tts_model,
            voice=settings.tts_voice,
            speed=float(settings.tts_speed),
            prompt=prompt,
            api_key=settings.api_key,
        )

        if isinstance(response, bytes):
            """выдача успешного запроса"""
            await message.reply_voice(
                voice=BufferedInputFile(response, filename='voice.ogg'),
                parse_mode=ParseMode.HTML
            )
            logger.debug("Голосовое сообщение от нейросети получено")
        else:
            await message.answer(
                "<b>Что-то пошло не так!\n{response}</b>",
                parse_mode=ParseMode.HTML,
            )
