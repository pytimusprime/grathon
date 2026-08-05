"""
Pagination helpers for long lists and content
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional

if TYPE_CHECKING:
    from grathon.high_level.contexts.message_context import MessageContext

from .formatted_text import TextFormatter


class PaginationHelper:
    """Helper for paginating content"""

    @staticmethod
    async def paginate_list(
        ctx: MessageContext,
        items: list[str],
        page_size: int = 10,
        title: str = "",
        header: str = "",
        footer: str = "",
        numbered: bool = True
    ) -> None:
        """
        Send paginated list to user

        Args:
            ctx: MessageContext
            items: List of items to paginate
            page_size: Items per page
            title: Title for the list
            header: Header text on each page
            footer: Footer text on each page
            numbered: Show item numbers

        Examples:
            >>> items = [f"Item {i}" for i in range(1, 50)]
            >>> await PaginationHelper.paginate_list(ctx, items, page_size=10)
        """
        if not items:
            await ctx.reply("📭 List is empty")
            return

        total_pages = (len(items) + page_size - 1) // page_size

        for page_num in range(total_pages):
            start = page_num * page_size
            end = start + page_size
            page_items = items[start:end]

            # Build message
            message_parts = []

            if title:
                message_parts.append(f"**{title}**\n")

            if header:
                message_parts.append(f"{header}\n")

            # Add items with numbers
            for i, item in enumerate(page_items, start=start + 1):
                if numbered:
                    message_parts.append(f"{i}. {item}")
                else:
                    message_parts.append(f"• {item}")

            if footer:
                message_parts.append(f"\n{footer}")

            # Add page indicator
            message_parts.append(
                f"\n\n📄 صفحه {page_num + 1}/{total_pages}"
            )

            message_text = "\n".join(message_parts)

            # Format as markdown
            formatter = TextFormatter(ctx.client)
            formatted = await formatter.markdown(message_text)

            await ctx.reply(formatted)

    @staticmethod
    async def paginate_dict(
        ctx: MessageContext,
        items: dict[str, Any],
        page_size: int = 10,
        title: str = "",
        value_formatter=None
    ) -> None:
        """
        Send paginated dictionary/mapping to user

        Args:
            ctx: MessageContext
            items: Dictionary to paginate
            page_size: Items per page
            title: Title for the list
            value_formatter: Optional function to format values

        Examples:
            >>> data = {"key1": "value1", "key2": "value2", ...}
            >>> await PaginationHelper.paginate_dict(ctx, data)
        """
        if not items:
            await ctx.reply("📭 List is empty")
            return

        # Convert to list of strings
        formatted_items = []
        for key, value in items.items():
            if value_formatter:
                formatted_value = value_formatter(value)
            else:
                formatted_value = str(value)

            formatted_items.append(f"**{key}**: {formatted_value}")

        await PaginationHelper.paginate_list(
            ctx,
            formatted_items,
            page_size=page_size,
            title=title,
            numbered=False
        )

    @staticmethod
    def calculate_pages(total_items: int, page_size: int) -> int:
        """
        Calculate number of pages needed

        Args:
            total_items: Total number of items
            page_size: Items per page

        Returns:
            Number of pages
        """
        return (total_items + page_size - 1) // page_size

    @staticmethod
    def get_page_items(
        items: list[Any],
        page: int,
        page_size: int
    ) -> list[Any]:
        """
        Get items for specific page

        Args:
            items: List of all items
            page: Page number (0-indexed)
            page_size: Items per page

        Returns:
            List of items for that page
        """
        start = page * page_size
        end = start + page_size
        return items[start:end]

    @staticmethod
    def get_page_info(
        total_items: int,
        page: int,
        page_size: int
    ) -> dict:
        """
        Get information about page

        Args:
            total_items: Total number of items
            page: Page number (0-indexed)
            page_size: Items per page

        Returns:
            Dictionary with page info:
            - total_pages: Total number of pages
            - total_items: Total number of items
            - page: Current page (0-indexed)
            - page_size: Items per page
            - start: First item number (1-indexed)
            - end: Last item number (1-indexed)
            - has_prev: Has previous page
            - has_next: Has next page
        """
        total_pages = (total_items + page_size - 1) // page_size

        return {
            "total_pages": total_pages,
            "total_items": total_items,
            "page": page,
            "page_size": page_size,
            "start": page * page_size + 1,
            "end": min((page + 1) * page_size, total_items),
            "has_prev": page > 0,
            "has_next": page < total_pages - 1,
        }


class Pagination:
    """Inline keyboard pagination for callback-based navigation.

    Generates an inline keyboard with pagination buttons for a list of items.
    Navigation callbacks follow the pattern ``{prefix}_{session_id}_{page}``.

    Args:
        items: List of items to paginate
        page_size: Number of items per page
        callback_prefix: Prefix for callback data (e.g., ``"search_page"``)
        session_id: Unique session identifier for this pagination instance
        item_formatter: Optional callable to format each item button label

    Examples:
        >>> items = [f"Item {i}" for i in range(1, 50)]
        >>> pagination = Pagination(items=items, page_size=5, callback_prefix="items")
        >>> kb = pagination.get_keyboard(page=0)
        >>> await ctx.reply("Page 1:", reply_markup=kb)
    """

    def __init__(
        self,
        items: list[Any],
        page_size: int = 10,
        callback_prefix: str = "page",
        session_id: Optional[str] = None,
        item_formatter: Optional[Callable[[Any, int], str]] = None,
    ):
        self.items = items
        self.page_size = max(1, page_size)
        self.callback_prefix = callback_prefix
        self.session_id = session_id or ""
        self.item_formatter = item_formatter or (lambda item, index: str(item))

    def get_page_info(self, page: int) -> dict:
        """Get information about a specific page.

        Args:
            page: Page number (0-indexed)

        Returns:
            Dictionary with page info
        """
        return PaginationHelper.get_page_info(len(self.items), page, self.page_size)

    def get_page_items(self, page: int) -> list[Any]:
        """Get items for a specific page.

        Args:
            page: Page number (0-indexed)

        Returns:
            List of items for that page
        """
        return PaginationHelper.get_page_items(self.items, page, self.page_size)

    def get_keyboard(self, page: int, extra_buttons: Optional[list[tuple[str, str]]] = None) -> Any:
        """Build inline keyboard for a specific page.

        Args:
            page: Page number (0-indexed)
            extra_buttons: Optional list of (label, callback_data) for extra buttons

        Returns:
            Inline keyboard markup
        """
        from grathon.high_level import KeyboardBuilder

        kb = KeyboardBuilder()
        info = self.get_page_info(page)
        page_items = self.get_page_items(page)

        # Add item buttons
        for idx, item in enumerate(page_items):
            global_idx = info["start"] + idx - 1
            label = self.item_formatter(item, global_idx)
            kb.button(label, f"pagination_{self.session_id}_{self.callback_prefix}_{page}_{global_idx}")
            kb.row()

        # Add navigation buttons
        if info["has_prev"] or info["has_next"]:
            if info["has_prev"]:
                kb.button("⬅️ قبلی", f"pagination_{self.session_id}_{self.callback_prefix}_{page - 1}")
            if info["has_next"]:
                kb.button("➡️ بعدی", f"pagination_{self.session_id}_{self.callback_prefix}_{page + 1}")
            kb.row()

        # Add extra buttons
        if extra_buttons:
            for label, callback in extra_buttons:
                kb.button(label, callback)
            kb.row()

        return kb.build()

    def build_callback(self, page: int) -> str:
        """Build callback data for a specific page.

        Args:
            page: Page number (0-indexed)

        Returns:
            Callback data string
        """
        return f"pagination_{self.session_id}_{self.callback_prefix}_{page}"
