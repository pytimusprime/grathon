"""
Message Tracker for TDLib Async Message Sending

TDLib sends messages asynchronously:
1. Immediate response with pending message (may have temporary ID)
2. Later, updateMessageSendSucceeded arrives with final message ID

This tracker matches pending messages with their final confirmations.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class PendingMessage:
    """Information about a pending message"""
    chat_id: int
    pending_id: int  # temporary ID from initial send
    timestamp: datetime
    future: asyncio.Future
    timeout: float = 5.0

    def is_expired(self) -> bool:
        """Check if timeout has elapsed"""
        elapsed = (datetime.now() - self.timestamp).total_seconds()
        return elapsed > self.timeout


class MessageTracker:
    """
    Track pending messages and correlate with final IDs

    Usage:
        tracker = MessageTracker()

        # When sending
        future = await tracker.track_pending(chat_id, pending_msg)

        # When receiving update
        await tracker.confirm_message(chat_id, pending_id, final_id)

        # Wait for result
        final_id = await future  # or timeout
    """

    def __init__(self):
        self._pending: Dict[Tuple[int, int], PendingMessage] = {}
        self._late_confirmations: Dict[Tuple[int, int], int] = {}
        self._lock = asyncio.Lock()

    async def track_pending(
        self,
        chat_id: int,
        pending_message_id: int,
        timeout: float = 5.0,
    ) -> asyncio.Future:
        """
        Track a pending message

        Args:
            chat_id: Chat ID
            pending_message_id: Temporary message ID
            timeout: Timeout duration (seconds)

        Returns:
            Future that resolves with the result
        """
        async with self._lock:
            key = (chat_id, pending_message_id)

            if key in self._late_confirmations:
                final_id = self._late_confirmations.pop(key)
                future = asyncio.Future()
                future.set_result(final_id)
                logger.debug(
                    f"Tracking started (late confirmation): chat={chat_id}, pending_id={pending_message_id}, final={final_id}"
                )
                return future

            future = asyncio.Future()
            self._pending[key] = PendingMessage(
                chat_id=chat_id,
                pending_id=pending_message_id,
                timestamp=datetime.now(),
                future=future,
                timeout=timeout,
            )

            logger.debug(
                f"Tracking started: chat={chat_id}, pending_id={pending_message_id}"
            )

            return future

    async def confirm_message(
        self,
        chat_id: int,
        pending_message_id: int,
        final_message_id: int,
    ) -> bool:
        """
        تائید پیام با final ID

        Args:
            chat_id: شناسه چت
            pending_message_id: ID موقتی
            final_message_id: ID نهایی

        Returns:
            True اگر تائید شد، False اگر pending نبود
        """
        async with self._lock:
            key = (chat_id, pending_message_id)

            if key not in self._pending:
                logger.debug(
                    f"پیام pending یافت نشد، ذخیره تأیید دیرهنگام: chat={chat_id}, id={pending_message_id}, final={final_message_id}"
                )
                self._late_confirmations[key] = final_message_id
                return False

            pending = self._pending.pop(key)

            if not pending.future.done():
                pending.future.set_result(final_message_id)
                logger.debug(
                    f"تائید شد: chat={chat_id}, pending={pending_message_id}, final={final_message_id}"
                )
                return True

            return False

    async def fail_message(
        self,
        chat_id: int,
        pending_message_id: int,
        error: Exception,
    ) -> bool:
        """
        Mark a message as failed with an error

        Args:
            chat_id: Chat ID
            pending_message_id: Temporary message ID
            error: The error that occurred

        Returns:
            True if failed, False if pending message not found
        """
        async with self._lock:
            key = (chat_id, pending_message_id)

            if key not in self._pending:
                return False

            pending = self._pending.pop(key)

            if not pending.future.done():
                pending.future.set_exception(error)
                logger.error(
                    f"Message failed: chat={chat_id}, id={pending_message_id}, error={error}"
                )
                return True

            return False

    async def cleanup_expired(self) -> int:
        """
        حذف پیام‌های expired

        Returns:
            تعداد پیام‌های حذف شده
        """
        async with self._lock:
            expired_keys = [
                key for key, pending in self._pending.items()
                if pending.is_expired()
            ]

            for key in expired_keys:
                pending = self._pending.pop(key)
                if not pending.future.done():
                    pending.future.set_exception(
                        TimeoutError(f"انتظار برای پیام timeout شد: {key}")
                    )
                logger.warning(
                    f"پیام timeout: chat={pending.chat_id}, id={pending.pending_id}"
                )

            return len(expired_keys)

    def get_pending_count(self) -> int:
        """Get count of pending messages"""
        return len(self._pending)

    async def clear(self):
        """Clear all pending messages"""
        async with self._lock:
            for pending in self._pending.values():
                if not pending.future.done():
                    pending.future.set_exception(
                        RuntimeError("MessageTracker cleared")
                    )
            self._pending.clear()


# Singleton instance
_message_tracker: Optional[MessageTracker] = None


def get_message_tracker() -> MessageTracker:
    """Get singleton MessageTracker instance"""
    global _message_tracker
    if _message_tracker is None:
        _message_tracker = MessageTracker()
    return _message_tracker
