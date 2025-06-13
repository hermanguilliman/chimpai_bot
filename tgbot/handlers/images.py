from aiogram.enums import ParseMode
from aiogram.types import Message, URLInputFile
from aiogram.utils.chat_action import ChatActionSender
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from loguru import logger

from tgbot.models.models import Settings
from tgbot.services.neural import OpenAIService
from tgbot.services.repository import Repo


async def image_creator_handler(
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
        "<b>⌛️ Запрос на создание изображения принят. Ожидание ответа...</b>",
        parse_mode=ParseMode.HTML,
    )

    async with ChatActionSender.upload_photo(
        message.from_user.id, message.bot
    ):
        logger.debug("Создаём изображение с помощью нейросети")
        image_url = await openai.create_image(
            base_url=settings.base_url,
            api_key=settings.api_key,
            prompt=prompt,
        )

        if isinstance(image_url, str):
            if image_url.startswith("https://"):
                image_url = URLInputFile(image_url)

                """выдача изображения"""
                await message.reply_photo(
                    image_url,
                    caption=f"Изображение по запросу: {message.text}",
                    parse_mode=ParseMode.HTML,
                )
                logger.debug("Изображение от нейросети получено")
            else:
                await message.reply(
                    f"<b>Ответ нейросети:</b> {image_url}",
                    parse_mode=ParseMode.HTML,
                )
                logger.debug(image_url)
        else:
            await message.answer(
                "<b>Что-то пошло не так, ответ от OpenAI не получен</b>",
                parse_mode=ParseMode.HTML,
            )
