from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from tgbot.handlers.images import image_creator_handler
from tgbot.misc.states import Dalle

dalle_dialog = Dialog(
    Window(
        MessageInput(image_creator_handler, content_types=[ContentType.TEXT]),
        Const("<b>🎨 DALL-E 3 🖌</b>\n"),
        Const("<b>Опишите изображение, которое хотели бы получить</b>"),
        Cancel(Const("👈 Назад")),
        state=Dalle.create_image,
        parse_mode=ParseMode.HTML,
    ),
)
