from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.services.openai import OpenAIService
from tgbot.services.repository import Repo
from tgbot.models.user import Users
from tgbot.models.aisettings import AISettings

async def answer_ai(message: types.Message, openai: OpenAIService, repo: Repo):
    settings = await repo.get_user_settings(message.from_id)
    await message.answer_chat_action(types.ChatActions.TYPING)
    
    ai_text_answer = await openai.get_answer(
        max_tokens=settings.max_tokens,
        model=settings.model,
        temperature=settings.temperature,
        prompt=message.text,
        )

    # ai_text_answer = await openai.get_answer(
    #     max_tokens=1024,
    #     model='text-davinci-003',
    #     temperature=0.7,
    #     prompt=message.text,
    #     )

    await message.answer(ai_text_answer)


def register_answer_ai(dp: Dispatcher):
    dp.register_message_handler(answer_ai, state="*", content_types=types.ContentTypes.ANY, is_admin=True)
