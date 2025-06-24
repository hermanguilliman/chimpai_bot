import asyncio
import logging
from dataclasses import dataclass
from typing import List, Optional, Union

import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Constants
DEFAULT_BASE_URL = "https://300.ya.ru/api"
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0
DEFAULT_TIMEOUT = 10.0
MAX_CONTENT_SIZE = 10 * 1024 * 1024  # 10 MB


@dataclass
class SharingResponse:
    """Response object for sharing URL requests."""

    status: str
    sharing_url: Optional[str] = None
    error: Optional[str] = None


@dataclass
class Chapter:
    """Represents a chapter in the summary with a subheading and theses."""

    subheading: str
    theses: List[str]


@dataclass
class SummaryResult:
    """Represents the summary result with title, chapters, and summary points."""

    title: str
    chapters: List[Chapter]
    summary_points: List[str]
    error: Optional[str] = None

    def to_markdown(self) -> str:
        """Format the summary result as Markdown.

        Returns:
            A string containing the formatted Markdown content.
        """
        markdown = []
        if self.error:
            markdown.append(f"## Error\n\n{self.error}")
            return "\n".join(markdown)

        markdown.append(f"# {self.title}")
        if self.chapters:
            markdown.append("\n## Подробный пересказ\n")
            for i, chapter in enumerate(self.chapters, 1):
                markdown.append(f"### {i}. {chapter.subheading}\n")
                for j, thesis in enumerate(chapter.theses, 1):
                    markdown.append(f"- {j}. {thesis}")
                markdown.append("")  # Add blank line for readability
        if self.summary_points:
            markdown.append("\n## Краткий пересказ\n")
            for i, point in enumerate(self.summary_points, 1):
                markdown.append(f"- {i}. {point}")
        return "\n".join(markdown)

    def to_plain_text(self) -> str:
        """Format the summary result as plain text.

        Returns:
            A string containing the formatted plain text content.
        """
        lines = []
        if self.error:
            lines.append(f"Error: {self.error}")
            return "\n".join(lines)

        lines.append(f"Заголовок: {self.title}")
        if self.chapters:
            lines.append("\nПодробный пересказ:")
            for i, chapter in enumerate(self.chapters, 1):
                lines.append(f"{i}. {chapter.subheading}")
                for j, thesis in enumerate(chapter.theses, 1):
                    lines.append(f"   {j}. {thesis}")
        if self.summary_points:
            lines.append("\nКраткий пересказ:")
            for i, point in enumerate(self.summary_points, 1):
                lines.append(f"   {i}. {point}")
        return "\n".join(lines)

    def to_html(self) -> str:
        """Format the summary result as HTML.

        Returns:
            A string containing the formatted HTML content.
        """
        html = [
            "<!DOCTYPE html>",
            '<html lang="ru">',
            "<head>",
            '<meta charset="UTF-8">',
            "<title>Summary Result</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; margin: 40px; }",
            "h1 { color: #333; }",
            "h2 { color: #555; }",
            "h3 { color: #777; }",
            "ul { margin: 10px 0; }",
            "li { margin: 5px 0; }",
            ".error { color: red; }",
            "</style>",
            "</head>",
            "<body>",
        ]

        if self.error:
            html.append(
                f'<div class="error"><h2>Error</h2><p>{self.error}</p></div>'
            )
        else:
            html.append(f"<h1>{self.title}</h1>")
            if self.chapters:
                html.append("<h2>Подробный пересказ</h2>")
                for i, chapter in enumerate(self.chapters, 1):
                    html.append(f"<h3>{i}. {chapter.subheading}</h3>")
                    html.append("<ul>")
                    for j, thesis in enumerate(chapter.theses, 1):
                        html.append(f"<li>{j}. {thesis}</li>")
                    html.append("</ul>")
            if self.summary_points:
                html.append("<h2>Краткий пересказ</h2>")
                html.append("<ul>")
                for i, point in enumerate(self.summary_points, 1):
                    html.append(f"<li>{i}. {point}</li>")
                html.append("</ul>")

        html.extend(["</body>", "</html>"])
        return "\n".join(html)


class YandexSummaryAPI:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self._api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        self._update_headers()
        self.session: Optional[aiohttp.ClientSession] = None

    def _update_headers(self):
        """Update headers based on current api_key."""
        self.headers = {"Authorization": f"OAuth {self._api_key}"}

    @property
    def api_key(self) -> Optional[str]:
        return self._api_key

    @api_key.setter
    def api_key(self, value: Optional[str]):
        self._api_key = value
        self._update_headers()
        # Если сессия уже создана, нужно обновить её заголовки
        if self.session:
            self.session._default_headers = self.headers

    async def __aenter__(self):
        """Create an aiohttp session with configured timeout."""
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            timeout=aiohttp.ClientTimeout(total=self.timeout),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the aiohttp session."""
        if self.session:
            await self.session.close()

    async def _get_sharing_url(self, article_url: str) -> SharingResponse:
        """Obtain a sharing URL for the given article.

        Args:
            article_url: URL of the article to summarize.

        Returns:
            SharingResponse with status, sharing URL, or error message.
        """
        endpoint = f"{self.base_url}/sharing-url"
        payload = {"article_url": article_url}

        for attempt in range(self.max_retries):
            try:
                async with self.session.post(
                    endpoint, json=payload
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return SharingResponse(
                        status=data.get("status", "unknown"),
                        sharing_url=data.get("sharing_url"),
                        error=data.get("error"),
                    )
            except aiohttp.ClientResponseError as e:
                logger.error(
                    f"Request failed for {article_url}: {e.status}, {e.message}",
                    extra={"article_url": article_url},
                )
                if attempt == self.max_retries - 1:
                    return SharingResponse(
                        status="error", error=f"HTTP error: {str(e)}"
                    )
            except aiohttp.ClientError as e:
                logger.error(
                    f"Client error for {article_url}: {str(e)}",
                    extra={"article_url": article_url},
                )
                if attempt == self.max_retries - 1:
                    return SharingResponse(
                        status="error", error=f"Client error: {str(e)}"
                    )
            except Exception as e:
                logger.error(
                    f"Unexpected error for {article_url}: {str(e)}",
                    extra={"article_url": article_url},
                )
                return SharingResponse(
                    status="error", error=f"Unexpected error: {str(e)}"
                )
            await asyncio.sleep(self.retry_delay * (2**attempt))
        return SharingResponse(status="error", error="Max retries exceeded")

    async def _set_summary_mode(self, sharing_url: str, mode: str) -> bool:
        """Set the summary mode (short or detailed) for the sharing URL.

        Args:
            sharing_url: The sharing URL to configure.
            mode: Summary mode ('short' or 'detailed').

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            toggle_url = f"{sharing_url.rstrip('/')}?/toggle"
            payload = {"summary-mode": mode}
            async with self.session.post(toggle_url, data=payload) as response:
                response.raise_for_status()
                return True
        except aiohttp.ClientError as e:
            logger.error(
                f"Failed to set summary mode to {mode} for {sharing_url}: {str(e)}",
                extra={"sharing_url": sharing_url},
            )
            return False
        except Exception as e:
            logger.error(
                f"Unexpected error in setting mode for {sharing_url}: {str(e)}",
                extra={"sharing_url": sharing_url},
            )
            return False

    async def _fetch_and_parse_url(
        self, url: str
    ) -> Union[BeautifulSoup, None]:
        """Fetch and parse HTML content from a URL.

        Args:
            url: URL to fetch and parse.

        Returns:
            BeautifulSoup object if successful, None otherwise.
        """
        try:
            async with self.session.get(url, max_field_size=16384) as response:
                if (
                    response.content_length
                    and response.content_length > MAX_CONTENT_SIZE
                ):
                    logger.warning(
                        f"Content size exceeds limit for {url}: {response.content_length}",
                        extra={"url": url},
                    )
                    return None
                response.raise_for_status()
                content_type = response.headers.get("Content-Type", "")
                if "text/html" not in content_type.lower():
                    logger.warning(
                        f"Non-HTML content at {url}: {content_type}",
                        extra={"url": url},
                    )
                    return None
                content = await response.text()
                return BeautifulSoup(content, "html.parser")
        except aiohttp.ClientError as e:
            logger.error(
                f"Failed to fetch URL {url}: {str(e)}", extra={"url": url}
            )
            return None
        except Exception as e:
            logger.error(
                f"Unexpected error fetching URL {url}: {str(e)}",
                extra={"url": url},
            )
            return None

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean text by removing bullet points and extra whitespace.

        Args:
            text: Text to clean.

        Returns:
            Cleaned text string.
        """
        return text.replace("• ", "").strip()

    @staticmethod
    def _extract_title(soup: BeautifulSoup) -> str:
        """Extract the title from parsed HTML.

        Args:
            soup: BeautifulSoup object containing parsed HTML.

        Returns:
            Extracted title or fallback text if not found.
        """
        title = soup.find(
            "h1", class_=lambda x: x and "title" in x
        ) or soup.find("h1")
        return title.get_text().strip() if title else "No title found"

    @staticmethod
    def _extract_detailed_chapters(soup: BeautifulSoup) -> List[Chapter]:
        """Extract detailed chapters from parsed HTML.

        Args:
            soup: BeautifulSoup object containing parsed HTML.

        Returns:
            List of Chapter objects with subheadings and theses.
        """
        chapters_list = soup.find("ul", class_=lambda x: x and "chapters" in x)
        if not chapters_list:
            return []

        chapters = []
        for chapter_elem in chapters_list.find_all(
            "li", class_=lambda x: x and "chapter" in x
        ):
            subheading = chapter_elem.find(
                "h2", class_=lambda x: x and "chapter-subheading" in x
            )
            subheading_text = (
                subheading.get_text().strip()
                if subheading
                else "No subheading"
            )

            theses = []
            theses_list = chapter_elem.find(
                "ul", class_=lambda x: x and "theses" in x
            )
            if theses_list:
                for thesis in theses_list.find_all(
                    "li", class_=lambda x: x and "thesis" in x
                ):
                    text_wrapper = thesis.find(
                        "span", class_=lambda x: x and "text-wrapper" in x
                    )
                    thesis_text = (
                        text_wrapper.get_text().strip()
                        if text_wrapper
                        else "No thesis text"
                    )
                    theses.append(YandexSummaryAPI._clean_text(thesis_text))
            chapters.append(Chapter(subheading=subheading_text, theses=theses))
        return chapters

    @staticmethod
    def _extract_short_summary(soup: BeautifulSoup) -> List[str]:
        """Extract short summary points from parsed HTML.

        Args:
            soup: BeautifulSoup object containing parsed HTML.

        Returns:
            List of summary points.
        """
        theses_list = soup.find("ul", discounts=lambda x: x and "theses" in x)
        if not theses_list:
            return []

        theses = []
        for thesis in theses_list.find_all(
            "li", class_=lambda x: x and "thesis" in x
        ):
            text_wrapper = thesis.find(
                "span", class_=lambda x: x and "text-wrapper" in x
            )
            thesis_text = (
                text_wrapper.get_text().strip()
                if text_wrapper
                else "No thesis text"
            )
            theses.append(YandexSummaryAPI._clean_text(thesis_text))
        return theses

    async def get_summary(
        self, article_url: str, summary_type: str = "detailed"
    ) -> SummaryResult:
        """Retrieve a summary for the given article URL.

        Args:
            article_url: URL of the article to summarize.
            summary_type: Type of summary ('detailed' or 'short').

        Returns:
            SummaryResult containing title, chapters, summary_points, and optional error.
        """
        if summary_type not in ["short", "detailed"]:
            return SummaryResult(
                title="",
                chapters=[],
                summary_points=[],
                error=f"Invalid summary_type: {summary_type}. Use 'short' or 'detailed'.",
            )

        async with self:
            response = await self._get_sharing_url(article_url)
            if response.error or not response.sharing_url:
                return SummaryResult(
                    title="",
                    chapters=[],
                    summary_points=[],
                    error=response.error or "Failed to obtain sharing URL",
                )

            if summary_type == "short":
                success = await self._set_summary_mode(
                    response.sharing_url, "short"
                )
                if not success:
                    return SummaryResult(
                        title="",
                        chapters=[],
                        summary_points=[],
                        error="Failed to set short summary mode",
                    )

            soup = await self._fetch_and_parse_url(response.sharing_url)
            if not soup:
                return SummaryResult(
                    title="",
                    chapters=[],
                    summary_points=[],
                    error="Failed to parse summary content",
                )

            title = self._extract_title(soup)
            chapters = (
                self._extract_detailed_chapters(soup)
                if summary_type == "detailed"
                else []
            )
            summary_points = (
                self._extract_short_summary(soup)
                if summary_type == "short"
                else []
            )
            return SummaryResult(
                title=title, chapters=chapters, summary_points=summary_points
            )
