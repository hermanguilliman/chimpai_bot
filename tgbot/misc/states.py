
from aiogram.dispatcher.filters.state import State, StatesGroup


class Main(StatesGroup):
    main = State()
    neural = State()


class Settings(StatesGroup):
    select = State()
    api_key = State()
    model = State()
    max_length = State()
    temperature = State()