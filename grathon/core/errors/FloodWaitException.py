"""
FloodWaitException — raised when Telegram enforces a rate limit

Usage:
    from grathon.core.errors import FloodWaitException

    try:
        await ctx.reply("Hello")
    except FloodWaitException as e:
        print(f"Wait {e.wait_seconds}s before retrying")
"""

from __future__ import annotations
import re
from typing import Any, Optional


class FloodWaitException(Exception):
    """Raised when Telegram returns a FLOOD_WAIT error

    Attributes:
        wait_seconds: Number of seconds to wait before retrying
        original_error: The original error/exception that caused this
    """

    # Patterns Telegram uses for flood wait errors
    _PATTERNS = [
        r"FLOOD_WAIT:\s*Wait\s+(\d+)",
        r"FLOOD_WAIT\]\s*Wait\s+(\d+)",
        r"retry after (\d+)",
    ]

    def __init__(self, wait_seconds: int, original_error: Any = None):
        self.wait_seconds = wait_seconds
        self.original_error = original_error
        super().__init__(f"FLOOD_WAIT: must wait {wait_seconds}s")

    @classmethod
    def from_error(cls, error: Any) -> Optional["FloodWaitException"]:
        """Try to parse a FloodWaitException from an error

        Args:
            error: Any error/exception to parse

        Returns:
            FloodWaitException if the error is a flood wait, None otherwise
        """
        error_str = str(error)
        for pattern in cls._PATTERNS:
            match = re.search(pattern, error_str, re.IGNORECASE)
            if match:
                return cls(wait_seconds=int(match.group(1)), original_error=error)
        return None
