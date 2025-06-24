from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from loguru import logger

from tgbot.models.models import Settings
from tgbot.services.repository import Repo
from tgbot.services.summary import SummaryChatService


async def input_summary_chat_handler(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,
):
    repo: Repo = manager.middleware_data.get("repo")
    summary: SummaryChatService = manager.middleware_data.get("summary")
    settings: Settings = await repo.get_settings(message.from_user.id)

    if settings is None:
        await message.answer(
            "<b>⚠️ Настройки не найдены. Попробуйте выполнить /start </b>",
            parse_mode=ParseMode.HTML,
        )
        return

    if not settings.summary_settings.api_key:
        await message.answer(
            "<b>⚠️ Сначала нужно установить api ключ! </b>",
            parse_mode=ParseMode.HTML,
        )
        return

    if not settings.summary_settings.base_url:
        await message.answer(
            "<b>⚠️ Сначала нужно выбрать сервер API! </b>",
            parse_mode=ParseMode.HTML,
        )
        return

    await message.answer(
        "<b>✍️ Пишем краткий пересказ...</b>",
        parse_mode=ParseMode.HTML,
    )

    async with ChatActionSender.typing(message.from_user.id, message.bot):
        logger.debug(f"Пользователь {message.from_user.id} запросил пересказ")
        summary_text = await summary.get_summary(
            base_url=settings.summary_settings.base_url,
            api_key=settings.summary_settings.api_key,
            url=message.text,
            summary_type=settings.summary_settings.summary_type,
        )
        await message.answer(summary_text)
