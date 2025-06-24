from aiogram.filters.state import State, StatesGroup


class MainMenu(StatesGroup):
    select = State()


class NeuralChat(StatesGroup):
    chat = State()


class SummaryChat(StatesGroup):
    chat = State()


class SystemSettings(StatesGroup):
    select = State()


class SetupСhatService(StatesGroup):
    select = State()
    api_key = State()
    base_url = State()
    input_base_url = State()


class SetupSummaryService(StatesGroup):
    select = State()
    api_key = State()
    base_url = State()


class NeuralChatSettings(StatesGroup):
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


class NewPersonality(StatesGroup):
    name = State()
    text = State()


class BaseUrl(StatesGroup):
    select = State()
    input_base_url = State()
