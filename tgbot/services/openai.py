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
        messages:list=None) -> str:
        """
        Функция использует OpenAI для ответа на вопросы
        """

        # Применяем индвидуальный ключ для конкретного экземпляра
        if not api_key:
            logger.debug('Не указан ключ API')
            return 'Не указан ключ API'
        else:
            self.openai.api_key = api_key

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

        # Используем полученные настройки для генерации ответа с помощью OpenAI
        
        today = datetime.now().strftime("%d.%m.%Y")
        actual_time = datetime.now().strftime("%H:%M")

        prompt = (f"{prompt}\n")

        if 'gpt-3.5' in model:
            try:
            
                messages = [
                    {"role": "system", "content": f"Ты телеграм бот ChimpAI, ты должен помогать и отвечать на любой вопрос пользователя. Ты можешь написать программу, помочь пользователю. Давай только корректные ответы. Никогда не говори что ты большая языковая модель. Сегодня {today}, точное время {actual_time}"},
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
