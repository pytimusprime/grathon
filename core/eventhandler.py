from __future__ import annotations

import asyncio
import logging
from typing import List, Callable, Awaitable, Generic, TypeVar, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from grathon.contexts.context import Context  # pyright: ignore [reportMissingImports]

logger = logging.getLogger(__name__)

TUpdate = TypeVar("TUpdate")

class EventHandler(Generic[TUpdate]):
    def __init__(
        self,
        event_type: type[TUpdate],
        callback: Callable[['Context[TUpdate]'], Any],
        filters: List[Callable[['Context[TUpdate]'], Awaitable[bool]]] | None = None,
    ):
        super().__init__()
        self.event_type = event_type
        self.callback = callback
        self.filters = filters or []

    async def check_and_execute(self, ctx: 'Context[TUpdate]') -> bool:
        """Execute handler if type and filters match."""

        if not isinstance(ctx.update, self.event_type):
            return False

        try:
            for f in self.filters:
                result = await f(ctx)
                if not result:
                    logger.debug(
                        "[FILTER SKIP] handler=%s filter=%s result=False",
                        self.callback.__name__, type(f).__name__,
                    )
                    return False
        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"[FILTER ERROR] handler={self.callback.__name__} filter={type(f).__name__} error={e}")
            await self._route_error(e, ctx, source="filter")
            return False

        try:
            print(f"[HANDLER RUN] handler={self.callback.__name__}")
            await self.callback(ctx)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"[HANDLER ERROR] handler={self.callback.__name__} error={e}")
            await self._route_error(e, ctx, source="callback")

        return True

    async def _route_error(self, error: Exception, ctx: 'Context[TUpdate]', source: str) -> None:
        """Forward an error to the client's central error_handler, falling
        back to a local logger if no handler is wired up."""
        error_handler = getattr(getattr(ctx, 'client', None), 'error_handler', None)
        if error_handler is not None:
            try:
                await error_handler.handle(error, ctx)
            except Exception:
                logger.exception(
                    "Central error_handler crashed while handling %s error in '%s'",
                    source, self.callback.__name__,
                )
        else:
            logger.exception(
                "Unhandled %s error in handler '%s'", source, self.callback.__name__,
            )