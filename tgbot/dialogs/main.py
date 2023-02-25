from tgbot.misc.states import Main, Settings, Neural
from tgbot.getters.base_data import get_base_data
from aiogram_dialog import Dialog, Window, Dialog
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Row, Start
from aiogram.types import ParseMode


main_dialog = Dialog(
    Window(
        # Главное окно
        Format("<b>{chimpai} 🐵 v0.2</b>\n"),
        Format('<b>Конфигурация prompt:</b>\n{model}/max:{max_length}/temp:{temperature}'),
        Row(                
            Start(Const("🤖 Нейро-Чат"), id='neural', state=Neural.chat),
            Start(Const("📝 Настройки"), id='settings', state=Settings.select),
        ),
        state=Main.main,
        getter=get_base_data,
        parse_mode=ParseMode.HTML,
    ),
)