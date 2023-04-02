from tgbot.misc.states import Main, Settings, Neural
from tgbot.getters.base_data import get_base_data
from aiogram_dialog import Dialog, Window, Dialog
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Row, Start, Group
from aiogram.types import ParseMode, ContentType


main_dialog = Dialog(
    Window(
        # Главное окно
        Const("<b>Главный экран ChimpAI 🐵</b>\n"),
        Const('<b>🖥 Текущая конфигурация бота:</b>\n'),
        Format('🤖 Активная модель: <b>{model}</b>', when='model'),
        Format('🔋 Длина ответа: <b>{max_length}</b> токенов', when='max_length'),
        Format('🧠 Оригинальность ответа: <b>{temperature}</b>', when='temperature'),
        Format('🎭 Личность: <b>{personality_name}</b>', when='personality_name'),
        Row(                
            Start(Const("🤖 Чат"), id='neural', state=Neural.chat),
            Start(Const("📝 Настройки"), id='settings', state=Settings.select),
        ),
        state=Main.main,
        getter=get_base_data,
        parse_mode=ParseMode.HTML,
    ),
)