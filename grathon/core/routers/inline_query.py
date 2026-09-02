"""Router for inline query events with filter support"""

from typing import Optional, Any, Callable, List

from grathon.core.router import Router
from grathon.core.TLSchema_Manager.tltypes import updateNewInlineQuery


class InlineQueryRouter(Router[updateNewInlineQuery]):
    """Router for inline query events with filter support"""

    def __init__(self) -> None:
        super().__init__(name="InlineQueryRouter")

    def on_inline_query(
        self,
        func: Optional[Callable[..., Any]] = None,
        filters: Optional[List[Any]] = None,
    ):
        """Register a handler for inline query events with optional filters

        Usage:
            >>> @router.on_inline_query(filters=[F.query(r"^dog")])
            ... async def handle_dog_search(ctx: InlineQueryCtx):
            ...     results = await search_dogs(ctx.query)
            ...     await ctx.answer_results(results)

            >>> @router.on_inline_query()
            ... async def handle_all_queries(ctx: InlineQueryCtx):
            ...     print(f"Query: {ctx.query}")
        """
        if func is not None:
            return self.on(updateNewInlineQuery, filters=filters, callback=func)
        return self.on(updateNewInlineQuery, filters=filters)
