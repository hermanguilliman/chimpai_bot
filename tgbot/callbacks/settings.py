from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from tgbot.services.repository import Repo
from aiogram.dispatcher.storage import FSMContext

# callback function to handle the button press
async def handle_settings_button_press(cb: CallbackQuery, repo: Repo, state: FSMContext):
    # get the data from the button press
    data = cb.data
    settings = await repo.get_user_settings(cb.from_user.id)
    if data == 'model':
        await cb.answer(settings.model)
        # use aiogram's Conversation feature to wait for the user's response
        # new_value = await cb.answer(chat_id=cb.from_user.id)
        # settings.model = new_value.text
        # await repo.set_new_model(new_value.text)
    elif data == 'length':
        await cb.answer(settings.max_tokens)
        # new_value = await cb.answer(chat_id=cb.from_user.id)
        # settings.max_tokens = int(new_value.text)
        # await repo.set_new_max_tokens(new_value.text)
    elif data == 'temperature':
        await cb.answer(settings.temperature)
        # new_value = await cb.answer(chat_id=cb.from_user.id)
        # settings.temperature = float(new_value.text)
        # await repo.set_new_temp(new_value.text)

# register the callback function to handle the button press
def register_settings_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(handle_settings_button_press, state="*")
