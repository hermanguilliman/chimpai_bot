from aiogram.filters.state import State, StatesGroup


class Main(StatesGroup):
    main = State()


class Neural(StatesGroup):
    chat = State()
    transcribe = State()
    image_create = State()
    tts = State()


class RootSettings(StatesGroup):
    select = State()
    api_key = State()


class ChatSettings(StatesGroup):
    select = State()
    model = State()
    max_length = State()
    temperature = State()
    basic_personality_list = State()
    custom_personality_list = State()
    select_custom_personality = State()



class TTSSettings(StatesGroup):
    select = State()
    tts_model = State()
    tts_speed = State()
    tts_voice = State()


class Personality(StatesGroup):
    reset = State()
    name = State()
    text = State()
    finish = State()
