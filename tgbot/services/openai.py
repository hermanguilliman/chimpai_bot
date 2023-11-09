import io
from datetime import datetime

from loguru import logger
from openai import APIConnectionError, AsyncOpenAI, BadRequestError, RateLimitError

from tgbot.models.personality import Personality


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
        personality: Personality | None = None,
    ) -> str:
        """
        Функция использует OpenAI для ответа на вопросы
        """
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

        messages = [
            {"role": "user", "content": f"{prompt}"},
        ]
        if isinstance(personality, Personality):
            today = datetime.now().strftime("%d.%m.%Y")
            time = datetime.now().strftime("%H:%M")

            messages.insert(
                0,
                {
                    "role": "system",
                    "content": f"{personality.text}. Дата: {today}. Время: {time}",
                },
            )
        try:
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
            engines = await self.openai.models.list()
            return engines.data
        else:
            return "error"

    async def audio_to_text(self, audio_path: str, api_key: str = None) -> str:
        if api_key:
            self.openai.api_key = api_key
            with open(audio_path, "rb") as file:
                transcript = await self.openai.audio.transcriptions.create(
                    file=file, model="whisper-1"
                )
                return transcript.text
        else:
            pass

    async def create_image(self, prompt: str = None, api_key: str = None) -> str:
        if prompt:
            if api_key:
                try:
                    self.openai.api_key = api_key
                    image_url = await self.openai.images.generate(
                        prompt=prompt,
                        model="dall-e-3",
                        n=1,
                        size="1024x1024",
                        quality="hd",
                        response_format="url",
                    )
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

    async def create_speech(
        self,
        model: str = None,
        voice: str = None,
        speed: str = None,
        prompt: str = None,
        api_key: str = None,
    ):
        if prompt:
            if api_key:
                try:
                    self.openai.api_key = api_key
                    response = await self.openai.audio.speech.create(
                        model=model,
                        voice=voice,
                        speed=speed,
                        input=prompt,
                        response_format="opus",
                    )
                    return io.BytesIO(response.read()).getvalue()
                except Exception as e:
                    print(e)
