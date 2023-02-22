from tgbot.misc.states import Main
from tgbot.handlers.neural_chat import (
    get_main_data, 
    neural_handler, 
    show_settings
)
from aiogram_dialog import Dialog, Window, Dialog
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo, Back
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import ContentType, ParseMode


main_dialog = Dialog(
    Window(
        # Главное окно
        Format("<b>{chimpai} 🐵 v0.2</b>\n"),
        Format('<b>Конфигурация:</b>\n{model}/max:{max_length}/temp:{temperature}'),
        Row(                
            SwitchTo(Const("🤖 Нейро-Чат"), id='neural', state=Main.neural),
            Button(Const("📝 Настройки"), id='settings', on_click=show_settings),
        ),
        state=Main.main,
        getter=get_main_data,
        parse_mode=ParseMode.HTML,
    ),
    Window(
        MessageInput(neural_handler, content_types=[ContentType.TEXT]),
        Const("<b>🤖 Введите новый запрос:</b>"),
        Back(Const('↩️ Назад')),
        state=Main.neural,
        parse_mode=ParseMode.HTML,
    ),
)