from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from tgbot.handlers.transcription import voice_handler
from tgbot.misc.states import SpeechToText

speech_to_text_dialog = Dialog(
    Window(
        MessageInput(voice_handler, content_types=[ContentType.VOICE]),
        Const("<b>🎧 Speech to text - это перевод голоса в текст</b>\n"),
        Const("<b>Запишите или перешлите голосовое сообщение! 😀</b>\n"),
        Cancel(Const("👈 Назад")),
        state=SpeechToText.transcribe,
        parse_mode=ParseMode.HTML,
    ),
)
