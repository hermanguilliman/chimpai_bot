from openai.error import RateLimitError, APIConnectionError, AuthenticationError, APIError
import openai
from datetime import datetime
from loguru import logger

class OpenAIService():
    def __init__(self, openai: openai):
        self.openai: openai = openai

    async def get_answer(
        self,
        api_key:str=None,
        model:str=None,
        prompt:str=None,
        max_tokens:int=None,
        temperature:float=None,
        personality:str=None) -> str:
        """
        Функция использует OpenAI для ответа на вопросы
        """
        # Применяем индвидуальный ключ для конкретного экземпляра
        if not api_key:
            logger.debug('Не указан ключ API')
            return 'Не указан ключ API'
        if not model:
            logger.debug('Не указана модель для нейросети')
            return 'Не указана модель для нейросети'
        if not prompt:
            logger.debug('Не указан запрос для нейросети')
            return 'Не указан запрос для нейросети'
        if not max_tokens:
            logger.debug('Не указано максимальное число токенов для нейросети')
            return 'Не указано максимальное число токенов для нейросети'
        if not temperature:
            logger.debug('Не указана температура для нейросети')
            return 'Не указана температура для нейросети'
        
        self.openai.api_key = api_key
        
        # Используем полученные настройки для генерации ответа с помощью OpenAI
        
        today = datetime.now().strftime("%d.%m.%Y")
        time = datetime.now().strftime("%H:%M")

        if 'gpt-3.5' in model:
            try:
                messages = [
                    {"role": "system", "content": f"{personality} Сегодня на календаре: {today}. Точное время: {time}"},
                    {"role": "user", "content": f"{prompt}"}
                ]

                completions = await self.openai.ChatCompletion.acreate(
                    model=model,
                    max_tokens=max_tokens,
                    n=1,
                    stop=None,
                    temperature=temperature,
                    messages=messages,
                    )
                return completions.choices[0].message.content
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
                completions = await self.openai.Completion.acreate(
                    model=model,
                    prompt=prompt,
                    max_tokens=max_tokens,
                    n=1,
                    stop=None,
                    temperature=temperature,
                    )
                logger.debug('Ответ от нейросети получен')
            except RateLimitError:
                return 'Слишком частые запросы!'

            except APIConnectionError:
                return 'Ошибка подключения к API'

            except AuthenticationError:
                return 'Ошибка аутентификации API'

            except APIError:
                return 'Сервер вернул ошибку API'

        message = completions.choices[0].text
        return message.strip()
    

    async def get_engines(self, api_key) -> list:
        if api_key:
            self.openai.api_key = api_key
            return self.openai.Engine.list()
        else:
            return 'error'
