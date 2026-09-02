from __future__ import annotations

import asyncio
import re
import logging
from typing import Callable, Optional, List, Type, Any

logger = logging.getLogger("grathon.retry")


class FloodWaitError(Exception):
    """Telegram FLOOD_WAIT error parsed from update"""

    def __init__(self, wait_seconds: int, original_error: Any = None):
        self.wait_seconds = wait_seconds
        self.original_error = original_error
        super().__init__(f"FLOOD_WAIT: must wait {wait_seconds}s")


def parse_flood_wait(error: Any) -> Optional[int]:
    """Extract flood wait seconds from TDLib error string

    TDLib returns errors like:
        "FLOOD_WAIT: Wait 30 seconds"
        "[420 FLOOD_WAIT] Wait 15 seconds"
        "Too Many Requests: retry after 25"

    Returns:
        Number of seconds to wait, or None if not a flood wait error
    """
    error_str = str(error)

    patterns = [
        r"FLOOD_WAIT:\s*Wait\s+(\d+)",
        r"FLOOD_WAIT\]\s*Wait\s+(\d+)",
        r"retry after (\d+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, error_str, re.IGNORECASE)
        if match:
            return int(match.group(1))

    return None


def retry_middleware(
    max_retries: int = 3,
    base_delay: float = 2.0,
    max_delay: float = 60.0,
    retry_on: Optional[List[Type[Exception]]] = None,
    on_retry: Optional[Callable[[int, int, Any], Any]] = None,
) -> Callable:
    """Create retry middleware for flood wait and other transient errors

    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        base_delay: Base delay for exponential backoff in seconds (default: 2.0)
        max_delay: Maximum delay between retries (default: 60.0)
        retry_on: List of exception types to retry on. If None, retries on flood wait only.
        on_retry: Callback(attempt, wait_seconds, error) called before each retry

    Returns:
        Middleware function for bot.use()

    Usage:
        from grathon.high_level.middlewares.retry import retry_middleware

        bot.use(retry_middleware())

        # Or with custom config:
        bot.use(retry_middleware(
            max_retries=5,
            base_delay=1.0,
            on_retry=lambda attempt, wait, err: print(f"Retry {attempt} in {wait}s")
        ))
    """
    async def middleware(ctx, next_fn):
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                return await next_fn(ctx)
            except Exception as e:
                last_error = e

                # Check if this is a flood wait error
                wait_seconds = parse_flood_wait(e)

                if wait_seconds is not None:
                    # Cap the delay
                    actual_delay = min(wait_seconds, max_delay)

                    logger.warning(
                        "Flood wait: %ds (attempt %d/%d)",
                        actual_delay, attempt + 1, max_retries + 1
                    )

                    if on_retry:
                        try:
                            result = on_retry(attempt + 1, actual_delay, e)
                            if asyncio.iscoroutine(result):
                                await result
                        except Exception:
                            pass

                    if attempt < max_retries:
                        await asyncio.sleep(actual_delay)
                        continue

                # Not a flood wait or max retries exceeded
                raise

        raise last_error

    return middleware


def auto_retry(
    max_retries: int = 3,
    base_delay: float = 2.0,
    max_delay: float = 60.0,
) -> Callable:
    """Simplified retry middleware — retries on any transient error

    Usage:
        bot.use(auto_retry())
        bot.use(auto_retry(max_retries=5))
    """
    return retry_middleware(
        max_retries=max_retries,
        base_delay=base_delay,
        max_delay=max_delay,
    )
