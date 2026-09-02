"""
Middleware to track updateMessageSendSucceeded and updateMessageSendFailed

When TDLib sends updateMessageSendSucceeded:
1. Finalize pending message ID
2. Resolve all waiting futures
3. Update archive ID mapping in utils.files
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from grathon.core.TLSchema_Manager.tltypes import (
    updateMessageSendSucceeded,
    updateMessageSendFailed,
)
from grathon.core.contexts.context import Context
from grathon.high_level.helpers.message_tracker import get_message_tracker

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


async def message_send_middleware(ctx: Context, next_fn) -> None:
    """
    Middleware برای ردگیری ارسال پیام‌های موفق و ناموفق

    وقتی updateMessageSendSucceeded یا updateMessageSendFailed میاد:
    1. MessageTracker را آپدیت میکنیم
    2. به next handler میفرستیم
    3. archive ID mapping را آپدیت میکنیم (برای forward_from_archive)

    Args:
        ctx: Context object
        next_fn: تابع بعدی در chain
    """
    tracker = get_message_tracker()
    update = ctx.update

    # Handle successful send
    if isinstance(update, updateMessageSendSucceeded):
        old_message_id = update.old_message_id
        message = update.message
        print(f"[MIDDLEWARE] updateMessageSendSucceeded: old_id={old_message_id}, message_id={getattr(message, 'id', '?')}, chat_id={getattr(message, 'chat_id', '?')}")

        if message and hasattr(message, 'id'):
            chat_id = message.chat_id
            final_id = message.id

            await tracker.confirm_message(
                chat_id=chat_id,
                pending_message_id=old_message_id,
                final_message_id=final_id,
            )

            # Update archive ID mapping
            try:
                from utils.files import register_temp_id
                register_temp_id(old_message_id, final_id)
            except Exception:
                pass

            logger.debug(
                f"✅ پیام ارسال موفق: chat={chat_id}, "
                f"old_id={old_message_id} → new_id={final_id}"
            )
    
    # Handle failed send
    elif isinstance(update, updateMessageSendFailed):
        message = update.message
        old_message_id = update.old_message_id
        error_obj = update.error
        error_msg = getattr(error_obj, 'message', 'Unknown error')
        print(f"[MIDDLEWARE] updateMessageSendFailed: old_id={old_message_id}, error={error_msg}")
        
        if message:
            chat_id = message.chat_id
            error_message = (
                f"{error_obj.message}" if error_obj and hasattr(error_obj, 'message')
                else "Unknown error"
            )

            error = RuntimeError(f"ارسال پیام ناموفق: {error_message}")

            await tracker.fail_message(
                chat_id=chat_id,
                pending_message_id=old_message_id,
                error=error,
            )

            # Track failed temp ID for archive queue retry
            try:
                from utils.files import _failed_temp_ids, mark_failed_temp
                # Parse Telegram "retry after N" from the error so archive
                # retry sleeps the exact FloodWait instead of re-hitting it.
                retry_after = 0.0
                err_text = error_msg or ""
                try:
                    import re as _re
                    _m = _re.search(r"retry after (\d+)", err_text, _re.IGNORECASE)
                    if _m:
                        retry_after = float(int(_m.group(1)))
                except Exception:
                    pass
                mark_failed_temp(old_message_id, retry_after)
            except Exception:
                # Fallback to the previous bare-set behaviour
                try:
                    from utils.files import _failed_temp_ids
                    _failed_temp_ids.add(old_message_id)
                except Exception:
                    pass

            logger.warning(
                f"❌ پیام ارسال ناموفق: chat={chat_id}, id={old_message_id}, "
                f"error={error_message}"
            )

    # Cleanup expired pending messages periodically
    pending_count = tracker.get_pending_count()
    if pending_count > 10:
        expired = await tracker.cleanup_expired()
        if expired > 0:
            logger.warning(f"⏰ {expired} پیام timeout شده حذف شد")

    # Continue to next middleware/handler
    await next_fn(ctx)


def install_message_send_middleware(client) -> None:
    """
    نصب middleware برای ردگیری ارسال پیام‌ها

    Args:
        client: TdClient instance

    استفاده:
        bot = GrathonBot(...)
        from grathon.high_level.helpers.message_send_middleware import install_message_send_middleware
        install_message_send_middleware(bot._client)
    """
    client.use(message_send_middleware)
    logger.info("✅ Message Send Middleware نصب شد")
