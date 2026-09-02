"""Context for inline query events (updateNewInlineQuery)"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Any, List

from grathon.core.TLSchema_Manager.tltypes import (
    updateNewInlineQuery,
    InputInlineQueryResult,
    inlineQueryResultsButton,
)
from grathon.core.contexts.context import Context

if TYPE_CHECKING:
    from grathon.core.tdclient import TdClient


class InlineQueryCtx(Context[updateNewInlineQuery]):
    """Rich context for inline query events

    Properties:
        query_id: Unique inline query ID
        sender_user_id: User who sent the query
        query: The search query text
        offset: Pagination offset for results
        chat_type: Type of chat where query was sent ('private', 'group', 'supergroup', 'channel')
        user_location: Optional user location if shared
    """

    def __init__(self, client: TdClient, update: updateNewInlineQuery):
        super().__init__(client, update)
        self.query_id = getattr(update, 'id', None)
        self.sender_user_id = getattr(update, 'sender_user_id', None)
        self.query = getattr(update, 'query', '')
        self.offset = getattr(update, 'offset', '')
        self.chat_type = getattr(update, 'chat_type', None)
        self.user_location = getattr(update, 'user_location', None)

    @property
    def chat_id(self) -> Optional[int]:
        """Inline queries don't have a chat_id (they're from the user directly)"""
        return self.sender_user_id

    @property
    def user_id(self) -> Optional[int]:
        """Get the user ID of who sent the inline query

        Unified accessor — use this instead of sender_user_id directly.

        Examples:
            uid = ctx.user_id
        """
        return self.sender_user_id

    async def answer_results(
        self,
        results: List[InputInlineQueryResult],
        cache_time: int = 300,
        is_personal: bool = False,
        next_offset: Optional[str] = None,
        button: Optional[inlineQueryResultsButton] = None,
    ) -> Any:
        """Answer the inline query with search results

        Args:
            results: List of InlineQueryResult objects
            cache_time: How long (in seconds) to cache results on Telegram (default: 300)
            is_personal: If True, results only visible to the user who made the query
            next_offset: Pagination offset for next set of results
            button: Optional button to show above results

        Examples:
            results = [article_result, photo_result]
            await ctx.answer_results(results)
            await ctx.answer_results(results, is_personal=True, cache_time=0)
        """
        kwargs = {
            "inline_query_id": self.query_id,
            "results": results,
            "cache_time": cache_time,
            "is_personal": is_personal,
        }
        if next_offset is not None:
            kwargs["next_offset"] = next_offset
        if button is not None:
            kwargs["button"] = button

        return await self.api.answer_inline_query(**kwargs)  # type: ignore

    async def answer_empty(
        self,
        cache_time: int = 0,
        button: Optional[inlineQueryResultsButton] = None,
    ) -> Any:
        """Answer with no results (shows empty state)

        Args:
            cache_time: How long (in seconds) to cache the empty result
            button: Optional button to show

        Examples:
            await ctx.answer_empty()
            await ctx.answer_empty(cache_time=30)
        """
        kwargs = {
            "inline_query_id": self.query_id,
            "results": [],
            "cache_time": cache_time,
        }
        if button is not None:
            kwargs["button"] = button

        return await self.api.answer_inline_query(**kwargs)  # type: ignore
