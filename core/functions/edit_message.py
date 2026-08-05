"""
Edit message helper function

Abstracts the API call for editing messages
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Optional

from grathon.core.TLSchema_Manager.tltypes import (
    formattedText,
    inputMessageText,
    ReplyMarkup, Message,
)
from grathon.core.errors.SendMessageException import SendMessageException

if TYPE_CHECKING:
    from grathon.core.contexts.context import Context


async def edit_message_text(
    ctx: 'Context',
    chat_id: int,
    message_id: int,
    text: formattedText,
    reply_markup: Optional[ReplyMarkup] = None,
) -> Message:
    """
    Edit a message's text content

    Args:
        ctx: Context object
        chat_id: ID of chat containing the message
        message_id: ID of message to edit
        text: New formatted text
        reply_markup: Optional new keyboard

    Returns:
        Response from API

    Raises:
        SendMessageException: If API call fails

    Examples:
        await edit_message_text(ctx, chat_id, msg_id, new_text)
    """
    try:
        input_content = inputMessageText(
            text=text,
            link_preview_options=None,
            clear_draft=False,
        )

        response = await ctx.api.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup,  # pyright: ignore [reportArgumentType]
            input_message_content=input_content,
        )

        return response

    except asyncio.CancelledError:
        raise
    except Exception as e:
        raise SendMessageException(exception=e)
