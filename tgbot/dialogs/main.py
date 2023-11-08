from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, Start
from aiogram_dialog.widgets.text import Const

from tgbot.getters.base_data import get_base_data
from tgbot.handlers.neural_chat import neural_handler
from tgbot.handlers.transcription import voice_handler
from tgbot.misc.states import Main, Neural, RootSettings

main_dialog = Dialog(
    Window(
        # Главное окно
        Const("<b>Главный экран ChimpAI 🐵</b>\n"),
        Row(
            Start(Const("🤖 Чат"), id="neural_chat", state=Neural.chat),
            Start(Const("🎨 Художник"), id="dalle", state=Neural.image_create),
        ),
        Row(
            Start(
                Const("🎧 Транскрибация"),
                id="voice_transcribe",
                state=Neural.transcribe,
            ),
            Start(Const("🎙 Озвучка"), id="tts", state=Neural.tts),
        ),
        Start(Const("📝 Настройки"), id="settings", state=RootSettings.select),
        # Короткий путь к текстовому запросу или расшифровке войса
        MessageInput(neural_handler, content_types=[ContentType.TEXT]),
        MessageInput(voice_handler, content_types=[ContentType.VOICE]),
        state=Main.main,
        getter=get_base_data,
        parse_mode=ParseMode.HTML,
    ),
)
