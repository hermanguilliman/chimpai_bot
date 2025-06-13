from aiogram.filters.state import State, StatesGroup


class MainMenu(StatesGroup):
    select = State()


class ChatGPT(StatesGroup):
    chat = State()


class SpeechToText(StatesGroup):
    transcribe = State()


class Dalle(StatesGroup):
    create_image = State()


class TextToSpeech(StatesGroup):
    tts = State()


class RootSettings(StatesGroup):
    select = State()
    api_key = State()


class ChatSettings(StatesGroup):
    select = State()
    model = State()
    max_length = State()
    temperature = State()


class PersonalitySettings(StatesGroup):
    basic_list = State()
    custom_list = State()
    custom_person_select = State()
    custom_person_edit_name = State()
    custom_person_edit_description = State()
    custom_person_delete_confirm = State()


class TTSSettings(StatesGroup):
    select = State()
    tts_model = State()
    tts_speed = State()
    tts_voice = State()


class NewPersonality(StatesGroup):
    name = State()
    text = State()


class BaseUrl(StatesGroup):
    select = State()
    input_base_url = State()
