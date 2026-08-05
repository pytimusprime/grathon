"""Error handling for bot events"""

import logging
from typing import Callable, Optional, List, Any
from grathon.core.contexts.context import Context

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Centralized error handling container"""

    def __init__(self):
        self._handlers: List[Callable[[Exception, Optional[Context]], Any]] = []
        # Register default logger so errors are always logged
        self._handlers.append(self._default_log_handler)

    @staticmethod
    async def _default_log_handler(error: Exception, ctx: Optional[Context] = None) -> None:
        """Default handler that logs all errors to stderr"""
        handler_info = ""
        if ctx is not None:
            update_type = type(ctx.update).__name__ if hasattr(ctx, 'update') else "unknown"
            handler_info = f" (update: {update_type})"
        logger.error("Handler error%s: %s", handler_info, error, exc_info=error)

    def add_handler(self, handler: Callable[[Exception, Optional[Context]], Any]) -> Callable:
        """Register an error handler

        Args:
            handler: Async function that takes (error: Exception, ctx: Optional[Context])

        Returns:
            The handler (for use as decorator)

        Usage:
            @error_handler.add_handler
            async def my_error_handler(error, ctx):
                await ctx.reply(f"Error: {error}")
        """
        self._handlers.append(handler)
        return handler

    def remove_handler(self, handler: Callable[[Exception, Optional[Context]], Any]) -> bool:
        """Unregister a previously-added error handler.

        Returns True if the handler was found and removed, False otherwise.
        """
        try:
            self._handlers.remove(handler)
            return True
        except ValueError:
            return False

    def disable_default_logging(self) -> None:
        """Stop the framework's built-in error logger from running.

        Call this once you've registered your own logging-aware handler
        to avoid every error producing two log entries (one from the
        default logger, one from your handler).
        """
        self.remove_handler(self._default_log_handler)

    async def handle(self, error: Exception, ctx: Optional[Context] = None) -> None:
        """Execute all registered error handlers

        Args:
            error: The exception that occurred
            ctx: Context object if available
        """
        for handler in self._handlers:
            try:
                await handler(error, ctx)
            except Exception as e:
                logger.warning("Error handler failed: %s", e, exc_info=True)
