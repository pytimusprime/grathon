from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Optional, Any, List, Type, Union
try:
    from typing import TypeIs
except ImportError:
    from typing_extensions import TypeIs

from grathon.core.TLSchema_Manager.tltypes import updateNewMessage, message, MessageContent, messageText, messageAnimation, \
    messageAudio, messagePhoto, messageVideoNote, messageVideo, messageVoiceNote, messageSticker, messageDocument, \
    MessageReplyTo, ReplyMarkup, formattedText, inputMessageText, messageSendOptions, messageReplyToMessage, inputMessageReplyToMessage
from grathon.core.contexts.context import Context
from grathon.core.functions.send_message import send_message_base

if TYPE_CHECKING:
    from grathon.core.tdclient import TdClient

def is_update_new_message(update: Any) -> TypeIs[updateNewMessage]:
    return isinstance(update, updateNewMessage)

def is_message(update: Any) -> TypeIs[message]:
    return isinstance(update, message)

media_types:List[Type[MessageContent]] = [
    messageAnimation,
    messageAudio,
    messagePhoto,
    messageVideo,
    messageVideoNote,
    messageVoiceNote,
]

class NewMessageCtx(Context[updateNewMessage]):
    def __init__(self, client: 'TdClient', update: updateNewMessage):
        super().__init__(client, update)
        self.message: Optional[message] = None
        self.content: Optional[MessageContent] = None
        self.message_text: Optional[messageText] = None
        self._replied_message: Optional[message] = None
        self._replied_message_fetched: bool = False

        if is_update_new_message(update) and getattr(update, "message", None) is not None:
            update_message:Optional[message] = getattr(update, "message",None)
            if is_message(update_message):
                self.message = update_message
                self.content = update_message.content  # pyright: ignore [reportOptionalMemberAccess]
                if self.content and isinstance(self.content, messageText):
                    self.message_text = self.content

    @property
    def is_video(self) -> Union[bool ,messageVideo]:
        if isinstance(self.content, messageVideo):
            return self.content
        return False

    @property
    def is_voice(self) -> Union[bool ,messageVoiceNote]:
        if isinstance(self.content, messageVoiceNote):
            return self.content
        return False

    @property
    def is_animation(self) -> Union[bool ,messageAnimation]:
        if isinstance(self.content, messageAnimation):
            return self.content
        return False

    @property
    def is_photo(self) -> Union[bool ,messagePhoto]:
        if isinstance(self.content, messagePhoto):
            return self.content
        return False

    @property
    def is_document(self) -> Union[bool ,messageDocument]:
        if isinstance(self.content, messageDocument):
            return self.content
        return False

    @property
    def is_audio(self) -> Union[bool ,messageAudio]:
        if isinstance(self.content, messageAudio):
            return self.content
        return False

    @property
    def is_sticker(self) -> Union[bool ,messageSticker]:
        if isinstance(self.content, messageSticker):
            return self.content
        return False

    @property
    def reply_to(self):
        if self.message and isinstance(self.message.reply_to,MessageReplyTo):
            return self.message.reply_to
        return None

    async def get_replied_message(self) -> Optional[message]:
        """
        Fetch the message that this message is replying to

        Returns:
            The replied message object, or None if this message doesn't reply to anything or fetch failed

        Examples:
            replied = await ctx.get_replied_message()
            if replied and replied.content:
                await ctx.reply(f"You replied to a message about: {type(replied.content).__name__}")
        """
        if not self.reply_to:
            return None

        if self._replied_message_fetched:
            return self._replied_message

        try:
            reply_info = self.reply_to
            # Check if it's a message reply (not story reply)
            if isinstance(reply_info, messageReplyToMessage) and reply_info.chat_id and reply_info.message_id:
                # For regular message replies
                replied_msg = await self.client.api.get_message(
                    chat_id=reply_info.chat_id,
                    message_id=reply_info.message_id
                )
                if replied_msg and isinstance(replied_msg, message):
                    self._replied_message = replied_msg
                    self._replied_message_fetched = True
                    return replied_msg
        except Exception:
            pass

        self._replied_message_fetched = True
        return None

    @property
    def replied(self) -> 'RepliedMessageAccessor':
        """
        Access replied message properties easily

        Returns:
            RepliedMessageAccessor for accessing file and content info from replied message

        Examples:
            file_id = ctx.replied.file_id  # Get file ID from replied message
            has_file = ctx.replied.has_file  # Check if replied message has a file
            await ctx.replied.download("/tmp/file.pdf")  # Download replied message file
        """
        return RepliedMessageAccessor(self)

    @property
    def is_outgoing(self) -> bool:
        """Check if the current user is the sender of this message"""
        if self.message:
            return bool(getattr(self.message, "is_outgoing", False))
        return False

    @property
    def is_incoming(self) -> bool:
        """Check if the message was received from another user"""
        return not self.is_outgoing

    @property
    def chat_id(self):
        if self.message:
            return self.message.chat_id
        return None

    @property
    def sender_id(self):
        if self.message:
            return self.message.sender_id
        return None

    @property
    def user_id(self) -> Optional[int]:
        """Get the sender's user ID as an int

        Unified accessor — use this instead of sender_id.user_id directly.

        Examples:
            uid = ctx.user_id  # works in any message handler
        """
        if self.message and self.message.sender_id:
            return getattr(self.message.sender_id, "user_id", None)
        return None

    @property
    def message_id(self) -> Optional[int]:
        """Get the current message ID

        Unified accessor — use this instead of self.message.id directly.

        Examples:
            msg_id = ctx.message_id  # works in any message handler
        """
        if self.message:
            return self.message.id
        return None

    @property
    def text(self) -> Optional[str]:
        """Get message text content

        For text messages: returns the message text.
        For media messages (photo, video, etc.): returns the caption text.
        This makes ctx.text work uniformly for all message types.

        Examples:
            @bot.on_message()
            async def handler(ctx):
                if ctx.text:
                    await ctx.reply(f"You said: {ctx.text}")
        """
        # Plain text message
        if self.message_text and self.message_text.text:
            return self.message_text.text.text

        # Media message with caption
        if self.content and hasattr(self.content, "caption") and self.content.caption:
            caption = self.content.caption
            if hasattr(caption, "text"):
                return caption.text

        return None

    @property
    def plain_text(self) -> Optional[str]:
        """Get text only from text messages, ignore media captions

        Unlike ctx.text which returns captions for media messages,
        ctx.plain_text returns None for media messages — only real text messages.

        Examples:
            @bot.on_message()
            async def handler(ctx):
                # Only handle pure text messages, ignore photos/videos with captions
                if ctx.plain_text:
                    await ctx.reply(f"You typed: {ctx.plain_text}")
        """
        if self.message_text and self.message_text.text:
            return self.message_text.text.text
        return None

    @property
    def file_id(self) -> Optional[int]:
        """Get file ID from message content (if any)

        Returns:
            File ID for photo (largest size), video, audio, document, sticker,
            animation, voice note, or video note. None if message has no file.
        """
        if not self.content:
            return None

        if isinstance(self.content, messagePhoto):
            if self.content.photo and self.content.photo.sizes:
                sizes = self.content.photo.sizes
                return sizes[-1].photo.id if sizes else None
        elif isinstance(self.content, messageVideo):
            if self.content.video and self.content.video.video:
                return self.content.video.video.id
        elif isinstance(self.content, messageAudio):
            if self.content.audio and self.content.audio.audio:
                return self.content.audio.audio.id
        elif isinstance(self.content, messageDocument):
            if self.content.document and self.content.document.document:
                return self.content.document.document.id
        elif isinstance(self.content, messageSticker):
            if self.content.sticker and self.content.sticker.sticker:
                return self.content.sticker.sticker.id
        elif isinstance(self.content, messageAnimation):
            if self.content.animation and self.content.animation.animation:
                return self.content.animation.animation.id
        elif isinstance(self.content, messageVoiceNote):
            if self.content.voice_note and self.content.voice_note.voice:
                return self.content.voice_note.voice.id
        elif isinstance(self.content, messageVideoNote):
            if self.content.video_note and self.content.video_note.video:
                return self.content.video_note.video.id

        return None

    @property
    def remote_file_id(self) -> Optional[str]:
        """Get persistent Telegram file_id string from message content

        Use this for storing in database and re-sending later via FileHelper.send_by_file_id().
        Unlike file_id (internal TDLib int), this is the persistent string ID.

        Returns:
            Remote file_id string, or None if message has no file.

        Examples:
            fid = ctx.remote_file_id  # "AgACAgIAAxk..."
            if fid:
                db.save_file(fid)
        """
        if not self.content:
            return None

        file_obj = None
        if isinstance(self.content, messagePhoto):
            if self.content.photo and self.content.photo.sizes:
                sizes = self.content.photo.sizes
                file_obj = sizes[-1].photo if sizes else None
        elif isinstance(self.content, messageVideo):
            if self.content.video and self.content.video.video:
                file_obj = self.content.video.video
        elif isinstance(self.content, messageAudio):
            if self.content.audio and self.content.audio.audio:
                file_obj = self.content.audio.audio
        elif isinstance(self.content, messageDocument):
            if self.content.document and self.content.document.document:
                file_obj = self.content.document.document
        elif isinstance(self.content, messageSticker):
            if self.content.sticker and self.content.sticker.sticker:
                file_obj = self.content.sticker.sticker
        elif isinstance(self.content, messageAnimation):
            if self.content.animation and self.content.animation.animation:
                file_obj = self.content.animation.animation
        elif isinstance(self.content, messageVoiceNote):
            if self.content.voice_note and self.content.voice_note.voice:
                file_obj = self.content.voice_note.voice
        elif isinstance(self.content, messageVideoNote):
            if self.content.video_note and self.content.video_note.video:
                file_obj = self.content.video_note.video

        if file_obj and hasattr(file_obj, "remote") and file_obj.remote:
            remote = file_obj.remote
            if hasattr(remote, "id"):
                return remote.id
        return None

    @property
    def file_size(self) -> Optional[int]:
        """Get file size in bytes from message content

        Returns:
            File size in bytes, or None if message has no file.

        Examples:
            size = ctx.file_size
            if size and size > 100 * 1024 * 1024:
                await ctx.reply("File is larger than 100MB")
        """
        if not self.content:
            return None

        file_obj = None
        if isinstance(self.content, messagePhoto):
            if self.content.photo and self.content.photo.sizes:
                sizes = self.content.photo.sizes
                file_obj = sizes[-1].photo if sizes else None
        elif isinstance(self.content, messageVideo):
            if self.content.video and self.content.video.video:
                file_obj = self.content.video.video
        elif isinstance(self.content, messageAudio):
            if self.content.audio and self.content.audio.audio:
                file_obj = self.content.audio.audio
        elif isinstance(self.content, messageDocument):
            if self.content.document and self.content.document.document:
                file_obj = self.content.document.document
        elif isinstance(self.content, messageSticker):
            if self.content.sticker and self.content.sticker.sticker:
                file_obj = self.content.sticker.sticker
        elif isinstance(self.content, messageAnimation):
            if self.content.animation and self.content.animation.animation:
                file_obj = self.content.animation.animation
        elif isinstance(self.content, messageVoiceNote):
            if self.content.voice_note and self.content.voice_note.voice:
                file_obj = self.content.voice_note.voice
        elif isinstance(self.content, messageVideoNote):
            if self.content.video_note and self.content.video_note.video:
                file_obj = self.content.video_note.video

        if file_obj and hasattr(file_obj, "size"):
            return file_obj.size
        return None

    @property
    def session(self) -> dict[str, Any]:
        """Get session data for this chat

        Returns an empty dict if no session store is available.
        Useful for tracking user state across messages without modifying the bot.

        Usage:
            @bot.on_command("start")
            async def start(ctx):
                ctx.session["step"] = 1
                await ctx.reply("Step 1")

            @bot.on_message()
            async def handler(ctx):
                step = ctx.session.get("step", 0)
                if step == 1:
                    ctx.session["step"] = 2
        """
        if self.client.session is not None and self.chat_id is not None:
            return self.client.session.get(self.chat_id)
        return {}


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
    ) -> message:
        """
        Send a reply message to the user (Telethon-style)

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

        Examples:
            await ctx.reply("Hello!")
            await ctx.reply("**Bold** text", parse_mode="markdown")
            await ctx.reply("<b>Bold</b> text", parse_mode="html")
            await ctx.reply(file="./photo.jpg")
            msg = await ctx.reply("Msg", wait_for_confirmation=True)
            # msg.id is the FINAL message ID
        """
        if not self.chat_id:
            raise ValueError("Cannot reply: chat_id not available")

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
            return await FileHelper.send_file(self, file, caption, file_type, reply_markup=reply_markup)  # pyright: ignore [reportReturnType]

        # Text-only reply
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

        # Get message ID to reply to
        if reply_to_message_id is None and self.message:
            reply_to_message_id = self.message.id

        # Create send options
        send_options = messageSendOptions(
            disable_notification=False,
            from_background=False
        )

        reply_to = None
        if reply_to_message_id is not None:
            reply_to = inputMessageReplyToMessage(message_id=reply_to_message_id)

        # Send the message
        pending_message = await send_message_base(
            ctx=self,
            chat_id=self.chat_id,
            topic_id=None,  # null = no topic (TDLib expects MessageTopic or null)
            reply_to=reply_to,
            options=send_options,
            reply_markup=reply_markup,
            input_message_content=input_content,
            wait_for_confirmation=wait_for_confirmation,
            confirmation_timeout=confirmation_timeout,
        )

        return pending_message  # pyright: ignore [reportReturnType]

    async def reply_markdown(self, text: str) -> Any:
        """
        Reply with Markdown formatting

        Args:
            text: Message text with Markdown syntax

        Returns:
            Response from API

        Examples:
        """
        from grathon.high_level.helpers.formatted_text import TextFormatter
        formatter = TextFormatter(self.client)
        formatted = await formatter.markdown(text)
        return await self.reply(formatted)

    async def reply_html(self, text: str) -> Any:
        """
        Reply with HTML formatting

        Args:
            text: Message text with HTML tags

        Returns:
            Response from API

        Examples:
        """
        from grathon.high_level.helpers.formatted_text import TextFormatter
        formatter = TextFormatter(self.client)
        formatted = await formatter.html(text)
        return await self.reply(formatted)

    @property
    def command(self) -> Optional[str]:
        """
        Extract command name from message text

        Returns:
            Command name without slash (e.g. "start" for "/start")
            or None if message is not a command

        Examples:
            ctx.text = "/start arg1"
            ctx.command
            "start"

            ctx.text = "/start@mybot"
            ctx.command
            "start"
        """
        if not self.text or not self.text.startswith("/"):
            return None
        # Handle "/start@botname arg1" → "start"
        cmd_part = self.text.split()[0][1:]  # strip "/" and take first word
        return cmd_part.split("@")[0]        # strip @botname suffix

    @property
    def args(self) -> list[str]:
        """
        Get command arguments as a list

        Returns:
            List of arguments after the command, or empty list

        Examples:
            >>> ctx.text = "/start arg1 arg2"
            >>> ctx.args
            ["arg1", "arg2"]
            >>> ctx.text = "/start"
            >>> ctx.args
            []
        """
        if not self.text or not self.text.startswith("/"):
            return []
        parts = self.text.split()
        return parts[1:]  # skip first part (/command)

    async def edit(self, text: str | formattedText, message_id: int | None = None) -> Any:
        """
        Edit a message (default: the replied message if replying, else current message)

        Args:
            text: New message text (string or formattedText)
            message_id: Optional message ID to edit (default: replied message or current)

        Returns:
            Response from API

        Examples:
            await ctx.edit("Updated message")  # Edits replied message
            await ctx.edit("Updated", message_id=123456)  # Edits specific message
        """
        if not self.chat_id:
            raise ValueError("Cannot edit: chat_id not available")

        # Determine which message to edit
        target_message_id = message_id

        if target_message_id is None:
            # Prefer replied message if available
            if self.reply_to and isinstance(self.reply_to, messageReplyToMessage):
                target_message_id = self.reply_to.message_id
            # Otherwise use current message
            elif self.message:
                target_message_id = self.message.id

        if target_message_id is None:
            raise ValueError("Cannot edit: no message ID found")

        # Convert string to formattedText if needed
        if isinstance(text, str):
            formatted_text = formattedText(text=text)
        else:
            formatted_text = text

        # Use helper function
        from grathon.core.functions.edit_message import edit_message_text  # pyright: ignore [reportMissingImports]
        return await edit_message_text(
            ctx=self,
            chat_id=self.chat_id,
            message_id=target_message_id,
            text=formatted_text,
            reply_markup=None
        )

    async def edit_markdown(self, text: str) -> Any:
        """
        Edit message with Markdown formatting

        Args:
            text: Message text with Markdown syntax

        Returns:
            Response from API

        Examples:
        """
        from grathon.high_level.helpers.formatted_text import TextFormatter
        formatter = TextFormatter(self.client)
        formatted = await formatter.markdown(text)
        return await self.edit(formatted)

    async def edit_html(self, text: str) -> Any:
        """
        Edit message with HTML formatting

        Args:
            text: Message text with HTML tags

        Returns:
            Response from API

        Examples:
        """
        from grathon.high_level.helpers.formatted_text import TextFormatter
        formatter = TextFormatter(self.client)
        formatted = await formatter.html(text)
        return await self.edit(formatted)

    async def delete(self, message_id: int | None = None, revoke: bool = True) -> Any:
        """
        Delete a message (default: the replied message if replying, else current message)

        Args:
            message_id: Optional message ID to delete (default: replied or current)
            revoke: Delete for all users (default True)

        Returns:
            Response from API

        Examples:
            await ctx.delete()  # Deletes replied message
            await ctx.delete(message_id=123456)  # Delete specific message
        """
        if not self.chat_id:
            raise ValueError("Cannot delete: chat_id not available")

        # Determine which message to delete
        target_message_id = message_id

        if target_message_id is None:
            # Prefer replied message if available
            if self.reply_to and isinstance(self.reply_to, messageReplyToMessage):
                target_message_id = self.reply_to.message_id
            # Otherwise use current message
            elif self.message:
                target_message_id = self.message.id

        if target_message_id is None:
            raise ValueError("Cannot delete: no message ID found")

        # Use helper function
        from grathon.core.functions.delete_message import delete_messages  # pyright: ignore [reportMissingImports]
        return await delete_messages(
            ctx=self,
            chat_id=self.chat_id,
            message_ids=[target_message_id],
            revoke=revoke
        )

    async def download(self, output_path: str = "") -> Optional[str]:
        """
        Download the file from this message

        Args:
            output_path: Optional path to save file. If empty, returns TDLib cache path.

        Returns:
            Path to downloaded file, or None if message has no file

        Examples:
            path = await ctx.download()  # returns cache path

            path = await ctx.download("/tmp/myfile.pdf")  # saves to path
        """
        fid = self.file_id
        if fid is None:
            return None

        from grathon.high_level.helpers.files import FileHelper
        return await FileHelper.download_file(self, fid, output_path)

    async def forward(
        self,
        to_chat_id: int,
        send_copy: bool = False,
        wait_for_confirmation: bool = True,
        confirmation_timeout: float = 5.0,
    ) -> Any:
        """
        Forward this message to another chat

        Args:
            to_chat_id: ID of destination chat
            send_copy: If True, sends a copy (hides "forwarded from"). Default False.
            wait_for_confirmation: Wait for final confirmation (default: True)
            confirmation_timeout: Timeout for confirmation (seconds)

        Returns:
            Messages object with final message IDs

        Examples:
            await ctx.forward(12345)  # forward to chat 12345

            await ctx.forward(12345, send_copy=True)  # send as copy

            # Do not wait for confirmation
            await ctx.forward(12345, wait_for_confirmation=False)
        """
        if not self.chat_id or not self.message:
            raise ValueError("Cannot forward: chat_id or message not available")

        # Use helper function
        from grathon.core.functions.forward_message import forward_messages  # pyright: ignore [reportMissingImports]
        return await forward_messages(
            ctx=self,
            chat_id=to_chat_id,
            from_chat_id=self.chat_id,
            message_ids=[self.message.id],
            send_copy=send_copy,
            remove_caption=False,
            wait_for_confirmation=wait_for_confirmation,
            confirmation_timeout=confirmation_timeout,
        )

    async def send_file(self, file_path: str, caption: str = "", file_type: str = "auto") -> bool:
        if not self.chat_id:
            return False

        try:
            import os
            from grathon.high_level.helpers.files import FileHelper

            abs_path = os.path.abspath(file_path)
            if not os.path.exists(abs_path):
                return False

            return await FileHelper.send_file(self, abs_path, caption, file_type)

        except Exception:
            return False

    async def reply_file(self, file_path: str, caption: str = "", file_type: str = "auto") -> bool:
        """
        Send file as a reply to this message

        Args:
            file_path: Path to file to send
            caption: Optional caption for file
            file_type: Type of file ("auto", "photo", "video", "audio", "document", etc.)

        Returns:
            True if successful, False otherwise

        Examples:
            await ctx.reply_file("/tmp/report.pdf", caption="Q1 Report")
        """
        # For now, just send file to same chat (TDLib reply threading handled separately)
        return await self.send_file(file_path, caption, file_type)


class RepliedMessageAccessor:
    """
    Helper class to access file and content information from replied messages

    Provides convenient access to file_id, file type checks, and download methods
    for the message that this message is replying to.

    Examples:
        if ctx.replied.has_file:
            path = await ctx.replied.download("/tmp/attachment.pdf")
        if ctx.replied.is_photo:
            await ctx.reply("You replied to a photo!")
    """

    def __init__(self, ctx: NewMessageCtx):
        self.ctx = ctx

    @property
    def message(self) -> Optional[message]:
        """Get the replied message object (may be None if not fetched yet)"""
        if self.ctx._replied_message_fetched:
            return self.ctx._replied_message
        return None

    @property
    def text(self) -> Optional[str]:
        """Get text content from replied message

        Works for both plain text messages and media messages with captions.

        Examples:
            replied_text = ctx.replied.text
        """
        msg = self.message
        if msg is None or msg.content is None:
            return None

        # Plain text message
        if hasattr(msg.content, "text") and msg.content.text:
            text_obj = msg.content.text
            if hasattr(text_obj, "text"):
                return text_obj.text
            if isinstance(text_obj, str):
                return text_obj

        # Media message with caption
        if hasattr(msg.content, "caption") and msg.content.caption:
            caption = msg.content.caption
            if hasattr(caption, "text"):
                return caption.text
            if isinstance(caption, str):
                return caption

        return None

    @property
    def sender_id(self):
        """Get the sender_id of the replied message

        Returns the MessageSender union object (messageSenderUser or messageSenderChat).

        Examples:
            sender = ctx.replied.sender_id
            if hasattr(sender, "user_id"):
                user_id = sender.user_id
        """
        msg = self.message
        if msg is None:
            return None
        return getattr(msg, "sender_id", None)

    @property
    def user_id(self) -> Optional[int]:
        """Get the sender's user ID from the replied message

        Convenience accessor that extracts the int user_id from sender_id.

        Examples:
            uid = ctx.replied.user_id
        """
        sender = self.sender_id
        if sender is None:
            return None
        return getattr(sender, "user_id", None)

    @property
    def has_file(self) -> bool:
        """Check if replied message has a file/media without fetching it"""
        if not self.ctx.reply_to:
            return False
        return True

    @property
    def file_id(self) -> Optional[int]:
        """
        Get file ID from replied message (requires async fetch)

        Use: fid = await ctx.replied.get_file_id() instead for async operation

        Returns:
            File ID from cached replied message if already fetched, None otherwise
        """
        if self.ctx._replied_message:
            return self._extract_file_id(self.ctx._replied_message)
        return None

    async def get_file_id(self) -> Optional[int]:
        """
        Async method to get file ID from replied message

        Returns:
            File ID from replied message, or None if message has no file

        Examples:
            fid = await ctx.replied.get_file_id()
            if fid:
                path = await ctx.replied.download("/tmp/file.pdf")
        """
        replied = await self.ctx.get_replied_message()
        if replied:
            return self._extract_file_id(replied)
        return None

    def _extract_file_id(self, msg: message) -> Optional[int]:
        """Extract file ID from message content"""
        content = msg.content
        if not content:
            return None

        if isinstance(content, messagePhoto):
            if content.photo and content.photo.sizes:
                sizes = content.photo.sizes
                return sizes[-1].photo.id if sizes else None
        elif isinstance(content, messageVideo):
            if content.video and content.video.video:
                return content.video.video.id
        elif isinstance(content, messageAudio):
            if content.audio and content.audio.audio:
                return content.audio.audio.id
        elif isinstance(content, messageDocument):
            if content.document and content.document.document:
                return content.document.document.id
        elif isinstance(content, messageSticker):
            if content.sticker and content.sticker.sticker:
                return content.sticker.sticker.id
        elif isinstance(content, messageAnimation):
            if content.animation and content.animation.animation:
                return content.animation.animation.id
        elif isinstance(content, messageVoiceNote):
            if content.voice_note and content.voice_note.voice:
                return content.voice_note.voice.id
        elif isinstance(content, messageVideoNote):
            if content.video_note and content.video_note.video:
                return content.video_note.video.id

        return None

    @property
    def is_video(self) -> Union[bool, messageVideo]:
        """Check if replied message is a video (cached check)"""
        if self.ctx._replied_message:
            if isinstance(self.ctx._replied_message.content, messageVideo):
                return self.ctx._replied_message.content
        return False

    @property
    def is_photo(self) -> Union[bool, messagePhoto]:
        """Check if replied message is a photo (cached check)"""
        if self.ctx._replied_message:
            if isinstance(self.ctx._replied_message.content, messagePhoto):
                return self.ctx._replied_message.content
        return False

    @property
    def is_document(self) -> Union[bool, messageDocument]:
        """Check if replied message is a document (cached check)"""
        if self.ctx._replied_message:
            if isinstance(self.ctx._replied_message.content, messageDocument):
                return self.ctx._replied_message.content
        return False

    @property
    def is_audio(self) -> Union[bool, messageAudio]:
        """Check if replied message is an audio file (cached check)"""
        if self.ctx._replied_message:
            if isinstance(self.ctx._replied_message.content, messageAudio):
                return self.ctx._replied_message.content
        return False

    @property
    def is_voice(self) -> Union[bool, messageVoiceNote]:
        """Check if replied message is a voice note (cached check)"""
        if self.ctx._replied_message:
            if isinstance(self.ctx._replied_message.content, messageVoiceNote):
                return self.ctx._replied_message.content
        return False

    @property
    def is_animation(self) -> Union[bool, messageAnimation]:
        """Check if replied message is an animation (cached check)"""
        if self.ctx._replied_message:
            if isinstance(self.ctx._replied_message.content, messageAnimation):
                return self.ctx._replied_message.content
        return False

    @property
    def is_sticker(self) -> Union[bool, messageSticker]:
        """Check if replied message is a sticker (cached check)"""
        if self.ctx._replied_message:
            if isinstance(self.ctx._replied_message.content, messageSticker):
                return self.ctx._replied_message.content
        return False

    async def download(self, output_path: str = "") -> Optional[str]:
        """
        Download file from replied message

        Args:
            output_path: Optional path to save file. If empty, returns TDLib cache path.

        Returns:
            Path to downloaded file, or None if replied message has no file or download failed

        Examples:
            path = await ctx.replied.download()  # returns cache path
            path = await ctx.replied.download("/tmp/myfile.pdf")  # saves to specific path
            if path:
                await ctx.reply(f"Downloaded: {path}")
        """
        fid = await self.get_file_id()
        if fid is None:
            return None

        from grathon.high_level.helpers.files import FileHelper
        return await FileHelper.download_file(self.ctx, fid, output_path)

