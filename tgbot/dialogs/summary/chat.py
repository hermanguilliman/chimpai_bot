from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row
from aiogram_dialog.widgets.text import Const, Format

from tgbot.callbacks.summary import toggle_summary_type
from tgbot.getters.summary import summary_data_getter
from tgbot.handlers.summary_chat import input_summary_chat_handler
from tgbot.misc.states import SummaryChat

summary_chat_dialog = Dialog(
    Window(
        Const("<b>📄 Yandex Пересказчик</b>\n"),
        Const("<b>Отправьте ссылку на статью или видео...</b>"),
        Format("Текущий формат пересказа {summary_type}", when="summary_type"),
        MessageInput(
            input_summary_chat_handler, content_types=[ContentType.TEXT]
        ),
        Row(
            Cancel(Const("👈 Назад")),
            Button(
                Const("🔄 Тип пересказа"),
                id="toggle_type",
                on_click=toggle_summary_type,
            ),
        ),
        state=SummaryChat.chat,
        parse_mode=ParseMode.HTML,
        getter=summary_data_getter,
    )
)
