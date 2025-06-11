import datetime
import os
from tempfile import NamedTemporaryFile

from aiogram import types
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from tgbot.services.repository import Repo


async def clear_context(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    user_id = manager.bg()._event_context.user.id
    repo: Repo = manager.middleware_data.get("repo")
    await repo.clear_conversation_history(user_id)
    await callback.answer(
        "🗑 История беседы очищена!",
    )


async def download_history(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    user_id = manager.bg()._event_context.user.id
    repo: Repo = manager.middleware_data.get("repo")
    history = await repo.get_full_conversation_history(user_id)
    settings = await repo.get_settings(user_id)

    if not history:
        await callback.answer("Ваша история сообщений пуста")
        return

    # Форматирование в Markdown
    markdown_content = f"# История переписки с пользователем {user_id}\n"
    markdown_content += (
        f"## Настройки\n Личность: {settings.personality_name}\n"
    )
    markdown_content += f"Описание личности: {settings.personality_text}\n\n"
    for entry in history:
        timestamp = entry.created_at.strftime("%Y-%m-%d %H:%M:%S")
        role = "Пользователь" if entry.role == "user" else "ChimpAI"
        markdown_content += f"## {role} ({timestamp})\n\n{entry.content}\n\n"

    # Создаём временный файл
    with NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as temp_file:
        temp_file.write(markdown_content)
        temp_file_path = temp_file.name

    # Отправляем пользователю
    with open(temp_file_path, "rb") as file:
        input_file = types.BufferedInputFile(
            file.read(),
            filename=f"chimpai_history_{user_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        )
        await callback.bot.send_document(user_id, input_file)

    # Удаляем временный файл
    os.unlink(temp_file_path)
