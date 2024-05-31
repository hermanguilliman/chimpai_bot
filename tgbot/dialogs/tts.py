from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Row, Start
from aiogram_dialog.widgets.text import Const, Format

from tgbot.getters.base_data import get_base_data
from tgbot.handlers.tts import tts_handler
from tgbot.misc.states import TextToSpeech, TTSSettings


text_to_speech_dialog = Dialog(
    Window(
        MessageInput(tts_handler, content_types=[ContentType.TEXT]),
        Const(
            "<b>🗣 Text to speech - это озвучивание текста\n</b>"
        ),
        Format("<b>🦜 Выбранный голос: {tts_voice}</b>"),
        Format("<b>⏩ Скорость произношения: {tts_speed}</b>\n"),
        Const("<b>Введите текст, который нужно озвучить!\n</b>"),
        Row(
            Cancel(Const("👈 Назад")),
            Start(
                Const("📝Настройки голоса"),
                id="voice_settings",
                state=TTSSettings.select,
            ),
        ),
        getter=get_base_data,
        state=TextToSpeech.tts,
        parse_mode=ParseMode.HTML,
    )
)
