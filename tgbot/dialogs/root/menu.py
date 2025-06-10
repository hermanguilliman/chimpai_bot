from aiogram import F
from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Start
from aiogram_dialog.widgets.text import Const

from tgbot.getters.base_data import get_base_data
from tgbot.misc.states import (
    ChatGPT,
    Dalle,
    MainMenu,
    RootSettings,
    SpeechToText,
    TextToSpeech,
)

main_dialog = Dialog(
    Window(
        # Главное окно
        Const("<b>Главный экран ChimpAI 🐵</b>\n"),
        Start(
            Const("🚨 Ключ OpenAI отстутсвует! 🔑"),
            id="setup_api_key",
            state=RootSettings.api_key,
            when=~F["api_key"],
        ),
        Row(
            Start(Const("🤖 Нейро чат"), id="neural_chat", state=ChatGPT.chat),
            Start(Const("🎨 DALL-E"), id="dalle", state=Dalle.create_image),
        ),
        Row(
            Start(
                Const("🎧 Звук в текст"),
                id="voice_transcribe",
                state=SpeechToText.transcribe,
            ),
            Start(Const("🎙 Текст в звук"), id="tts", state=TextToSpeech.tts),
        ),
        Start(Const("📝 Настройки"), id="settings", state=RootSettings.select),
        state=MainMenu.select,
        getter=get_base_data,
        parse_mode=ParseMode.HTML,
    ),
)
