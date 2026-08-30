"""Router for callback query events with filter support"""

import json
from typing import Optional, Any, Callable, List

from grathon.core.router import Router
from grathon.core.TLSchema_Manager.tltypes import updateNewCallbackQuery


class CallbackQueryRouter(Router[updateNewCallbackQuery]):
    """Router for inline button callbacks with filter support"""

    def __init__(self) -> None:
        super().__init__(name="CallbackQueryRouter")
        self._auto_handle_close_button = True

    def on_callback_query(
        self,
        func: Optional[Callable[..., Any]] = None,
        filters: Optional[List[Any]] = None,
    ):
        """Register a handler for callback query events with optional filters

        Usage:
            >>> @router.on_callback_query(filters=[F.callback(r"^confirm")])
            ... async def handle_confirm(ctx: CallbackQueryCtx):
            ...     await ctx.answer("Confirmed!")

            >>> @router.on_callback_query()
            ... async def handle_all_callbacks(ctx: CallbackQueryCtx):
            ...     print(ctx.data_str)
        """
        if func is not None:
            return self.on(updateNewCallbackQuery, filters=filters, callback=func)
        return self.on(updateNewCallbackQuery, filters=filters)

    async def handle_close_button(self, ctx) -> bool:
        """Auto-handle close button callbacks

        Returns True if a close button was handled, False otherwise
        """
        if not self._auto_handle_close_button:
            return False

        try:
            # Try to parse as close button callback
            data_str = ctx.data_str
            if not data_str:
                return False

            # Try to decompress if needed
            from grathon.high_level.callback_db import resolve_callback
            resolved = resolve_callback(data_str)
            if resolved:
                data_str = resolved

            # Try to parse as JSON
            callback_dict = json.loads(data_str)

            # Check if it's a close button
            if callback_dict.get("__grathon_close__") is True:
                closing_message = callback_dict.get("message", "")

                if closing_message:
                    # Replace message with closing message (remove keyboard)
                    await ctx.edit_message(closing_message, parse_mode="markdown")
                else:
                    # Just remove the keyboard, keep the message text
                    await ctx.edit_message(
                        message_text=None,  # Keep original text
                        reply_markup=None   # Remove keyboard
                    )

                # Answer the button click
                await ctx.answer()
                return True

        except (json.JSONDecodeError, ValueError, AttributeError):
            # Not a close button, let user handlers process it
            pass

        return False
