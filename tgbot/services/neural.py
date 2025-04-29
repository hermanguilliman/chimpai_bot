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

from tgbot.models.history import ConversationHistory


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
                logger.debug(f"Missing required parameter: {param}")
                raise self.ValidationError(
                    f"Missing required parameter: {param}"
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
                    f"Empty response received. Attempt {attempt + 1}/{max_retries}"
                )
            except PermissionDeniedError:
                logger.error("Permission denied")
                return "Access denied (403)"
            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    logger.error("All retry attempts failed")
                    return None
                logger.info("Retrying...")
        return None

    async def get_engines(self, api_key: Optional[str]) -> list | str:
        if not api_key:
            return "Missing API key"

        self.openai.api_key = api_key
        try:
            engines = await self.openai.models.list()
            return engines.data
        except Exception as e:
            logger.error(f"Error fetching engines: {e}")
            return "Error fetching models"

    async def audio_to_text(
        self, audio_path: str, api_key: Optional[str]
    ) -> Optional[str]:
        if not api_key:
            return "Missing API key"

        self.openai.api_key = api_key
        try:
            with open(audio_path, "rb") as file:
                transcript = await self.openai.audio.transcriptions.create(
                    file=file, model="whisper-1"
                )
                return transcript.text
        except Exception as e:
            logger.error(f"Audio transcription error: {e}")
            return None

    async def create_image(
        self, prompt: Optional[str], api_key: Optional[str]
    ) -> str:
        if not prompt:
            return "Missing prompt"
        if not api_key:
            return "Missing API key"

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
            logger.debug("Invalid request")
            return "Service rules violation"
        except RateLimitError:
            logger.debug("Rate limit exceeded")
            return "Image generation rate limit exceeded"
        except APIConnectionError:
            logger.debug("Connection error")
            return "Network connection error"
        except Exception as e:
            logger.error(f"Image generation error: {e}")
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
            logger.error(f"Speech generation error: {e}")
            return None
