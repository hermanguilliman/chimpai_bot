from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Row, Start
from aiogram_dialog.widgets.text import Const, Format

from tgbot.getters.base_data import get_base_data
from tgbot.handlers.images import image_creator_handler
from tgbot.handlers.neural_chat import neural_handler
from tgbot.handlers.tts import tts_handler
from tgbot.handlers.transcription import voice_handler
from tgbot.handlers.voice_chatgpt import voice_to_chatgpt_handler
from tgbot.misc.states import Neural, ChatSettings, TTSSettings

neural_chat = Dialog(
    Window(
        Const("<b>🖥 Конфигурация чата:</b>\n"),

        Format(
            "🤖 Модель нейросети: <b>{model}</b>",
            when="model"
        ),

        Format(
            "🔋 Длина ответа: <b>{max_length}</b> токенов",
            when="max_length"
        ),

        Format(
            "🧠 Оригинальность ответа: <b>{temperature}</b>",
            when="temperature"
        ),

        Format(
            "🎭 Личность: <b>{personality}</b>",
            when="personality"
        ),

        Const("\n<b>Задай мне любой вопрос текстом или голосом 😎</b>"),

        # Инпут для голосового ввода запроса
        MessageInput(
            voice_to_chatgpt_handler,
            content_types=[ContentType.VOICE]),

        # Инпут для текстового ввода запроса
        MessageInput(
            neural_handler,
            content_types=[ContentType.TEXT]),

        Row(
            Cancel(
                Const("👈 Назад")),
            Start(
                Const("📝 Настройки чата"),
                id="settings",
                state=ChatSettings.select),
        ),
        state=Neural.chat,
        parse_mode=ParseMode.HTML,
        getter=get_base_data,
    ),
    Window(
        MessageInput(
            voice_handler,
            content_types=[ContentType.VOICE]
        ),
        Const("<b>🎧 Я могу транскрибировать любое голосовое сообщение!</b>\n"),
        Const("<b>Запишите или перешлите голосовое сообщение! 😀</b>\n"),
        Cancel(Const("👈 Назад")),
        state=Neural.transcribe,
        parse_mode=ParseMode.HTML,
    ),
    Window(
        MessageInput(image_creator_handler, content_types=[ContentType.TEXT]),
        Const("<b>🖌 DALL-E это нейросеть для создания изображений 😎</b>\n"),
        Const("<b>Опишите желаемое изображение, а я его нарисую!😉\n</b>"),
        Cancel(Const("👈 Назад")),
        state=Neural.image_create,
        parse_mode=ParseMode.HTML,
    ),
    Window(
        MessageInput(tts_handler, content_types=[ContentType.TEXT]),
        Const("<b>🗣 Технология TTS (Text to Speech) позволяет озвучить текст на любом языке.\n</b>"),
        Const("<b>Ваши настройки голоса:</b>"),
        Format("<b>Голос: {tts_voice}</b>"),
        Format("<b>Скорость произношения: {tts_speed}</b>\n"),
        Const("<b>🦜 Введите текст, который нужно озвучить!\n</b>"),
        Row(
            Cancel(Const("👈 Назад")),
            Start(
                Const("📝Настройки голоса"),
                id="voice_settings",
                state=TTSSettings.select
                ),
        ),
        getter=get_base_data,
        state=Neural.tts,
        parse_mode=ParseMode.HTML,
    ),
)
