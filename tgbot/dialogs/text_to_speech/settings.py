from aiogram.enums import ParseMode
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Group,
    Select,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from tgbot.callbacks.tts_settings import (
    on_big_decrease_tts_speed,
    on_big_increase_tts_speed,
    on_decrease_tts_speed,
    on_increase_tts_speed,
    on_reset_tts_speed,
    on_tts_speed_selected,
    on_tts_voice_selected,
)
from tgbot.getters.base_data import get_base_data
from tgbot.getters.tts_settings import get_tts_speed, voices_names_getter
from tgbot.misc.states import TTSSettings

tts_settings_dialog = Dialog(
    Window(
        Const("<b>🦜 Настройки генерации голоса 🦜</b>"),
        SwitchTo(
            Format("👺 Голос: {tts_voice}"),
            id="tts_voice_switch",
            state=TTSSettings.tts_voice,
            when="tts_voice",
        ),
        SwitchTo(
            Format("⏩ Скорость произношения: {tts_speed}"),
            id="tts_speed_switch",
            state=TTSSettings.tts_speed,
            when="tts_speed",
        ),
        Cancel(Const("👈 Назад")),
        state=TTSSettings.select,
        parse_mode=ParseMode.HTML,
        getter=get_base_data,
    ),
    Window(
        # Выбор голоса
        Const("<b>🦜 Настройка голоса озвучки:</b>"),
        Group(
            Select(
                Format("👺 {item}"),
                items="tts_voices",
                item_id_getter=lambda x: x,
                id="select_voice",
                on_click=on_tts_voice_selected,
            ),
            width=2,
        ),
        SwitchTo(
            Const("👈 Назад"),
            id="back_to_tts_menu",
            state=TTSSettings.select,
        ),
        state=TTSSettings.tts_voice,
        parse_mode=ParseMode.HTML,
        getter=voices_names_getter,
    ),
    Window(
        Const("<b>⏩ Настройка скорости произношения</b>"),
        Group(
            Button(
                Format("✅ Установить скорость: {tts_speed}"),
                id="new_tts_speed",
                when="tts_speed",
                on_click=on_tts_speed_selected,
            ),
            width=1,
        ),
        Group(
            Button(
                Const("🔻 0.1"), id="decrease", on_click=on_decrease_tts_speed
            ),
            Button(
                Const("0.1 🔺"), id="increase", on_click=on_increase_tts_speed
            ),
            width=2,
        ),
        Group(
            Button(
                Const("🔻 0.5"),
                id="big_decrease",
                on_click=on_big_decrease_tts_speed,
            ),
            Button(
                Const("0.5 🔺"),
                id="big_increase",
                on_click=on_big_increase_tts_speed,
            ),
            width=2,
        ),
        Group(
            Button(
                Const("🌚 Как было"),
                id="reset_tts_speed",
                on_click=on_reset_tts_speed,
            ),
            SwitchTo(
                Const("👈 Назад"),
                id="back_to_tts_menu",
                state=TTSSettings.select,
            ),
            width=2,
        ),
        state=TTSSettings.tts_speed,
        parse_mode=ParseMode.HTML,
        getter=get_tts_speed,
    ),
)
