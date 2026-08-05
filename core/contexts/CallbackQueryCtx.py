"""Context for inline button callback queries (updateNewCallbackQuery events)"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Any, Union, cast

from grathon.core.TLSchema_Manager.tltypes import (
    updateNewCallbackQuery,
    callbackQueryPayloadData,
    formattedText,
    inputMessageText,
    ReplyMarkup,
    messageSendOptions,
)
from grathon.core.contexts.context import Context
from grathon.core.functions.send_message import send_message_base

if TYPE_CHECKING:
    import re as re_module
    from grathon.core.tdclient import TdClient
    from grathon.core.contexts.NewMessageCtx import NewMessageCtx


class CallbackQueryCtx(Context[updateNewCallbackQuery]):
    """Rich context for inline button click events

    Properties:
        query_id: Unique callback query ID
        sender_user_id: User who clicked the button
        chat_id: Chat containing the message with button
        message_id: Message ID of the message with button
        data: Raw callback bytes from button
        data_str: Decoded callback data (UTF-8)
    """

    def __init__(self, client: TdClient, update: updateNewCallbackQuery):
        super().__init__(client, update)
        self.query_id = update.id
        self.sender_user_id = update.sender_user_id
        self._chat_id = update.chat_id
        self.message_id = update.message_id
        self.chat_instance = update.chat_instance
        self._payload = update.payload
        self._callback_match: Optional[re_module.Match] = None

    @property
    def chat_id(self) -> Optional[int]:
        """Get chat ID from callback query"""
        return self._chat_id

    @property
    def user_id(self) -> Optional[int]:
        """Get the user ID of who clicked the button

        Unified accessor — use this instead of sender_user_id directly.

        Examples:
            uid = ctx.user_id  # int user ID of the clicking user
        """
        return self.sender_user_id

    @property
    def match(self) -> Optional[re_module.Match]:
        """Get the regex match object from the callback filter

        Set automatically by CallbackDataFilter when F.callback(pattern) matches.
        Use this to access capture groups without re-matching.

        Examples:
            @bot.on_callback(r"^delete_(\\d+)$")
            async def handle(ctx):
                item_id = ctx.match.group(1)  # access captured group
        """
        return self._callback_match

    @property
    def callback_data(self) -> Optional[bytes]:
        """Raw callback bytes from Telegram"""
        if isinstance(self._payload, callbackQueryPayloadData):
            return self._payload.data
        return None

    @property
    def data_str(self) -> Optional[str]:
        """Decoded callback data (UTF-8) — auto-resolves aliases via CallbackStore"""
        raw = self.callback_data
        if isinstance(raw, bytes):
            decoded = raw.decode('utf-8', errors='replace') if raw else None
        elif isinstance(raw, str):
            decoded = raw
        else:
            return None

        if decoded is None:
            return None

        # Resolve callback alias if present (lazy import to avoid circular dependency)
        from grathon.high_level.callback_store import CallbackStore
        resolved = CallbackStore.resolve(decoded)
        if resolved is not None:
            return resolved
        return decoded

    @property
    def session(self) -> dict[str, Any]:
        """Get session data for this chat

        Returns an empty dict if no session store is available.
        Useful for tracking user state across messages without modifying the bot.
        """
        if self.client.session is not None and self.chat_id is not None:
            return self.client.session.get(self.chat_id)
        return {}


    async def answer(self, text: str = "", alert: bool = False) -> Any:
        """Answer the callback query (shows toast or alert in Telegram)

        Args:
            text: Notification text (empty = silent)
            alert: If True, show as alert box; else toast
        """
        return await self.api.answer_callback_query(  # type: ignore
            callback_query_id=self.query_id,
            text=text,
            show_alert=alert
        )

    async def edit_message(
        self,
        text: Union[str, formattedText],
        parse_mode: Optional[str] = "markdown",
        reply_markup: Optional[ReplyMarkup] = None,
    ) -> Any:
        """Edit the message that contained the button

        Args:
            text: New message text (string or formattedText)
            parse_mode: "markdown", "html", or None for plain text
            reply_markup: Optional keyboard/inline buttons

        Returns:
            Response from API

        Examples:
            await ctx.edit_message("Updated text")
            await ctx.edit_message("**Bold**", parse_mode="markdown")
            await ctx.edit_message("<b>Bold</b>", parse_mode="html")
        """
        # Convert string to formattedText if needed
        if isinstance(text, str):
            # Apply formatting if parse_mode specified
            if parse_mode:
                from grathon.high_level.helpers.formatted_text import TextFormatter
                formatter = TextFormatter(self.client)
                if parse_mode.lower() == "markdown":
                    formatted_text = await formatter.markdown(text)
                elif parse_mode.lower() == "html":
                    formatted_text = await formatter.html(text)
                else:
                    formatted_text = formattedText(text=text)
            else:
                formatted_text = formattedText(text=text)
        else:
            formatted_text = text

        input_content = inputMessageText(
            text=formatted_text,
            link_preview_options=None,
            clear_draft=False
        )
        try:
            msg = await self.api.get_message(
                chat_id=self.chat_id, message_id=self.message_id
            )
        except Exception:
            msg = None
        if msg and hasattr(msg, 'content') and msg.content is not None:
            content_type = getattr(msg.content, '__td_type__', '')
            is_media = content_type in (
                'messagePhoto', 'messageVideo', 'messageAudio',
                'messageVoiceNote', 'messageVideoNote', 'messageAnimation',
                'messageDocument', 'messageSticker',
            )
        else:
            is_media = False
        if is_media:
            caption = formatted_text if isinstance(formatted_text, formattedText) else formattedText(text=str(text))
            return await self.api.edit_message_caption(
                chat_id=self.chat_id,
                message_id=self.message_id,
                reply_markup=reply_markup,
                caption=caption,
                show_caption_above_media=False
            )
        try:
            return await self.api.edit_message_text(  # type: ignore
                chat_id=self.chat_id,
                message_id=self.message_id,
                reply_markup=reply_markup,
                input_message_content=input_content
            )
        except Exception:
            caption = formatted_text if isinstance(formatted_text, formattedText) else formattedText(text=str(text))
            return await self.api.edit_message_caption(  # type: ignore
                chat_id=self.chat_id,
                message_id=self.message_id,
                reply_markup=reply_markup,
                caption=caption,
                show_caption_above_media=False
            )

    async def edit_message_markdown(self, text: str, reply_markup: Optional[ReplyMarkup] = None) -> Any:
        """Edit the message with Markdown formatting (shortcut)

        Args:
            text: Message text with Markdown syntax
            reply_markup: Optional keyboard/inline buttons

        Examples:
            >>> await ctx.edit_message_markdown("**Bold** and __italic__")
        """
        return await self.edit_message(text, parse_mode="markdown", reply_markup=reply_markup)

    async def edit_message_html(self, text: str, reply_markup: Optional[ReplyMarkup] = None) -> Any:
        """Edit the message with HTML formatting (shortcut)

        Args:
            text: Message text with HTML tags
            reply_markup: Optional keyboard/inline buttons

        Examples:
            >>> await ctx.edit_message_html("<b>Bold</b> and <i>italic</i>")
        """
        return await self.edit_message(text, parse_mode="html", reply_markup=reply_markup)

    async def edit_message_caption(
        self,
        text: Union[str, formattedText],
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        parse_mode: Optional[str] = "markdown",
        reply_markup: Optional[ReplyMarkup] = None,
        show_caption_above_media: Optional[bool] = False,
    ) -> Any:
        """Edit the caption of a media message (photo/video/animation)

        Use this for messages that contain media (photo+text) instead of edit_message().
        edit_message() / editMessageText only works for text-only messages.

        Args:
            text: New caption text (string or formattedText)
            chat_id: Override chat_id (default: current chat_id)
            message_id: Override message_id (default: current message_id)
            parse_mode: "markdown", "html", or None for plain text
            reply_markup: Optional keyboard/inline buttons
            show_caption_above_media: Pass True to show caption above media

        Returns:
            Response from API
        """
        target_chat = chat_id if chat_id is not None else self.chat_id
        target_msg = message_id if message_id is not None else self.message_id
        if target_chat is None or target_msg is None:
            raise ValueError("Cannot edit caption: chat_id or message_id not available")

        if isinstance(text, str):
            if parse_mode:
                from grathon.high_level.helpers.formatted_text import TextFormatter
                formatter = TextFormatter(self.client)
                if parse_mode.lower() == "markdown":
                    caption = await formatter.markdown(text)
                elif parse_mode.lower() == "html":
                    caption = await formatter.html(text)
                else:
                    caption = formattedText(text=text)
            else:
                caption = formattedText(text=text)
        else:
            caption = text

        return await self.api.edit_message_caption(  # type: ignore
            chat_id=target_chat,
            message_id=target_msg,
            reply_markup=reply_markup,
            caption=caption,
            show_caption_above_media=show_caption_above_media,
        )

    async def edit_message_reply_markup(
        self,
        reply_markup: Optional[ReplyMarkup] = None,
    ) -> Any:
        """Edit only the inline keyboard of the message that contained the button.

        Use this to swap keyboards (e.g. main menu -> quality list) on an
        existing post without changing the text, caption, or media.

        Args:
            reply_markup: New inline keyboard (or None to remove buttons)

        Returns:
            Response from API
        """
        target_chat = self.chat_id
        target_msg = self.message_id
        if target_chat is None or target_msg is None:
            raise ValueError("Cannot edit reply markup: chat_id or message_id not available")
        return await self.api.edit_message_reply_markup(  # type: ignore
            chat_id=target_chat,
            message_id=target_msg,
            reply_markup=reply_markup,
        )

    async def delete_message(self, revoke: bool = True) -> Any:
        """Delete the message that contained the button

        Args:
            revoke: If True, delete for all users; else just for this user
        """
        return await self.api.delete_messages(  # type: ignore
            chat_id=self.chat_id,
            message_ids=[self.message_id],
            revoke=revoke
        )

    async def send_message(
        self,
        text: str | formattedText | None = None,
        parse_mode: Optional[str] = "markdown",
        file: Optional[str] = None,
        file_type: str = "auto",
        reply_markup: Optional[ReplyMarkup] = None,
    ) -> Any:
        """Send a new message to the same chat

        Args:
            text: Message text or formattedText (used as caption when file given)
            parse_mode: "markdown", "html", or None for plain text (default: markdown)
            file: Path to file (photo/video/audio/document)
            file_type: "auto", "photo", "video", "audio", "document", "voice", "animation", "sticker"
            reply_markup: Optional keyboard/inline buttons

        Returns:
            Response from API

        Examples:
            await ctx.send_message("Hello!")
            await ctx.send_message("**Bold** text", parse_mode="markdown")
            await ctx.send_message("<b>Bold</b> text", parse_mode="html")
            await ctx.send_message(file="./photo.jpg")
        """
        if not self.chat_id:
            raise ValueError("Cannot send message: chat_id not available")

        # Handle file with optional formatting
        if file is not None:
            from grathon.high_level.helpers.files import FileHelper
            caption = ""
            if isinstance(text, str):
                # Apply formatting if parse_mode specified
                if parse_mode:
                    from grathon.high_level.helpers.formatted_text import TextFormatter
                    formatter = TextFormatter(self.client)
                    if parse_mode.lower() == "markdown":
                        caption = await formatter.markdown(text)
                    elif parse_mode.lower() == "html":
                        caption = await formatter.html(text)
                    else:
                        caption = text
                else:
                    caption = text
            elif isinstance(text, formattedText):
                caption = text
            return await FileHelper.send_file(cast('NewMessageCtx', self), file, caption, file_type)

        # Text-only message
        if text is None:
            raise ValueError("Either 'text' or 'file' must be provided")

        # Convert string to formattedText if needed
        if isinstance(text, str):
            # Apply formatting if parse_mode specified
            if parse_mode:
                from grathon.high_level.helpers.formatted_text import TextFormatter
                formatter = TextFormatter(self.client)
                if parse_mode.lower() == "markdown":
                    formatted_text = await formatter.markdown(text)
                elif parse_mode.lower() == "html":
                    formatted_text = await formatter.html(text)
                else:
                    formatted_text = formattedText(text=text)
            else:
                formatted_text = formattedText(text=text)
        else:
            formatted_text = text

        # Create input message content
        input_content = inputMessageText(
            text=formatted_text,
            link_preview_options=None,
            clear_draft=True
        )

        # Create send options
        send_options = messageSendOptions(
            disable_notification=False,
            from_background=False
        )

        # Send the message
        return await send_message_base(  # type: ignore
            ctx=self,
            chat_id=self.chat_id,
            topic_id=None,
            reply_to=None,
            options=send_options,
            reply_markup=reply_markup,
            input_message_content=input_content
        )

    async def send_message_markdown(
        self,
        text: str,
        reply_markup: Optional[ReplyMarkup] = None,
    ) -> Any:
        """Send a message with Markdown formatting (shortcut)

        Args:
            text: Message text with Markdown syntax
            reply_markup: Optional keyboard/inline buttons

        Returns:
            Response from API
        """
        return await self.send_message(text, parse_mode="markdown", reply_markup=reply_markup)

    async def send_message_html(
        self,
        text: str,
        reply_markup: Optional[ReplyMarkup] = None,
    ) -> Any:
        """Send a message with HTML formatting (shortcut)

        Args:
            text: Message text with HTML tags
            reply_markup: Optional keyboard/inline buttons

        Returns:
            Response from API
        """
        return await self.send_message(text, parse_mode="html", reply_markup=reply_markup)

    async def reply(
        self,
        text: str | formattedText | None = None,
        reply_to_message_id: Optional[int] = None,
        disable_web_page_preview: bool = False,
        file: Optional[str] = None,
        file_type: str = "auto",
        parse_mode: Optional[str] = "markdown",
        reply_markup: Optional[ReplyMarkup] = None,
        wait_for_confirmation: bool = True,
        confirmation_timeout: float = 5.0,
    ) -> Any:
        """Send a reply message to the same chat (mirrors NewMessageCtx.reply)

        Args:
            text: Message text or formattedText (used as caption when file given)
            reply_to_message_id: ID of message to reply to
            disable_web_page_preview: Disable link previews
            file: Path to file (photo/video/audio/document)
            file_type: "auto", "photo", "video", "audio", "document", "voice", "animation", "sticker"
            parse_mode: "markdown", "html", or None for plain text
            reply_markup: Inline or reply keyboard
            wait_for_confirmation: Wait for final confirmation (default: True)
            confirmation_timeout: Timeout for confirmation (seconds)

        Returns:
            Final message object (with final message_id)
        """
        if not self.chat_id:
            raise ValueError("Cannot reply: chat_id not available")

        if file is not None:
            from grathon.high_level.helpers.files import FileHelper
            caption = ""
            if isinstance(text, str):
                if parse_mode:
                    from grathon.high_level.helpers.formatted_text import TextFormatter
                    formatter = TextFormatter(self.client)
                    if parse_mode.lower() == "markdown":
                        caption = await formatter.markdown(text)
                    elif parse_mode.lower() == "html":
                        caption = await formatter.html(text)
                    else:
                        caption = text
                else:
                    caption = text
            elif isinstance(text, formattedText):
                caption = text
            print(f"[CB REPLY] calling FileHelper.send_file file={file} type={file_type} chat_id={self.chat_id}")
            return await FileHelper.send_file(cast('NewMessageCtx', self), file, caption, file_type, reply_markup=reply_markup)

        if text is None:
            raise ValueError("Either 'text' or 'file' must be provided")

        return await self.send_message(text=text, parse_mode=parse_mode, reply_markup=reply_markup)

    async def send_file(self, file_path: str, caption: str = "", file_type: str = "auto") -> bool:
        """Send file to the same chat

        Args:
            file_path: Path to file to send
            caption: Optional caption for file
            file_type: Type of file ("auto", "photo", "video", "audio", "document", etc.)

        Returns:
            True if successful, False otherwise

        Examples:
            await ctx.send_file("/tmp/report.pdf", caption="Q1 Report")
            await ctx.send_file("/tmp/image.jpg")
        """
        if not self.chat_id:
            return False

        from grathon.high_level.helpers.files import FileHelper
        return await FileHelper.send_file(cast('NewMessageCtx', self), file_path, caption, file_type)
