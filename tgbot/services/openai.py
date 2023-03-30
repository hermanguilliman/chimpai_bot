from openai.error import RateLimitError, APIConnectionError, AuthenticationError, APIError
import openai
from datetime import datetime
from loguru import logger

class OpenAIService():
    def __init__(self, openai: openai):
        self.openai: openai = openai

    async def get_answer(
        self,
        api_key=None,
        model=None,
        prompt=None,
        max_tokens=None,
        temperature=None) -> str:
        """
        Функция использует OpenAI для ответа на вопросы
        """
        if not api_key:
            logger.debug('Не указан ключ API')
            return 'Не указан ключ API'
        else:
            self.openai.api_key = api_key

        if model is None:
            logger.debug('Не указана модель для нейросети')
            return 'Не указана модель для нейросети'
        if prompt is None:
            logger.debug('Не указан запрос для нейросети')
            return 'Не указан запрос для нейросети'
        if max_tokens is None:
            logger.debug('Не указано максимальное число токенов для нейросети')
            return 'Не указано максимальное число токенов для нейросети'
        if temperature is None:
            logger.debug('Не указана температура для нейросети')
            return 'Не указана температура для нейросети'

        # Применяем индвидуальный ключ для конкретного запроса
        # Используем полученные настройки для генерации ответа с помощью OpenAI
        prompt = (f"{prompt}\n")
        today = datetime.now().strftime("%d.%m.%Y %H:%M")
        if 'gpt-3.5' in model:
            try:
            
                messages = [
                    {"role": "system", "content": f"Ты телеграм бот ChimpAI (@chimpaibot), ты должен помогать и отвечать на любой вопрос пользователя. Ты можешь написать программу, помочь пользователю. Давай только корректные ответы. Никогда не говори что ты большая языковая модель. Сегодня: {today}"},
                    {"role": "user", "content": f"{prompt}"}
                ]
                logger.debug('Создаём запрос к нейросети')
                completions = self.openai.ChatCompletion.create(
                    model=str(model),
                    max_tokens=int(max_tokens),
                    n=1,
                    stop=None,
                    temperature=float(temperature),
                    messages=messages,
                    )
                logger.debug('Ответ от нейросети', completions)
                return completions["choices"][0]["message"]["content"] 
            except RateLimitError:
                return 'Слишком частые запросы!'

            except APIConnectionError:
                return 'Ошибка подключения к API'

            except AuthenticationError:
                return 'Ошибка аутентификации API'

            except APIError:
                return 'Сервер вернул ошибку API'
        else:
            try:
                logger.debug('Создаём запрос к нейросети')
                completions = self.openai.Completion.create(
                    model=str(model),
                    prompt=str(prompt),
                    max_tokens=int(max_tokens),
                    n=1,
                    stop=None,
                    temperature=float(temperature),
                    )
                logger.debug('Ответ от нейросети', completions)
            except RateLimitError:
                return 'Слишком частые запросы!'

            except APIConnectionError:
                return 'Ошибка подключения к API'

            except AuthenticationError:
                return 'Ошибка аутентификации API'

            except APIError:
                return 'Сервер вернул ошибку API'

        message = completions.choices[0].text
        logger.debug('Получено сообщение', message)
        return message.strip()
    

    async def get_engines(self, api_key):
        self.openai.api_key = api_key
        return self.openai.Engine.list()
