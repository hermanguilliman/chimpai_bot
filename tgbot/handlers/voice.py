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


# Voice to ChatGPT
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

    async with ChatActionSender.typing(message.from_user.id, message.bot):
        logger.info("Перевод голоса в текст")
        file = await message.bot.get_file(message.voice.file_id)
        file_path = file.file_path
        local_path = f"voices/{message.from_user.id}.oga"
        if os.path.exists(local_path):
            os.remove(local_path)

        await message.bot.download_file(file_path, local_path)
        text = await openai.audio_to_text(
            base_url=settings.base_url,
            api_key=settings.api_key,
            audio_path=local_path,
        )
        if text:
            await message.reply(
                f"<b>🎧 Вот, что я услышал:</b>\n\n{text[:4000]}",
                parse_mode=ParseMode.HTML,
            )
            answer = await openai.get_answer(
                base_url=settings.base_url,
                api_key=settings.api_key,
                model=settings.model,
                prompt=text,
                max_tokens=int(settings.max_tokens),
                temperature=float(settings.temperature),
                person_text=settings.personality_text,
            )

            if answer:
                text_chunks = split_text(answer, 4000)
                # разбиваем длинные тексты на части
                for chunk in text_chunks:
                    try:
                        await message.reply(
                            chunk, parse_mode=ParseMode.MARKDOWN
                        )
                        await sleep(1)

                        logger.debug("Ответ от нейросети получен")
                    except Exception:
                        await message.reply(chunk, parse_mode=ParseMode.HTML)
                        await sleep(1)

                await sleep(1)
                logger.debug("Ответ от нейросети получен")
            else:
                await message.reply(
                    "<b>К сожалению ответ от нейросети не получен</b>",
                    parse_mode=ParseMode.HTML,
                )
        else:
            await message.reply(
                "<b>К сожалению не получилось расшифровать сообщение</b>",
                parse_mode=ParseMode.HTML,
            )

        if os.path.exists(local_path):
            os.remove(local_path)
