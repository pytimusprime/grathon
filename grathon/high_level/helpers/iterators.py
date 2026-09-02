"""
Async Iterators for chats, messages, etc.
Inspired by Telethon iter_messages, iter_dialogs

Usage:
    async for chat in iter_dialogs(client, limit=100):
        print(chat.title)

    async for msg in iter_messages(client, chat_id, limit=500):
        print(msg.id)
"""

from __future__ import annotations
from typing import AsyncIterator, Optional, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from grathon.core.tdclient import TdClient


async def iter_dialogs(
    client: "TdClient",
    limit: Optional[int] = None,
    chat_list: Any = None,
    chunk_size: int = 100,
) -> AsyncIterator[int]:
    """
    Iterate over all chats/dialogs.

    مثل Telethon iter_dialogs - با offset خودکار همه chat ها رو لود می‌کنه

    Args:
        client: TdClient instance
        limit: حداکثر تعداد chat برای دریافت (None = همه)
        chat_list: نوع لیست (Main, Archive, ...). None = پیش‌فرض
        chunk_size: تعداد chat در هر batch

    Yields:
        chat_id ها به ترتیب

    Example:
        async for chat_id in iter_dialogs(client, limit=100):
            chat = await client.api.get_chat(chat_id=chat_id)
            print(chat.title)
    """
    seen: set[int] = set()
    yielded = 0

    while True:
        # Load بیشتر chats از سرور
        try:
            await client.api.load_chats(
                chat_list=chat_list,
                limit=chunk_size,
            )
        except Exception:
            # ممکنه که همه chat ها لود شده‌اند
            pass

        # دریافت chats
        result = await client.api.get_chats(
            chat_list=chat_list,
            limit=chunk_size if limit is None else min(chunk_size, (limit - yielded) + 50),
        )

        chat_ids = getattr(result, "chat_ids", []) or []
        if not chat_ids:
            break

        # بررسی chat های جدید
        new_chats = [c for c in chat_ids if c not in seen]
        if not new_chats:
            # دیگر chat جدیدی نیست
            break

        for chat_id in new_chats:
            seen.add(chat_id)
            yield chat_id
            yielded += 1
            if limit is not None and yielded >= limit:
                return


async def iter_messages(
    client: "TdClient",
    chat_id: int,
    limit: Optional[int] = None,
    from_message_id: int = 0,
    offset: int = 0,
    chunk_size: int = 100,
    only_local: bool = False,
) -> AsyncIterator[Any]:
    """
    Iterate over messages in a chat.

    مثل Telethon iter_messages - با offset خودکار همه پیام‌ها رو لود می‌کنه

    Args:
        client: TdClient instance
        chat_id: شناسه chat
        limit: حداکثر تعداد message (None = همه)
        from_message_id: شروع از این message_id (0 = آخرین)
        offset: تعداد پیام برای skip
        chunk_size: تعداد در هر batch
        only_local: فقط از cache (نه از سرور)

    Yields:
        message objects به ترتیب (newest first)

    Example:
        async for msg in iter_messages(client, chat_id=12345, limit=500):
            print(msg.id, msg.content)
    """
    yielded = 0
    current_from_id = from_message_id

    while True:
        # محاسبه limit برای این batch
        batch_limit = chunk_size
        if limit is not None:
            remaining = limit - yielded
            if remaining <= 0:
                return
            batch_limit = min(chunk_size, remaining)

        # دریافت history
        result = await client.api.get_chat_history(
            chat_id=chat_id,
            from_message_id=current_from_id,
            offset=offset,
            limit=batch_limit,
            only_local=only_local,
        )

        messages = getattr(result, "messages", []) or []
        if not messages:
            # بدون message دیگر
            break

        # yield کردن messages
        last_msg_id = None
        for msg in messages:
            yield msg
            yielded += 1
            last_msg_id = getattr(msg, "id", None)
            if limit is not None and yielded >= limit:
                return

        # اگر offset استفاده شد، فقط برای اولین batch
        offset = 0

        # برای batch بعدی، از آخرین message شروع کن
        if last_msg_id is None:
            break
        current_from_id = last_msg_id

        # اگر تعداد دریافتی کمتر از خواسته بود، احتمالاً به انتها رسیدیم
        if len(messages) < batch_limit:
            break


async def iter_chat_history(
    client: "TdClient",
    chat_id: int,
    limit: Optional[int] = None,
    chunk_size: int = 100,
) -> AsyncIterator[Any]:
    """
    Alias برای iter_messages - برای راحتی

    Example:
        async for msg in iter_chat_history(client, chat_id, limit=1000):
            ...
    """
    async for msg in iter_messages(
        client=client,
        chat_id=chat_id,
        limit=limit,
        chunk_size=chunk_size,
    ):
        yield msg


async def search_messages(
    client: "TdClient",
    chat_id: int,
    query: str = "",
    limit: Optional[int] = None,
    chunk_size: int = 100,
    filter: Any = None,
) -> AsyncIterator[Any]:
    """
    جستجو در پیام‌های یک chat با pagination خودکار

    Args:
        client: TdClient instance
        chat_id: شناسه chat
        query: متن جستجو
        limit: حداکثر تعداد نتیجه
        chunk_size: تعداد در هر batch
        filter: فیلتر TDLib (مثلاً searchMessagesFilterPhoto)

    Yields:
        پیام‌های یافت‌شده

    Example:
        async for msg in search_messages(client, chat_id, query="hello", limit=50):
            print(msg)
    """
    yielded = 0
    from_message_id = 0

    while True:
        batch_limit = chunk_size
        if limit is not None:
            remaining = limit - yielded
            if remaining <= 0:
                return
            batch_limit = min(chunk_size, remaining)

        result = await client.api.search_chat_messages(
            chat_id=chat_id,
            topic_id=None,
            query=query,
            sender_id=None,
            from_message_id=from_message_id,
            offset=0,
            limit=batch_limit,
            filter=filter,
        )

        messages = getattr(result, "messages", []) or []
        if not messages:
            break

        last_id = None
        for msg in messages:
            yield msg
            yielded += 1
            last_id = getattr(msg, "id", None)
            if limit is not None and yielded >= limit:
                return

        if last_id is None or len(messages) < batch_limit:
            break
        from_message_id = last_id
