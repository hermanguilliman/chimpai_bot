import io
from typing import List, Optional

from loguru import logger
from openai import (
    APIConnectionError,
    AsyncOpenAI,
    BadRequestError,
    PermissionDeniedError,
    RateLimitError,
)

from tgbot.models.models import ConversationHistory


class OpenAIService:
    def __init__(self, openai: AsyncOpenAI):
        self.openai = openai
        self.default_system_message = (
            "Давай короткие и информативные ответы, не более одного абзаца."
        )

    class ValidationError(Exception):
        pass

    async def _prepare_messages(
        self,
        prompt: str,
        person_text: Optional[str] = None,
        history: Optional[List[ConversationHistory]] = None,
    ) -> List[dict]:
        messages = [
            {
                "role": "system",
                "content": person_text or self.default_system_message,
            }
        ]

        if history:
            messages.extend(
                {"role": msg.role, "content": msg.content}
                for msg in reversed(history)
            )

        messages.append({"role": "user", "content": prompt})
        return messages

    def _validate_params(self, **kwargs) -> None:
        required_params = [
            "api_key",
            "model",
            "prompt",
            "max_tokens",
            "temperature",
        ]
        for param in required_params:
            if kwargs.get(param) is None:
                logger.debug(f"Отсутствует требуемый параметр: {param}")
                raise self.ValidationError(
                    f"Отсутствует требуемый параметр: {param}"
                )

    async def get_answer(
        self,
        api_key: str,
        model: str,
        prompt: str,
        max_tokens: int,
        temperature: float,
        person_text: Optional[str] = None,
        history: Optional[List[ConversationHistory]] = None,
        max_retries: int = 3,
    ) -> Optional[str]:
        try:
            self._validate_params(
                api_key=api_key,
                model=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
        except self.ValidationError as e:
            return str(e)

        self.openai.api_key = api_key
        messages = await self._prepare_messages(prompt, person_text, history)

        for attempt in range(max_retries):
            try:
                response = await self.openai.chat.completions.create(
                    messages=messages,
                    model=model,
                    max_tokens=max_tokens,
                    n=1,
                    stop=None,
                    temperature=temperature,
                )
                if response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content
                logger.error(
                    f"Получен пустой ответ. Попытка {attempt + 1}/{max_retries}"
                )
            except PermissionDeniedError:
                logger.error("Доступ запрещен")
                return "Доступ запрещен (403)"
            except Exception as e:
                logger.error(f"Ошибка на попытке {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    logger.error("Все попытки закончились неудачей")
                    return None
            logger.info("Повторная попытка...")
        return None

    async def get_engines(self, api_key: Optional[str]) -> list | str:
        if not api_key:
            return "Отсутствует API ключ"

        self.openai.api_key = api_key
        try:
            engines = await self.openai.models.list()
            return engines.data
        except Exception as e:
            logger.error(f"Ошибка получения моделей: {e}")
            return "Ошибка получения моделей"

    async def audio_to_text(
        self, audio_path: str, api_key: Optional[str]
    ) -> Optional[str]:
        if not api_key:
            return "Отсутствует API ключ"

        self.openai.api_key = api_key
        try:
            with open(audio_path, "rb") as file:
                transcript = await self.openai.audio.transcriptions.create(
                    file=file, model="whisper-1"
                )
                return transcript.text
        except Exception as e:
            logger.error(f"Ошибка расшифровки аудио: {e}")
            return None

    async def create_image(
        self, prompt: Optional[str], api_key: Optional[str]
    ) -> str:
        if not prompt:
            return "Отсутствует запрос"
        if not api_key:
            return "Отсутствует API ключ"

        self.openai.api_key = api_key
        try:
            response = await self.openai.images.generate(
                prompt=prompt,
                model="dall-e-3",
                n=1,
                size="1024x1024",
                quality="hd",
                response_format="url",
            )
            return response.data[0].url
        except BadRequestError:
            logger.debug("Ошибка запроса")
            return "Ошибка запроса"
        except RateLimitError:
            logger.debug("Превышен лимит генерации изображений")
            return "Превышен лимит генерации изображений"
        except APIConnectionError:
            logger.debug("Ошибка соединения")
            return "Ошибка соединения"
        except Exception as e:
            logger.error(f"Ошибка генерации изображения: {e}")
            return str(e)

    async def create_speech(
        self,
        prompt: Optional[str],
        api_key: Optional[str],
        model: str = "tts-1",
        voice: str = "alloy",
        speed: str = "1.0",
    ) -> Optional[bytes]:
        if not prompt:
            return None
        if not api_key:
            return None

        self.openai.api_key = api_key
        try:
            response = await self.openai.audio.speech.create(
                model=model,
                voice=voice,
                speed=speed,
                input=prompt,
                response_format="opus",
            )
            return io.BytesIO(response.read()).getvalue()
        except Exception as e:
            logger.error(f"Ошибка генерации голоса: {e}")
            return None
