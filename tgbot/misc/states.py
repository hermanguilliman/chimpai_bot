from aiogram.dispatcher.filters.state import State, StatesGroup


class Main(StatesGroup):
    chat = State()


class Settings(StatesGroup):
    summary = State()
    model = State()
    max_lenght = State()
    temperature = State()