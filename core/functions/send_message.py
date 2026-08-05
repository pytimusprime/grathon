"""
send message make sending all type of content easy
and handle all sending message options

"""

import asyncio
from typing import TYPE_CHECKING

from grathon.core.TLSchema_Manager.tltypes import (InputMessageContent, InputMessageReplyTo,
                                          MessageTopic, ReplyMarkup,
                                          messageSendOptions, inputMessageText, formattedText, linkPreviewOptions, message,
                                          messageSendingStateFailed)
from grathon.core.contexts.context import Context, TUpdate
from grathon.core.errors.SendMessageException import SendMessageException

if TYPE_CHECKING:
    pass



def create_formating_entities():
    ...

def create_input_text(
        text: formattedText | None = None,
        link_preview_options: linkPreviewOptions | None = None,
        clear_draft: bool | None = None
):
    return inputMessageText(
        text,
        link_preview_options,
        clear_draft=clear_draft
    )


async def send_message_base(
    ctx: Context[TUpdate],
    chat_id: int,
    topic_id: MessageTopic | None,
    reply_to: InputMessageReplyTo | None,
    options: messageSendOptions,
    reply_markup: ReplyMarkup | None,
    input_message_content: InputMessageContent,
    wait_for_confirmation: bool = True,
    confirmation_timeout: float = 5.0,
):
    try:
        response = await ctx.api.send_message(
            chat_id=chat_id,
            topic_id=topic_id,  # pyright: ignore [reportArgumentType]
            reply_to=reply_to,  # pyright: ignore [reportArgumentType]
            options=options,
            reply_markup=reply_markup,  # pyright: ignore [reportArgumentType]
            input_message_content=input_message_content
        )

        if hasattr(response, '__td_type__') and response.__td_type__ == 'error':
            error_code = getattr(response, 'code', 0)
            error_msg = getattr(response, 'message', 'Unknown error')
            raise SendMessageException(exception=RuntimeError(f"TDLib error {error_code}: {error_msg}"))

        if isinstance(response, message) and response.sending_state is not None:
            if isinstance(response.sending_state, messageSendingStateFailed):
                error_msg = getattr(getattr(response.sending_state, 'error', None), 'message', 'Unknown error')
                raise SendMessageException(exception=RuntimeError(f"Message send failed: {error_msg}"))

        if wait_for_confirmation and isinstance(response, message):
            from grathon.high_level.helpers.message_tracker import get_message_tracker
            tracker = get_message_tracker()
            try:
                print(f"[SEND_BASE] Tracking message: chat={chat_id}, temp_id={response.id}, has_sending_state={hasattr(response, 'sending_state')}, sending_state={getattr(response, 'sending_state', None)}")
                future = await tracker.track_pending(
                    chat_id=chat_id,
                    pending_message_id=response.id,
                    timeout=confirmation_timeout,
                )
                try:
                    final_id = await asyncio.wait_for(
                        future,
                        timeout=confirmation_timeout + 1
                    )
                    print(f"[SEND_BASE] Got final_id={final_id}, updating response.id from {response.id}")
                    if isinstance(final_id, int):
                        response.id = final_id
                except asyncio.TimeoutError:
                    print(f"[SEND_BASE] TIMEOUT waiting for confirmation for temp_id={response.id}")
            except Exception as e:
                print(f"[SEND_BASE] ERROR in confirmation: {e}")

        return response

    except asyncio.CancelledError:
        raise
    except Exception as e:
        raise SendMessageException(exception=e)
