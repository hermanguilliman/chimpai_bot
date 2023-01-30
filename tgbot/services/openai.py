from openai.error import RateLimitError, APIConnectionError, AuthenticationError, APIError
import openai
class OpenAIService():
    def __init__(self, openai: openai):
        self.openai: openai = openai

    async def get_answer(
        self,
        model=None,
        prompt=None,
        max_tokens=None,
        temperature=None) -> str:

        """
        Функция использует OpenAI для ответа на вопросы
        """
        if model is None:
            return 'Не указана модель для нейросети'
        if prompt is None:
            return 'Не указан запрос для нейросети'
        if max_tokens is None:
            return 'Не указано максимальное число токенов для нейросети'
        if temperature is None:
            return 'Не указана температура для нейросети'

        # Используем полученные настройки для генерации ответа с помощью OpenAI
        prompt = (f"{prompt}\n")
        try:
            completions = self.openai.Completion.create(
                engine=str(model),
                prompt=str(prompt),
                max_tokens=int(max_tokens),
                n=1,
                stop=None,
                temperature=float(temperature),
                )
        except RateLimitError:
            return 'Достигнут лимит по тарифному плану. Проверьте ваш личный кабинет https://beta.openai.com/account/usage'

        except APIConnectionError:
            return 'Ошибка подключения к OpenAI API'

        except AuthenticationError:
            return 'Ошибка аутентификации OpenAI API'

        except APIError:
            return 'Сервер вернул ошибку API'

        message = completions.choices[0].text
        return message.strip()

    async def get_engines(self):
        return self.openai.Engine.list()
