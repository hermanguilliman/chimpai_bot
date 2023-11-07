from datetime import datetime
from openai import AsyncOpenAI, BadRequestError, RateLimitError, APIConnectionError
from loguru import logger


class OpenAIService:
    def __init__(self, openai: AsyncOpenAI):
        self.openai: AsyncOpenAI = openai

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
                    "content": f"{personality} Дата: {today}. Время: {time}",
                },
                {"role": "user", "content": f"{prompt}"},
            ]

            completions = await self.openai.chat.completions.create(
                messages=messages,
                model=model,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=temperature,
            )
        except Exception as e:
            return f"{e}"

        message = completions.choices[0].message.content
        return str(message)

    async def get_engines(self, api_key: str = None) -> list:
        if api_key:
            self.openai.api_key = api_key
            return self.openai.models.list()
        else:
            return "error"

    async def audio_to_text(self, audio_path: str, api_key: str = None) -> str:
        if api_key:
            self.openai.api_key = api_key
            with open(audio_path, "rb") as file:
                transcript = await self.openai.audio.transcriptions.create(file=file, model="whisper-1")
                return transcript.text

    async def create_image(self, prompt: str = None, api_key: str = None) -> str:
        if prompt:
            if api_key:
                try:
                    self.openai.api_key = api_key
                    image_url = await self.openai.images.generate(
                        prompt=prompt,
                        model='dall-e-3',
                        n=1,
                        size="1024x1024",
                        quality="hd",
                        response_format="url")
                    return image_url.data[0].url
                except BadRequestError:
                    return "Измените текст запроса, чтобы не нарушать правила сервиса."
                except RateLimitError:
                    return "Превышен лимит изображений в минуту. Попробуйте позднее."
                except APIConnectionError:
                    return "Ошибка соединения с нейросетью"
                except Exception as e:
                    return f"{e}"

        else:
            return "Не указано текстовое описание"
