"""Multi-step interactive conversation flows with state management"""

from __future__ import annotations
import asyncio
from typing import Dict, Optional, Tuple, TYPE_CHECKING, Union

from grathon.core.contexts.NewMessageCtx import NewMessageCtx
from grathon.core.contexts.CallbackQueryCtx import CallbackQueryCtx

if TYPE_CHECKING:
    from grathon.core.contexts.context import Context


class ConversationTimeout(Exception):
    """Raised when user doesn't respond within the conversation timeout"""
    pass


_CANCELLED = object()


class ConversationStore:
    """Global registry of handlers waiting for user input

    Maintains two separate dicts to avoid cross-resolving:
    - Message futures: for wait_message()
    - Callback futures: for wait_callback()
    """

    _message_futures: Dict[Tuple[int, int], asyncio.Future] = {}
    _callback_futures: Dict[Tuple[int, int], asyncio.Future] = {}

    @classmethod
    def register_message(cls, chat_id: int, user_id: int, future: asyncio.Future) -> None:
        """Register a Future waiting for the next message from (chat_id, user_id)

        The message can be of any content type (text, photo, document, video, etc.).
        """
        key = (chat_id, user_id)
        cls._message_futures[key] = future

    @classmethod
    def register_callback(cls, chat_id: int, user_id: int, future: asyncio.Future) -> None:
        """Register a Future waiting for the next button click from (chat_id, user_id)"""
        key = (chat_id, user_id)
        cls._callback_futures[key] = future

    @classmethod
    def resolve_message(cls, chat_id: int, user_id: int, ctx) -> bool:
        """Resolve waiting message Future if one exists

        Args:
            chat_id: Chat ID
            user_id: User ID
            ctx: NewMessageCtx with the reply

        Returns:
            True if a Future was found and resolved, False otherwise
        """
        key = (chat_id, user_id)
        if key in cls._message_futures:
            future = cls._message_futures.pop(key)
            if not future.done():
                future.set_result(ctx)
            return True
        return False

    @classmethod
    def resolve_callback(cls, chat_id: int, user_id: int, ctx) -> bool:
        """Resolve waiting callback Future if one exists

        Args:
            chat_id: Chat ID
            user_id: User ID
            ctx: CallbackQueryCtx with the button data

        Returns:
            True if a Future was found and resolved, False otherwise
        """
        key = (chat_id, user_id)
        if key in cls._callback_futures:
            future = cls._callback_futures.pop(key)
            if not future.done():
                future.set_result(ctx)
            return True
        return False

    @classmethod
    def cancel_message(cls, chat_id: int, user_id: int) -> bool:
        """Cancel a waiting message future for a user (e.g. when navigating away)

        Returns:
            True if a pending future was found and cancelled, False otherwise
        """
        key = (chat_id, user_id)
        future = cls._message_futures.pop(key, None)
        if future is not None and not future.done():
            future.set_result(_CANCELLED)
            return True
        return False

    @classmethod
    def clear(cls, chat_id: int, user_id: int) -> None:
        """Clear both message and callback futures for a user

        Used on conversation exit or timeout to clean up state.
        """
        key = (chat_id, user_id)
        cls._message_futures.pop(key, None)
        cls._callback_futures.pop(key, None)


async def conversation_middleware(ctx: Context, next_fn) -> None:
    """Middleware that intercepts messages for active conversations

    Must be installed via: client.use(conversation_middleware)

    When a user is in an active conversation waiting for input:
    - The Future is resolved with the incoming message/callback
    - This function returns WITHOUT calling next_fn
    - Normal handlers are skipped for that update

    When no conversation is waiting:
    - This function calls next_fn
    - Normal handlers process the update
    """
    if isinstance(ctx, NewMessageCtx):
        user_id = _get_message_user_id(ctx)
        chat_id = ctx.chat_id
        # DEBUG: Log what we found
        print(f"🔍 DEBUG: NewMessageCtx - chat_id={chat_id}, sender_id={getattr(ctx, 'sender_id', 'NOT_FOUND')}, user_id={user_id}, text={getattr(ctx, 'text', 'NO_TEXT')}", flush=True)
        print(f"🔍 DEBUG: Active futures - msg_keys={list(ConversationStore._message_futures.keys())}, cb_keys={list(ConversationStore._callback_futures.keys())}", flush=True)

        if user_id and ConversationStore.resolve_message(chat_id, user_id, ctx):  # pyright: ignore [reportArgumentType]
            print(f"✅ DEBUG: Message intercepted for user {user_id} in chat {chat_id}", flush=True)
            return  # Intercepted — don't call next()
        else:
            print(f"⏭️ DEBUG: No active conversation for chat={chat_id}, user={user_id}, passing to next", flush=True)

    elif isinstance(ctx, CallbackQueryCtx):
        if ConversationStore.resolve_callback(ctx.chat_id, ctx.sender_user_id, ctx):  # pyright: ignore [reportArgumentType]
            print(f"✅ DEBUG: Callback intercepted", flush=True)
            return  # Intercepted — don't call next()

    # Not in a conversation — process normally
    await next_fn(ctx)


class Conversation:
    """Context manager for multi-step interactive flows

    Allows a handler to ask questions and wait for user replies across
    multiple messages, while maintaining conversation state.

    Example:
        @router.on(updateNewMessage, filters=[F.command("register")])
        async def register(ctx: NewMessageCtx):
            async with Conversation(ctx, timeout=60) as conv:
                await conv.ask("What is your name?")
                name = await conv.wait_message()

                await conv.ask(f"Nice to meet you, {name}! Your email?")
                email = await conv.wait_message()

                await ctx.reply(f"✅ Registered: {name} ({email})")

    wait_message() resolves the next message of ANY content type.
    By default it returns plain ``str`` (text/caption, ``""`` for media without caption).
    Pass ``only_text=False`` to get the full :class:`NewMessageCtx` with all attributes:

        @router.on(updateNewMessage, filters=[F.command("store")])
        async def store(ctx: NewMessageCtx):
            async with Conversation(ctx, timeout=120) as conv:
                await conv.ask("Send me the file:")
                reply = await conv.wait_message(only_text=False)
                if reply is None:
                    await ctx.reply("Cancelled.")
                    return
                if reply.is_document:
                    await ctx.reply(f"Got file: {reply.file_id}")
                else:
                    await ctx.reply(f"Got text: {reply.text}")

    wait_callback() resolves the next button click. By default it returns the
    decoded callback data ``str``. Pass ``only_data=False`` to get the full
    :class:`CallbackQueryCtx` (with ``message_id``, ``chat_instance``, ...):

        @router.on(updateNewCallbackQuery, filters=[F.callback(r"^choose_(.+)$")])
        async def choose(ctx):
            async with Conversation(ctx, timeout=60) as conv:
                await conv.ask_buttons("Choose:", keyboard)
                data = await conv.wait_callback()        # -> "btn_1"
                cb = await conv.wait_callback(only_data=False)  # -> CallbackQueryCtx
                await ctx.edit_message_text(f"Clicked: {data} on msg {cb.message_id}")
    """

    def __init__(self, ctx: Context, timeout: float = 300.0):
        """Initialize conversation

        Args:
            ctx: The context (NewMessageCtx or CallbackQueryCtx) that initiated the conversation
            timeout: Seconds to wait for each user response (default: 5 minutes)
        """
        self._ctx = ctx
        self._timeout = timeout
        self._chat_id = ctx.chat_id  # pyright: ignore [reportAttributeAccessIssue]
        self._user_id = _get_user_id(ctx)
        self._pending_message_future: Optional[asyncio.Future] = None
        self._pending_callback_future: Optional[asyncio.Future] = None
        self._prompt_message_id: Optional[int] = None

    async def __aenter__(self) -> Conversation:
        """Enter the conversation context"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the conversation context and cleanup state"""
        ConversationStore.clear(self._chat_id, self._user_id)  # pyright: ignore [reportArgumentType]
        return False  # Don't suppress exceptions

    async def ask_buttons(self, text: str, reply_markup, **kwargs) -> None:
        """Send a question with buttons and pre-register callback future

        Like ask() but for button-based interactions.

        Args:
            text: The question text
            reply_markup: The keyboard markup with buttons
            **kwargs: Additional arguments passed to ctx.reply()
        """
        # Step 1: Pre-register callback future BEFORE sending the message
        loop = asyncio.get_running_loop()
        self._pending_callback_future = loop.create_future()
        ConversationStore.register_callback(
            self._chat_id, self._user_id, self._pending_callback_future  # pyright: ignore [reportArgumentType]
        )

        # Step 2: Send the message with buttons (use reply() with reply_markup parameter)
        sent = await self._ctx.reply(text, reply_markup=reply_markup, **kwargs)
        self._prompt_message_id = getattr(sent, "id", None)

    async def ask(self, text: str, **kwargs) -> None:
        """Send a question to the user and pre-register the future to receive the answer

        IMPORTANT: This pre-registers a future for the next incoming message BEFORE
        sending the question. This prevents a race condition where middleware might
        process the next message before wait_message() can register its future.

        Args:
            text: The question text
            **kwargs: Additional arguments passed to ctx.reply() (e.g., reply_markup)
        """
        # Step 1: Pre-register future BEFORE sending the message
        # This ensures middleware can intercept the response immediately
        loop = asyncio.get_running_loop()
        self._pending_message_future = loop.create_future()
        ConversationStore.register_message(
            self._chat_id, self._user_id, self._pending_message_future  # pyright: ignore [reportArgumentType]
        )

        # Step 2: Now send the question (safe to yield control here)
        sent = await self._ctx.reply(text, **kwargs)  # pyright: ignore [reportAttributeAccessIssue]
        self._prompt_message_id = getattr(sent, "id", None)

    @property
    def prompt_message_id(self) -> Optional[int]:
        """ID of the message sent by the last ask()/ask_buttons() call, if available.

        Useful when you need to reference the bot's prompt message, e.g. for
        edit_message_text() or delete_message() after the user responds.
        """
        return self._prompt_message_id

    async def wait_message(self, only_text: bool = True) -> Union[str, NewMessageCtx, None]:
        """Wait for the user's next message (any content type: text, photo, file...)

        If ask() was called before this, reuses the pre-registered future.
        Otherwise, creates and registers a new future (fallback for direct wait_message calls).

        Args:
            only_text: If True (default), return plain ``str`` (text or caption, ``""`` for
                media without caption) for backward compatibility.
                If False, return the full :class:`NewMessageCtx` object giving access
                to all message attributes (``text``, ``file_id``, ``is_document``,
                ``content``, ``remote_file_id``, etc.).

        Returns:
            If ``only_text=True``: ``str`` (or ``None`` on cancel).
            If ``only_text=False``: :class:`NewMessageCtx` (or ``None`` on cancel).

        Raises:
            ConversationTimeout: if user doesn't respond within the timeout period
        """
        # Use pre-registered future from ask() if available, otherwise create new one
        if self._pending_message_future is not None:
            future = self._pending_message_future
            self._pending_message_future = None
            print(f"⏳ DEBUG: Using pre-registered future for chat={self._chat_id}, user={self._user_id}", flush=True)
        else:
            # Fallback: create and register new future (for direct wait_message without ask)
            loop = asyncio.get_running_loop()
            future = loop.create_future()
            print(f"⏳ DEBUG: Registering new future for chat={self._chat_id}, user={self._user_id}", flush=True)
            ConversationStore.register_message(self._chat_id, self._user_id, future)  # pyright: ignore [reportArgumentType]

        print(f"⏳ DEBUG: Waiting for message (timeout={self._timeout}s)...", flush=True)

        try:
            msg_ctx = await asyncio.wait_for(future, timeout=self._timeout)
            if msg_ctx is _CANCELLED:
                print(f"⏹️ DEBUG: Conversation cancelled for chat={self._chat_id}, user={self._user_id}", flush=True)
                return None
            content_name = (
                type(msg_ctx.content).__name__ if getattr(msg_ctx, "content", None) else "text"
            )
            text_repr = getattr(msg_ctx, "text", None)
            print(f"✅ DEBUG: Message received: {text_repr!r} (content={content_name})", flush=True)
            if only_text:
                return msg_ctx.text or ""
            return msg_ctx  # pyright: ignore [reportReturnType]
        except asyncio.TimeoutError:
            print(f"⏱️ DEBUG: Timeout after {self._timeout}s", flush=True)
            raise ConversationTimeout(
                f"No response from user {self._user_id} within {self._timeout}s"
            )

    async def wait_callback(self, only_data: bool = True) -> Union[str, CallbackQueryCtx, None]:
        """Wait for the user's next button click

        If ask_buttons() was called before this, reuses the pre-registered future.
        Otherwise, creates and registers a new future (fallback for direct wait_callback calls).

        Args:
            only_data: If True (default), return the decoded callback data ``str``
                (e.g. ``"btn_1"``) for backward compatibility.
                If False, return the full :class:`CallbackQueryCtx` object giving access
                to all callback attributes (``data_str``, ``message_id``, ``chat_instance``,
                ``sender_user_id``, etc.).

        Returns:
            The callback data (``str`` when ``only_data=True``) or the full
            :class:`CallbackQueryCtx` (when ``only_data=False``), or ``None`` if the
            conversation was cancelled.

        Raises:
            ConversationTimeout: if user doesn't click within the timeout period
        """
        # Use pre-registered future from ask_buttons() if available, otherwise create new one
        if self._pending_callback_future is not None:
            future = self._pending_callback_future
            self._pending_callback_future = None
            print(f"⏳ DEBUG: Using pre-registered callback future for chat={self._chat_id}, user={self._user_id}", flush=True)
        else:
            # Fallback: create and register new future
            loop = asyncio.get_running_loop()
            future = loop.create_future()
            print(f"⏳ DEBUG: Registering new callback future for chat={self._chat_id}, user={self._user_id}", flush=True)
            ConversationStore.register_callback(self._chat_id, self._user_id, future)  # pyright: ignore [reportArgumentType]

        try:
            cb_ctx = await asyncio.wait_for(future, timeout=self._timeout)
            if cb_ctx is _CANCELLED:
                print(f"⏹️ DEBUG: Callback conversation cancelled for chat={self._chat_id}, user={self._user_id}", flush=True)
                return None
            if only_data:
                return cb_ctx.data_str or ""
            return cb_ctx  # pyright: ignore [returnType]
        except asyncio.TimeoutError:
            raise ConversationTimeout(
                f"No button click from user {self._user_id} within {self._timeout}s"
            )


def _get_user_id(ctx) -> Optional[int]:
    """Extract plain integer user ID from either context type

    Args:
        ctx: NewMessageCtx or CallbackQueryCtx

    Returns:
        User ID (int) or None if extraction fails
    """
    if isinstance(ctx, CallbackQueryCtx):
        return ctx.sender_user_id

    return _get_message_user_id(ctx)


def _get_message_user_id(ctx) -> Optional[int]:
    """Extract user ID from NewMessageCtx

    Note: sender_id in NewMessageCtx is a MessageSender object (either
    messageSenderUser or messageSenderChat), not a plain integer.

    Args:
        ctx: NewMessageCtx

    Returns:
        User ID if sender is messageSenderUser, None otherwise
    """
    sender = getattr(ctx, "sender_id", None)
    print(f"🔍 DEBUG _get_message_user_id: sender={sender}, type={type(sender).__name__}", flush=True)
    if sender is not None:
        print(f"🔍 DEBUG: sender has user_id? {hasattr(sender, 'user_id')}", flush=True)
        if hasattr(sender, "user_id"):
            user_id = sender.user_id
            print(f"✅ DEBUG: Got user_id = {user_id}", flush=True)
            return user_id
    print(f"❌ DEBUG: Could not extract user_id from sender", flush=True)
    return None
