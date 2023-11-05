from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.formatting import Text, Bold
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from loguru import logger
import os
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
            Text(Bold("⚠️ Настройки не найдены. Попробуйте выполнить /start")),
            parse_mode=ParseMode.MARKDOWN,
        )
        return
    if not settings.api_key:
        await message.answer(
            Text(Bold("⚠️ Сначала нужно установить api ключ!")),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    async with ChatActionSender.typing(message.from_user.id, message.bot):
        logger.info("Пытаемся перевести войс в текст")
        file = await message.bot.get_file(message.voice.file_id)
        file_path = file.file_path
        local_path = f"voices/{message.from_user.id}.oga"
        await message.bot.download_file(file_path, local_path)
        text = await openai.audio_to_text(
            audio_path=local_path,
            api_key=settings.api_key)
        await message.reply(text)
        os.remove(local_path)
