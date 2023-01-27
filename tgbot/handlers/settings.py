from aiogram import Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from tgbot.misc.states import Main, Settings
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from tgbot.services.repository import Repo

async def admin_settings(message: Message, state: FSMContext, repo: Repo):
    settings = await repo.get_user_settings(message.from_id)
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    model_button = InlineKeyboardButton(f'Модель: {settings.model}', callback_data='model')
    length_button = InlineKeyboardButton(f'Макс. длина: {settings.max_tokens}', callback_data='length')
    temp_button = InlineKeyboardButton(f'Температура: {settings.temperature}', callback_data='temperature')
    keyboard.add(model_button, length_button, temp_button)

    await Settings.summary.set()
    await message.answer("Какие параметры хотите изменить?", reply_markup=keyboard)


def register_admin_settings(dp: Dispatcher):
    dp.register_message_handler(
        admin_settings,
        commands=['settings'],
        state='*',
        is_admin=True
        )
