"""
Text formatting helper using TDLib's parseMarkdown and parseTextEntities
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grathon.core.tdclient import TdClient

from grathon.core.TLSchema_Manager.tltypes import (
    formattedText,
    textParseModeMarkdown,
    textParseModeHTML,
)


class TextFormatter:
    """
    Helper for text formatting using TDLib's built-in parsing functions.

    TDLib handles all entity extraction automatically via:
    - parseMarkdown(): Parses Markdown syntax
    - parseTextEntities(): Parses HTML or Markdown based on parse_mode

    No manual entity management needed!
    """

    def __init__(self, client: TdClient):
        """
        Initialize formatter

        Args:
            client: TdClient instance
        """
        self.client = client

    async def markdown(self, text: str) -> formattedText:
        """
        Parse text with Markdown formatting.

        TDLib automatically extracts entities from Markdown syntax.

        Supported Markdown syntax:
            **bold**
            __italic__
            __**bold italic**__
            `inline code`
            ```pre code block```
            ```python
            code with language
            ```
            ~~strikethrough~~
            ||spoiler||
            [link text](https://example.com)
            [mention](tg://user?id=123456789)

        Args:
            text: Text with Markdown formatting

        Returns:
            formattedText object with entities extracted by TDLib

        Example:
            formatted = await formatter.markdown("**bold** and `code`")
            >>> # TDLib returns: formattedText(
            >>> #     text="bold and code",
            >>> #     entities=[
            >>> #         textEntity(offset=0, length=4, type=textEntityTypeBold()),
            >>> #         textEntity(offset=13, length=4, type=textEntityTypeCode())
            >>> #     ]
            >>> # )
        """
        try:
            # Parse markdown using TDLib
            result = await self.client.api.parse_markdown(
                text=formattedText(text=text)
            )
            return result
        except Exception as e:
            # Fallback: return plain text if parsing fails
            print(f"Error parsing markdown: {e}")
            return formattedText(text=text)

    async def html(self, text: str) -> formattedText:
        """
        Parse text with HTML formatting.

        TDLib automatically extracts entities from HTML tags.

        Supported HTML tags:
            <b>bold</b>
            <i>italic</i>
            <u>underline</u>
            <s>strikethrough</s>
            <code>inline code</code>
            <pre>code block</pre>
            <pre><code>code with language</code></pre>
            <blockquote>block quote</blockquote>
            <a href="https://example.com">link</a>
            <tg-emoji emoji-id="123">custom emoji</tg-emoji>

        Args:
            text: Text with HTML formatting

        Returns:
            formattedText object with entities extracted by TDLib

        Example:
            formatted = await formatter.html("<b>bold</b> and <code>code</code>")
            # TDLib returns same as markdown example
        """
        return await self.client.api.parse_text_entities(
            text=text,
            parse_mode=textParseModeHTML()
        )

    async def plain(self, text: str) -> formattedText:
        """
        Create formattedText without any formatting (plain text).

        Args:
            text: Plain text without formatting

        Returns:
            formattedText object with no entities
        """
        return formattedText(text=text, entities=[])


# Quick API for common cases
__text_formatter_instance = None


async def format_markdown(client: TdClient, text: str) -> formattedText:
    """
    Quick function to format Markdown text without creating formatter instance.

    Args:
        client: TdClient instance
        text: Text with Markdown syntax

    Returns:
        formattedText object
    """
    formatter = TextFormatter(client)
    return await formatter.markdown(text)


async def format_html(client: TdClient, text: str) -> formattedText:
    """
    Quick function to format HTML text without creating formatter instance.

    Args:
        client: TdClient instance
        text: Text with HTML syntax

    Returns:
        formattedText object
    """
    formatter = TextFormatter(client)
    return await formatter.html(text)
