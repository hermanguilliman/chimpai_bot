import os

from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from loguru import logger

from tgbot.models.settings import Settings
from tgbot.services.openai import OpenAIService
from tgbot.services.repository import Repo


async def voice_handler(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
):
    repo: Repo = manager.middleware_data.get("repo")
    openai: OpenAIService = manager.middleware_data.get("openai")
    settings: Settings = await repo.get_settings(message.from_user.id)
    if settings is None:
        await message.answer(
            "<b>⚠️ Настройки не найдены. Попробуйте выполнить /start</b>",
            parse_mode=ParseMode.HTML,
        )
        return
    if settings.api_key:
        async with ChatActionSender.typing(message.from_user.id, message.bot):
            logger.info("Пытаемся перевести войс в текст")
            file = await message.bot.get_file(message.voice.file_id)
            file_path = file.file_path
            local_path = f"voices/{message.from_user.id}.oga"
            await message.bot.download_file(file_path, local_path)
            text = await openai.audio_to_text(
                audio_path=local_path, api_key=settings.api_key
            )
            await message.reply(text)
            os.remove(local_path)
    else:
        await message.answer(
            "<b>⚠️ Сначала нужно установить api ключ!</b>",
            parse_mode=ParseMode.HTML,
        )
        return
