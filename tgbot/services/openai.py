import io
from typing import List

from loguru import logger
from openai import (
    APIConnectionError,
    AsyncOpenAI,
    BadRequestError,
    PermissionDeniedError,
    RateLimitError,
)

from tgbot.models.history import ConversationHistory


class OpenAIService:
    def __init__(self, openai: AsyncOpenAI):
        self.openai: AsyncOpenAI = openai

    async def __prepare_messages(
        self,
        prompt: str,
        person_text: str | None = None,
        history: List[ConversationHistory] | None = None,
    ) -> list:
        messages = []

        # Добавляем системное сообщение
        if isinstance(person_text, str):
            messages.append({"role": "system", "content": person_text})
        else:
            messages.append(
                {
                    "role": "system",
                    "content": "Давай короткие и информативные ответы, не более одного абзаца.",
                }
            )

        # Добавляем историю сообщений, если она есть
        if history:
            # Переворачиваем историю, чтобы сообщения шли в хронологическом порядке
            for msg in reversed(history):
                messages.append({"role": msg.role, "content": msg.content})

        # Добавляем текущий запрос пользователя
        messages.append({"role": "user", "content": prompt})

        return messages

    async def get_answer(
        self,
        api_key: str = None,
        model: str = None,
        prompt: str = None,
        max_tokens: int = None,
        temperature: float = None,
        person_text: str = None,
        history: List[ConversationHistory] | None = None,
        max_retries: int = 3,
    ) -> str | None:
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

        messages = await self.__prepare_messages(prompt, person_text, history)

        for attempt in range(max_retries):
            try:
                completions = await self.openai.chat.completions.create(
                    messages=messages,
                    model=model,
                    max_tokens=max_tokens,
                    n=1,
                    stop=None,
                    temperature=temperature,
                )
                if (
                    completions.choices
                    and completions.choices[0].message.content is not None
                ):
                    message = completions.choices[0].message.content
                    return str(message)
                else:
                    logger.error(
                        f"Получен пустой ответ от нейросети. "
                        f"Попытка {attempt + 1} из {max_retries}."
                    )
            except PermissionDeniedError as e:
                logger.error(e)
                return "Ошибка 403. Отказано в доступе!"
            except Exception as e:
                logger.error(f"Ошибка нейросети на попытке {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    logger.info("Повторная попытка...")
                else:
                    logger.error("Все попытки завершились ошибкой.")
                    return None
        logger.error("Не удалось получить ответ после нескольких попыток.")
        return None

    async def get_engines(self, api_key: str = None) -> list:
        if api_key:
            self.openai.api_key = api_key
            engines = await self.openai.models.list()
            return engines.data
        else:
            return "error"

    async def audio_to_text(
        self, audio_path: str, api_key: str = None
    ) -> str | None:
        if api_key:
            self.openai.api_key = api_key

            try:
                with open(audio_path, "rb") as file:
                    transcript = await self.openai.audio.transcriptions.create(
                        file=file, model="whisper-1"
                    )
                    return transcript.text
            except Exception as e:
                logger.error(e)
                return None

    async def create_image(
        self, prompt: str = None, api_key: str = None
    ) -> str:
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
                except BadRequestError as e:
                    logger.debug(e)
                    return "Нарушение правил сервиса."
                except RateLimitError as e:
                    logger.debug(e)
                    return "Превышен лимит изображений в минуту."
                except APIConnectionError as e:
                    logger.debug(e)
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
