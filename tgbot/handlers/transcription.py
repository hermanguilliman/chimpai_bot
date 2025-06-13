import os
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


# Voice to Text
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
    if not settings.api_key:
        await message.answer(
            "<b>⚠️ Сначала нужно установить api ключ!</b>",
            parse_mode=ParseMode.HTML,
        )
        return
    elif not settings.base_url:
        await message.answer(
            "<b>⚠️ Сначала нужно выбрать сервер API!</b>",
            parse_mode=ParseMode.HTML,
        )
        return
    else:
        async with ChatActionSender.typing(message.from_user.id, message.bot):
            logger.info("Перевод голоса в текст")
            file = await message.bot.get_file(message.voice.file_id)
            file_path = file.file_path
            local_path = f"voices/{message.from_user.id}.oga"
            if os.path.exists(local_path):
                os.remove(local_path)

            await message.bot.download_file(file_path, local_path)
            text = await openai.audio_to_text(
                audio_path=local_path,
                base_url=settings.base_url,
                api_key=settings.api_key,
            )

            if text:
                text_chunks = split_text(text, 4000)

                # разбиваем длинные тексты на части
                for chunk in text_chunks:
                    await message.reply(chunk)
                    await sleep(1)
            else:
                await message.reply("Не получилось расшифровать сообщение")

            if os.path.exists(local_path):
                os.remove(local_path)
