from tgbot.api.yandex_summary import YandexSummaryAPI


class SummaryChatService:
    def __init__(self, yandex_api: YandexSummaryAPI):
        self.api = yandex_api

    async def get_summary(
        self,
        base_url: str,
        api_key: str,
        url: str,
        summary_type: str = "detailed",
    ):
        self.api.base_url = base_url
        self.api.api_key = api_key
        result = await self.api.get_summary(
            article_url=url,
            summary_type=summary_type,
        )
        if result.error:
            return f"Ошибка сервиса: {result.error}"
        else:
            return result.to_plain_text()
