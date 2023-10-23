from aiogram.types import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Start
from aiogram_dialog.widgets.text import Const, Format

from tgbot.getters.base_data import get_base_data
from tgbot.misc.states import Main, Neural, Settings

main_dialog = Dialog(
    Window(
        # Главное окно
        Const("<b>Главный экран ChimpAI 🐵</b>\n"),
        Const("<b>🖥 Текущая конфигурация бота:</b>\n"),
        Format("🤖 Активная модель: <b>{model}</b>", when="model"),
        Format("🔋 Длина ответа: <b>{max_length}</b> токенов", when="max_length"),
        Format("🧠 Оригинальность ответа: <b>{temperature}</b>", when="temperature"),
        Format("🎭 Личность: <b>{personality}</b>", when="personality"),
        Row(
            Start(Const("🤖 Чат"), id="neural", state=Neural.chat),
            Start(Const("📝 Настройки"), id="settings", state=Settings.select),
        ),
        state=Main.main,
        getter=get_base_data,
        parse_mode=ParseMode.HTML,
    ),
)
