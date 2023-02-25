
from aiogram.types import Message, ChatActions, ParseMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import DialogManager
from tgbot.services.repository import Repo
from tgbot.models.aisettings import AISettings
from loguru import logger


async def neural_handler(
    message: Message,
    message_input: MessageInput,
    manager: DialogManager,):
    repo: Repo = manager.data['repo']
    openai = manager.data['openai']
    settings: AISettings = await repo.get_user_settings(message.from_id)
    
    prompt = message.text
    if message.reply_to_message:
        prompt = message.text + f'\n"{message.reply_to_message.text}"'
    
    await message.answer('<b>⌛️ Запрос отправлен. Ожидание ответа...</b>', parse_mode=ParseMode.HTML)
    await message.answer_chat_action(ChatActions.TYPING)

    try:
        if settings is not None:
            logger.debug('Создание запроса к нейросети')
            ai_text_answer = await openai.get_answer(
                api_key=settings.api_key,
                max_tokens=settings.max_tokens,
                model=settings.model,
                temperature=settings.temperature,
                prompt=prompt,
                )
        else:
            await message.answer('Настройки не найдены. Попробуйте выполнить /start')

        if ai_text_answer:
            """выдача успешного запроса"""
            await message.reply(ai_text_answer)
        else:
            await message.answer('Что-то пошло не так, ответ от OpenAI не получен')
    
    except:
        await message.answer('Ошибка получения ответа!')
        logger.error('Ошибка получения ответа!')
    