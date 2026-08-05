"""
Delete message helper function

Abstracts the API call for deleting messages
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, List, Any, Coroutine

from grathon.core.TLSchema_Manager.tltypes import Ok
from grathon.core.errors.SendMessageException import SendMessageException

if TYPE_CHECKING:
    from grathon.core.contexts.context import Context


async def delete_messages(
    ctx: 'Context',
    chat_id: int,
    message_ids: List[int],
    revoke: bool = True,
) -> Ok:
    """
    Delete one or more messages

    Args:
        ctx: Context object
        chat_id: ID of chat containing messages
        message_ids: List of message IDs to delete
        revoke: Delete for all users (default: True)

    Returns:
        Response from API

    Raises:
        SendMessageException: If API call fails

    Examples:
        # Delete single message
        await delete_messages(ctx, chat_id, [msg_id])

        # Delete multiple messages
        await delete_messages(ctx, chat_id, [id1, id2, id3])

        # Delete for current user only
        await delete_messages(ctx, chat_id, [msg_id], revoke=False)
    """
    try:
        response = await ctx.api.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=revoke,
        )

        return response

    except asyncio.CancelledError:
        raise
    except Exception as e:
        raise SendMessageException(exception=e)
