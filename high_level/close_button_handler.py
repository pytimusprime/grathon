"""Auto-close button handler for Grathon

Provides automatic handling of close/cancel buttons created with KeyboardBuilder.close_button()
"""

import json
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from grathon.core.contexts.context import Context
    from grathon.core.TLSchema_Manager.tltypes import updateNewCallbackQuery

from grathon.core.contexts.CallbackQueryCtx import CallbackQueryCtx


async def auto_handle_close_button(ctx: Union[CallbackQueryCtx, "Context[updateNewCallbackQuery]"]) -> bool:
    """
    Auto-handle close button callbacks (internal Grathon feature)

    Works with both CallbackQueryCtx (from plugin routers) and Context[updateNewCallbackQuery]

    When a close button is clicked:
    - If closing_message is set: Edit message to show closing message (keyboard removed)
    - If closing_message is empty: Just remove keyboard silently

    Usage:
        # Add this to your plugin before other callback handlers:
        @router.on(updateNewCallbackQuery)
        async def handle_callbacks(ctx):  # ctx is CallbackQueryCtx
            if await auto_handle_close_button(ctx):
                return  # Close button was handled
            # ... rest of your callback handlers
    """
    try:
        # Ensure ctx is CallbackQueryCtx (has required attributes)
        if not hasattr(ctx, "data_str"):
            return False
        if not ctx.data_str:  # type: ignore
            return False

        # Try to decompress if needed
        from grathon.high_level.callback_db import resolve_callback
        data_str = ctx.data_str  # type: ignore
        print(f"[DEBUG] Close button check - data_str: {data_str[:100]}")  # DEBUG

        resolved = resolve_callback(data_str)
        if resolved:
            print(f"[DEBUG] Resolved compressed data: {resolved[:100]}")  # DEBUG
            data_str = resolved

        # Try to parse as JSON (close button uses dict format)
        try:
            callback_dict = json.loads(data_str)
            print(f"[DEBUG] Parsed JSON: {callback_dict}")  # DEBUG
        except (json.JSONDecodeError, ValueError) as e:
            print(f"[DEBUG] Not JSON: {e}")  # DEBUG
            return False

        # Check if it's a close button marker
        if callback_dict.get("__grathon_close__") is not True:
            print(f"[DEBUG] Not a close button: {callback_dict}")  # DEBUG
            return False

        print(f"[DEBUG] ✅ Close button detected!")  # DEBUG

        # Get closing message (if any)
        closing_message = callback_dict.get("message", "").strip()

        if closing_message:
            # Replace message with closing message (keyboard removed)
            print(f"[DEBUG] Editing message with closing_message: {closing_message}")  # DEBUG
            await ctx.edit_message(closing_message, parse_mode="markdown")  # type: ignore
            await ctx.answer()  # Answer the callback  # type: ignore
        else:
            # Remove keyboard by re-editing message with same text but no keyboard
            print(f"[DEBUG] Fetching message to remove keyboard...")  # DEBUG
            try:
                # Fetch the original message
                chat_id = getattr(ctx, 'chat_id', None)  # type: ignore
                message_id = getattr(ctx, 'message_id', None)  # type: ignore
                print(f"[DEBUG] Calling get_message with chat_id={chat_id}, message_id={message_id}")  # DEBUG
                msg = await ctx.api.get_message(chat_id=chat_id, message_id=message_id)  # type: ignore
                print(f"[DEBUG] Got message: {type(msg)} = {msg}")  # DEBUG

                # Extract text from message
                print(f"[DEBUG] Message has content? {hasattr(msg, 'content')}")  # DEBUG
                if msg and hasattr(msg, 'content'):
                    content = getattr(msg, 'content', None)  # type: ignore
                    if content and hasattr(content, 'text') and hasattr(content.text, 'text'):
                        original_text = content.text.text  # type: ignore
                        print(f"[DEBUG] Original text: {original_text[:50]}...")  # DEBUG
                        # Edit with same text but no keyboard
                        await ctx.edit_message(original_text, reply_markup=None)  # type: ignore
                        print(f"[DEBUG] Edited message without keyboard")  # DEBUG
                        await ctx.answer()  # Answer the callback  # type: ignore
                    else:
                        print(f"[DEBUG] Could not extract text, just answering")  # DEBUG
                        await ctx.answer()  # type: ignore
                else:
                    print(f"[DEBUG] Message is None, just answering")  # DEBUG
                    await ctx.answer()  # type: ignore
            except Exception as e:
                print(f"[DEBUG] Error removing keyboard: {e}")  # DEBUG
                # Fallback: just answer
                await ctx.answer()  # type: ignore
        print(f"[DEBUG] ✅ Close button handled successfully!")  # DEBUG
        return True

    except Exception as e:
        # If anything goes wrong, let it pass through to user handlers
        print(f"[DEBUG] Exception in close button handler: {e}")  # DEBUG
        import traceback
        traceback.print_exc()
        return False
