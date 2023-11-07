from aiogram.filters.state import State, StatesGroup


class Main(StatesGroup):
    main = State()


class Neural(StatesGroup):
    chat = State()
    transcribe = State()
    image_create = State()


class Settings(StatesGroup):
    select = State()
    api_key = State()
    model = State()
    max_length = State()
    temperature = State()
    personality = State()


class Personality(StatesGroup):
    reset = State()
    name = State()
    text = State()
    finish = State()
