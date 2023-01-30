from aiogram import types, Dispatcher
from tgbot.services.openai import OpenAIService
from tgbot.services.repository import Repo
from tgbot.models.aisettings import AISettings

async def answer_ai(message: types.Message, openai: OpenAIService, repo: Repo):
    settings: AISettings = await repo.get_user_settings(message.from_id)
    await message.answer_chat_action(types.ChatActions.TYPING)
    
    ai_text_answer = await openai.get_answer(
        max_tokens=settings.max_tokens,
        model=settings.model,
        temperature=settings.temperature,
        prompt=message.text,
        )
    if ai_text_answer is not None:
        await message.answer(ai_text_answer)
    else:
        await message.answer('Что-то пошло не так, сообщение от AI не получено')


def register_answer_ai(dp: Dispatcher):
    dp.register_message_handler(
        answer_ai,
        state="*", # срабатывает всегда и везде
        content_types=types.ContentTypes.ANY, 
        is_admin=True
        )
