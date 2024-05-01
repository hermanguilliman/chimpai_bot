from aiogram import F
from aiogram.enums import ParseMode, ContentType
from tgbot.handlers.api_key import api_key_handler
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Cancel,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from tgbot.getters.base_data import get_base_data
from tgbot.misc.states import ChatSettings, RootSettings, TTSSettings

# Диалог настроек
root_settings_dialog = Dialog(
    Window(
        # Окно выбора настроек
        Const("<b>🛠 Главное окно настроек 🛠</b>"),
        SwitchTo(
            Format("🔑API ключ установлен ✅ ", when="api_key"),
            id="set_api_key",
            state=RootSettings.api_key,
        ),
        SwitchTo(
            Const("🔑 API ключ отсутствует ⛔️", when=~F["api_key"]),
            id="set_api_key",
            state=RootSettings.api_key,
        ),
        Start(
            Const("💬 Настройки чата"),
            id="chat_setup",
            state=ChatSettings.select,
        ),
        Start(
            Const("🗣 Настройки TTS"),
            id="voice_setup",
            state=TTSSettings.select,
        ),
        Cancel(Const("🤚 Отмена")),
        state=RootSettings.select,
        parse_mode=ParseMode.HTML,
        getter=get_base_data,
    ),
    Window(
        # Установка нового ключа апи
        MessageInput(api_key_handler, content_types=[ContentType.TEXT]),
        Const("<b>Укажите новый API ключ:</b>"),
        Const("<b>Подсказка:</b> Ключ OpenAI API выглядит как <b>sk-...</b>"),
        Cancel(Const("🤚 Отмена")),
        state=RootSettings.api_key,
        parse_mode=ParseMode.HTML,
    ),
)
