from typing import List, Optional

from loguru import logger
from openai import (
    APIError,
    AsyncOpenAI,
    PermissionDeniedError,
)

from tgbot.models.models import ConversationHistory


class NeuralChatService:
    """Сервис предоставляющий доступ к клиенту OpenAI"""

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
            "base_url",
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
        base_url: str,
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
                base_url=base_url,
                api_key=api_key,
                model=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
        except self.ValidationError as e:
            return str(e)
        self.openai.base_url = base_url
        self.openai.api_key = api_key
        messages = await self._prepare_messages(prompt, person_text, history)

        error_messages = {
            400: "ChimpAI сообщает - Ошибка 400: Неверный запрос",
            401: "ChimpAI сообщает - Ошибка 401: Неверный API-ключ",
            402: "ChimpAI сообщает - Ошибка 402: Требуется оплата",
            403: "ChimpAI сообщает - Ошибка 403: Доступ запрещен",
            404: "ChimpAI сообщает - Ошибка 404: Ресурс не найден",
            409: "ChimpAI сообщает - Ошибка 409: Конфликт запроса",
            422: "ChimpAI сообщает - Ошибка 422: Неверные параметры запроса",
            429: "ChimpAI сообщает - Ошибка 429: Превышен лимит запросов",
        }

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
                return error_messages[403]
            except APIError as e:
                for status_code, message in error_messages.items():
                    if e.status_code == status_code:
                        logger.error(message)
                        return message
                logger.error(f"Ошибка API на попытке {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    logger.error("Все попытки закончились неудачей")
                    return None
            except Exception as e:
                logger.error(f"Ошибка на попытке {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    logger.error("Все попытки закончились неудачей")
                    return None
            logger.info("Повторная попытка...")
        return None

    async def get_engines(
        self, base_url: str, api_key: Optional[str]
    ) -> list | str:
        if not base_url:
            return "Отсутствует адрес API"
        if not api_key:
            return "Отсутствует API ключ"
        self.openai.base_url = base_url
        self.openai.api_key = api_key

        error_messages = {
            400: "ChimpAI сообщает - Ошибка 400: Неверный запрос",
            401: "ChimpAI сообщает - Ошибка 401: Неверный API-ключ",
            402: "ChimpAI сообщает - Ошибка 402: Требуется оплата",
            403: "ChimpAI сообщает - Ошибка 403: Доступ запрещен",
            404: "ChimpAI сообщает - Ошибка 404: Ресурс не найден",
            409: "ChimpAI сообщает - Ошибка 409: Конфликт запроса",
            422: "ChimpAI сообщает - Ошибка 422: Неверные параметры запроса",
            429: "ChimpAI сообщает - Ошибка 429: Превышен лимит запросов",
        }

        try:
            engines = await self.openai.models.list()
            return engines.data
        except PermissionDeniedError:
            logger.error("Доступ запрещен")
            return error_messages[403]
        except APIError as e:
            for status_code, message in error_messages.items():
                if e.status_code == status_code:
                    logger.error(message)
                    return message
            logger.error(f"Ошибка получения моделей: {e}")
            return "Ошибка получения моделей"
        except Exception as e:
            logger.error(f"Ошибка получения моделей: {e}")
            return "Ошибка получения моделей"
