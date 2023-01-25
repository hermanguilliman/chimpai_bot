from aiogram import Dispatcher
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from tgbot.misc.states import Main, Settings
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

async def admin_settings(message: Message, state: FSMContext):

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_model = KeyboardButton('Model')
    btn_max_lenght = KeyboardButton('Lenght')
    btn_temperature = KeyboardButton('Temperature')
    markup.add(btn_model, btn_max_lenght, btn_temperature)
    await Settings.summary.set()
    await message.answer("Какие параметры хотите изменить?", reply_markup=markup)


def register_admin_settings(dp: Dispatcher):
    dp.register_message_handler(
        admin_settings,
        Text(equals='Settings', ignore_case=True),
        state='*',
        is_admin=True
        )
