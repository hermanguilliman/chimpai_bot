from loguru import logger
from aiogram import types, Dispatcher
from tgbot.services.openai import OpenAIService
from tgbot.services.repository import Repo
from tgbot.models.aisettings import AISettings

async def answer_ai(message: types.Message, openai: OpenAIService, repo: Repo):
    settings: AISettings = await repo.get_user_settings(message.from_id)
    await message.answer_chat_action(types.ChatActions.TYPING)
    
    try:
        if settings is not None:
            ai_text_answer = await openai.get_answer(
                max_tokens=settings.max_tokens,
                model=settings.model,
                temperature=settings.temperature,
                prompt=message.text,
                )
        else:
            await message.answer('Настройки не найдены. Попробуйте выполнить /start')

        if ai_text_answer is not None:
            await message.answer(ai_text_answer)
        else:
            await message.answer('Что-то пошло не так, сообщение от AI не получено')
    
    except:
        logger.error('Ошибка получения запроса!')


def register_answer_ai(dp: Dispatcher):
    dp.register_message_handler(
        answer_ai,
        state="*", # срабатывает всегда и везде
        content_types=types.ContentTypes.ANY, 
        is_admin=True
        )
