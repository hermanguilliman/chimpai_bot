from datetime import datetime

import openai
from loguru import logger


class OpenAIService:
    def __init__(self, openai: openai):
        self.openai: openai = openai

    async def get_answer(
        self,
        api_key: str = None,
        model: str = None,
        prompt: str = None,
        max_tokens: int = None,
        temperature: float = None,
        personality: str = None,
    ) -> str:
        """
        Функция использует OpenAI для ответа на вопросы
        """
        # Применяем индвидуальный ключ для конкретного экземпляра
        if not api_key:
            logger.debug("Не указан ключ API")
            return "Не указан ключ API"
        if not model:
            logger.debug("Не указана модель для нейросети")
            return "Не указана модель для нейросети"
        if not prompt:
            logger.debug("Не указан запрос для нейросети")
            return "Не указан запрос для нейросети"
        if not max_tokens:
            logger.debug("Не указано максимальное число токенов для нейросети")
            return "Не указано максимальное число токенов для нейросети"
        if not temperature:
            logger.debug("Не указана температура для нейросети")
            return "Не указана температура для нейросети"

        self.openai.api_key = api_key

        # Используем полученные настройки для генерации ответа с помощью OpenAI

        today = datetime.now().strftime("%d.%m.%Y")
        time = datetime.now().strftime("%H:%M")

        try:
            messages = [
                {
                    "role": "system",
                    "content": f"{personality} Сегодня на календаре: {today}. Точное время: {time}",
                },
                {"role": "user", "content": f"{prompt}"},
            ]

            completions = await self.openai.ChatCompletion.acreate(
                model=model,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=temperature,
                messages=messages,
            )
        except Exception as e:
            return f"{e}"

        message = completions.choices[0].message.content
        return str(message)

    async def get_engines(self, api_key: str) -> list:
        if api_key:
            self.openai.api_key = api_key
            return self.openai.Engine.list()
        else:
            return "error"
        

    async def audio_to_text(self, audio_path: str, api_key: str) -> str:
        if api_key:
            self.openai.api_key = api_key
            with open(audio_path, "rb") as file:
                transcript = await self.openai.Audio.atranscribe("whisper-1", file)
                return transcript.text
