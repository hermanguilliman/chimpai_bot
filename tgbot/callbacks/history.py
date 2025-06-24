import datetime
import html
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
    callback: types.CallbackQuery, button: Button, manager: DialogManager
):
    user_id = manager.bg()._event_context.user.id
    repo: Repo = manager.middleware_data.get("repo")
    history = await repo.get_full_conversation_history(user_id)
    settings = await repo.get_settings(user_id)

    if not history:
        await callback.answer("Ваша история сообщений пуста")
        return

    # Форматирование в зависимости от export_format
    if settings.chat_settings.export_format == "markdown":
        content = f"# История переписки с пользователем {user_id}\n"
        content += f"## Настройки\nЛичность: {settings.chat_settings.personality_name}\n"
        content += (
            f"Описание личности: {settings.chat_settings.personality_text}\n\n"
        )
        for entry in history:
            timestamp = entry.created_at.strftime("%Y-%m-%d %H:%M:%S")
            role = "Пользователь" if entry.role == "user" else "ChimpAI"
            content += f"## {role} ({timestamp})\n\n{entry.content}\n\n"
        file_extension = ".md"
    else:  # html
        # Загружаем шаблон
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "templates",
            "chat_history_template.html",
        )
        with open(template_path, "r", encoding="utf-8") as template_file:
            template = template_file.read()

        # Формируем HTML для сообщений
        messages_html = ""
        for entry in history:
            timestamp = entry.created_at.strftime("%Y-%m-%d %H:%M:%S")
            role = "user" if entry.role == "user" else "assistant"
            avatar_text = "U" if role == "user" else "A"
            content = html.escape(
                entry.content
            )  # Экранируем содержимое для безопасности
            messages_html += f"""
                <div class="message {role}">
                    <div class="avatar">{avatar_text}</div>
                    <div class="message-content">
                        <p>{content}</p>
                        <div class="timestamp">{timestamp}</div>
                    </div>
                </div>
            """

        # Подставляем данные в шаблон
        content = template.format(
            user_id=user_id,
            personality_name=html.escape(
                settings.chat_settings.personality_name or ""
            ),
            personality_text=html.escape(
                settings.chat_settings.personality_text or ""
            ),
            messages=messages_html,
        )
        file_extension = ".html"

    # Создаём временный файл
    with NamedTemporaryFile(
        mode="w", suffix=file_extension, delete=False, encoding="utf-8"
    ) as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    # Отправляем пользователю
    with open(temp_file_path, "rb") as file:
        input_file = types.BufferedInputFile(
            file.read(),
            filename=f"chimpai_history_{user_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}",
        )
        await callback.bot.send_document(user_id, input_file)

    # Удаляем временный файл
    os.unlink(temp_file_path)
