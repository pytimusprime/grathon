"""
Forward message helper function

Abstracts the API call for forwarding messages
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, List

from grathon.core.TLSchema_Manager.tltypes import messages as MessagesType, message
from grathon.core.errors.SendMessageException import SendMessageException

if TYPE_CHECKING:
    from grathon.core.contexts.context import Context


async def forward_messages(
    ctx: 'Context',
    chat_id: int,
    from_chat_id: int,
    message_ids: List[int],
    send_copy: bool = False,
    remove_caption: bool = False,
    wait_for_confirmation: bool = True,
    confirmation_timeout: float = 5.0,
):
    """
    Forward one or more messages to another chat

    Args:
        ctx: Context object
        chat_id: Destination chat ID
        from_chat_id: Source chat ID
        message_ids: List of message IDs to forward
        send_copy: If True, sends as copy (hides "forwarded from")
        remove_caption: If True, removes captions from forwarded messages
        wait_for_confirmation: Wait for final confirmation (default: True)
        confirmation_timeout: Timeout for confirmation (seconds)

    Returns:
        Messages object with final message IDs

    Raises:
        SendMessageException: If API call fails

    Examples:
        # Forward single message - wait for confirmation
        await forward_messages(ctx, to_chat_id, from_chat_id, [msg_id])

        # Forward as copy - don't wait for confirmation
        await forward_messages(
            ctx, to_chat_id, from_chat_id, [msg_id],
            send_copy=True,
            wait_for_confirmation=False
        )

        # Forward multiple messages
        await forward_messages(ctx, to_chat_id, from_chat_id, [id1, id2, id3])
    """
    try:
        # Send forward request
        pending_messages = await ctx.api.forward_messages(
            chat_id=chat_id,
            from_chat_id=from_chat_id,
            message_ids=message_ids,
            send_copy=send_copy,
            remove_caption=remove_caption
        )

        # Handle confirmation waiting
        if wait_for_confirmation and isinstance(pending_messages, MessagesType):
            if pending_messages.messages:
                from grathon.high_level.helpers.message_tracker import get_message_tracker

                tracker = get_message_tracker()

                # Track each pending message
                futures = []
                for msg in pending_messages.messages:
                    if isinstance(msg, message):
                        try:
                            future = await tracker.track_pending(
                                chat_id=chat_id,
                                pending_message_id=msg.id,
                                timeout=confirmation_timeout,
                            )
                            futures.append((msg.id, future))
                        except Exception:
                            pass

                # Wait for all confirmations
                if futures:
                    try:
                        results = await asyncio.wait_for(
                            asyncio.gather(*[f[1] for f in futures], return_exceptions=True),
                            timeout=confirmation_timeout + 1
                        )

                        # Update message IDs with final ones
                        for i, msg in enumerate(pending_messages.messages):
                            if i < len(results):
                                final_id = results[i]
                                if isinstance(final_id, int):
                                    msg.id = final_id

                    except asyncio.TimeoutError:
                        # Timeout - return pending messages as-is
                        pass

        return pending_messages

    except asyncio.CancelledError:
        raise
    except Exception as e:
        raise SendMessageException(exception=e)
