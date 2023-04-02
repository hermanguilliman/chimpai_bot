
from aiogram.dispatcher.filters.state import State, StatesGroup


class Main(StatesGroup):
    main = State()


class Neural(StatesGroup):
    chat = State()


class Settings(StatesGroup):
    select = State()
    api_key = State()
    model = State()
    max_length = State()
    temperature = State()
    personality = State()

class Personality(StatesGroup):
    name = State()
    text = State()
    finish = State()