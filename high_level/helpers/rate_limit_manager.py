"""RateLimitManager — proactive rate limiting and retry with flood wait handling."""

from __future__ import annotations

import asyncio
import logging
import time
import re
from typing import Callable, Optional, List, Any, Awaitable
from dataclasses import dataclass, field

logger = logging.getLogger("grathon.rate_limit")


@dataclass
class RateLimitEvent:
    """Information about a rate limit event."""
    chat_id: int
    error_message: str
    wait_seconds: float
    timestamp: float = field(default_factory=time.time)
    retry_count: int = 0


class RateLimitManager:
    """Manages rate limiting for message sends with proactive throttling and retry.

    Proactively enforces a minimum interval between sends to avoid hitting
    Telegram's flood limits. If a flood wait error still occurs, it retries
    with exponential backoff.

    Usage:
        from grathon.high_level.helpers.rate_limit_manager import RateLimitManager, install_rate_limit_manager

        # Install as middleware on the TDLib client
        install_rate_limit_manager(bot._client)

        # Register a callback for rate limit events
        manager = RateLimitManager.get_instance()
        manager.on_rate_limited(async def on_rate_limited(event):
            await bot.send_message(event.chat_id, f"⚠️ Rate limited. Retrying in {event.wait_seconds}s")
        )

        # Use in message sending helpers
        manager = RateLimitManager.get_instance()
        await manager.send(api.send_message, chat_id=chat_id, text="Hello")
    """

    _instance: Optional["RateLimitManager"] = None

    def __init__(
        self,
        min_interval: float = 1.0,
        max_retries: int = 5,
        base_delay: float = 2.0,
        max_delay: float = 60.0,
        backoff_multiplier: float = 1.5,
    ):
        self._min_interval = min_interval
        self._max_retries = max_retries
        self._base_delay = base_delay
        self._max_delay = max_delay
        self._backoff_multiplier = backoff_multiplier

        self._last_send_time: float = 0.0
        self._rate_limited = False
        self._current_wait = 0.0
        self._event_handlers: List[Callable[[RateLimitEvent], Awaitable[None]]] = []
        self._lock = asyncio.Lock()

    @classmethod
    def get_instance(cls) -> "RateLimitManager":
        """Get or create the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance."""
        cls._instance = None

    def on_rate_limited(self, handler: Callable[[RateLimitEvent], Awaitable[None]]) -> Callable:
        """Register a callback for rate limit events.

        Args:
            handler: Async function that receives a RateLimitEvent

        Returns:
            The handler (for use as decorator)
        """
        self._event_handlers.append(handler)
        return handler

    def off_rate_limited(self, handler: Callable[[RateLimitEvent], Awaitable[None]]) -> bool:
        """Unregister a rate limit event handler.

        Returns True if the handler was found and removed, False otherwise.
        """
        try:
            self._event_handlers.remove(handler)
            return True
        except ValueError:
            return False

    async def _notify_handlers(self, event: RateLimitEvent) -> None:
        """Notify all registered rate limit event handlers."""
        for handler in self._event_handlers:
            try:
                await handler(event)
            except Exception as e:
                logger.error("Rate limit handler failed: %s", e, exc_info=True)

    async def send(
        self,
        func: Callable,
        *args,
        **kwargs,
    ) -> Any:
        """Send a message through the rate limit manager with proactive throttling and retry.

        Args:
            func: The async function to call (e.g., api.send_message)
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            The result of func(*args, **kwargs)
        """
        async with self._lock:
            # Proactive rate limiting: enforce minimum interval between sends
            now = time.time()
            elapsed = now - self._last_send_time
            if elapsed < self._min_interval:
                wait_time = self._min_interval - elapsed
                logger.debug("Rate limit throttle: waiting %.1fs before send", wait_time)
                await asyncio.sleep(wait_time)

            self._last_send_time = time.time()
            last_error = None

            for attempt in range(self._max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    wait = self._parse_flood_wait(e)

                    if wait is not None and attempt < self._max_retries:
                        actual_wait = min(wait, self._max_delay)
                        self._rate_limited = True
                        self._current_wait = actual_wait

                        chat_id = kwargs.get("chat_id", 0)
                        event = RateLimitEvent(
                            chat_id=chat_id,
                            error_message=str(e),
                            wait_seconds=actual_wait,
                            retry_count=attempt + 1,
                        )
                        await self._notify_handlers(event)

                        logger.warning(
                            "Flood wait: %ds (attempt %d/%d)",
                            actual_wait, attempt + 1, self._max_retries,
                        )

                        await asyncio.sleep(actual_wait)
                        # Update last_send_time so next send also throttles
                        self._last_send_time = time.time()
                        continue

                    self._rate_limited = False
                    raise

            raise last_error

    @staticmethod
    def _parse_flood_wait(error: Any) -> Optional[float]:
        """Extract flood wait seconds from an error."""
        error_str = str(error)
        patterns = [
            r"FLOOD_WAIT:\s*Wait\s+(\d+)",
            r"FLOOD_WAIT\]\s*Wait\s+(\d+)",
            r"retry after (\d+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, error_str, re.IGNORECASE)
            if match:
                return float(match.group(1))
        return None

    @property
    def is_rate_limited(self) -> bool:
        """Whether the manager is currently rate limited."""
        return self._rate_limited

    @property
    def current_wait(self) -> float:
        """Current wait time in seconds."""
        return self._current_wait


def install_rate_limit_manager(client) -> RateLimitManager:
    """Install RateLimitManager as middleware on the TDLib client.

    Usage:
        from grathon.high_level.helpers.rate_limit_manager import install_rate_limit_manager
        install_rate_limit_manager(bot._client)

    Args:
        client: TdClient instance

    Returns:
        The RateLimitManager instance
    """
    manager = RateLimitManager.get_instance()
    logger.info("RateLimitManager installed")
    return manager


__all__ = [
    "RateLimitManager",
    "RateLimitEvent",
    "install_rate_limit_manager",
]
