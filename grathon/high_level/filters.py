"""
Filter DSL for declarative event matching in handlers

Supports composable filters with &, |, ~ operators.
Integrates seamlessly with Router.on(filters=[...]) API.
"""

from __future__ import annotations
import datetime
import re
import time
from typing import Any, Optional, Pattern, TYPE_CHECKING

from grathon.core.contexts.CallbackQueryCtx import CallbackQueryCtx
from grathon.high_level.callback_db import resolve_callback
from grathon.high_level.helpers.validation import InputValidator

if TYPE_CHECKING:
    from grathon.core.contexts.context import Context


class Filter:
    """Base filter class supporting &, |, ~ composition operators"""

    async def __call__(self, ctx: Context) -> bool:
        """Check if filter matches context

        Args:
            ctx: Context object with update and message information

        Returns:
            True if filter matches, False otherwise
        """
        return True

    def __and__(self, other: Filter) -> AndFilter:
        """Combine with AND operator: a & b"""
        return AndFilter(self, other)

    def __or__(self, other: Filter) -> OrFilter:
        """Combine with OR operator: a | b"""
        return OrFilter(self, other)

    def __invert__(self) -> NotFilter:
        """Negate with NOT operator: ~a"""
        return NotFilter(self)


class AndFilter(Filter):
    """Composition: both filters must pass (AND)"""

    def __init__(self, a: Filter, b: Filter):
        self.a = a
        self.b = b

    async def __call__(self, ctx: Context) -> bool:
        """Both filters must return True"""
        return await self.a(ctx) and await self.b(ctx)


class OrFilter(Filter):
    """Composition: either filter can pass (OR)"""

    def __init__(self, a: Filter, b: Filter):
        self.a = a
        self.b = b

    async def __call__(self, ctx: Context) -> bool:
        """Either filter can return True"""
        return await self.a(ctx) or await self.b(ctx)


class NotFilter(Filter):
    """Composition: invert filter result (NOT)"""

    def __init__(self, f: Filter):
        self.f = f

    async def __call__(self, ctx: Context) -> bool:
        """Invert the filter result"""
        return not await self.f(ctx)


class TextFilter(Filter):
    """Match message text with regex pattern"""

    def __init__(self, pattern: str):
        """Initialize with regex pattern

        Args:
            pattern: Regex pattern to match against message text
        """
        self.pattern: Pattern = re.compile(pattern)

    async def __call__(self, ctx: Context) -> bool:
        """Match text with regex"""
        if not hasattr(ctx, "text") or not ctx.text:
            return False
        return bool(self.pattern.search(ctx.text))


class CommandFilter(Filter):
    """Match message command name"""

    def __init__(self, *commands: str):
        """Initialize with command name(s)

        Args:
            *commands: One or more command names (without /)
                      e.g. "start", "help", "ban"
        """
        self.commands: set[str] = set(commands)

    async def __call__(self, ctx: Context) -> bool:
        """Check if message command matches any of the registered commands"""
        if not hasattr(ctx, "command"):
            return False
        return ctx.command in self.commands


class FromUserFilter(Filter):
    """Match message sender user ID

    Supports both static IDs and a callable for dynamic admin lists.
    """

    def __init__(self, *user_ids: int, user_ids_fn=None):
        """Initialize with user ID(s) or a callable that returns user IDs

        Args:
            *user_ids: One or more user IDs to match (static)
            user_ids_fn: Optional callable returning iterable of user IDs (dynamic)
                        Called on every update, so admins added at runtime are recognized.

        Examples:
            F.from_user(12345)                    # static
            F.from_user(user_ids_fn=get_admins)   # dynamic
        """
        self.user_ids: set[int] = set(user_ids)
        self._user_ids_fn = user_ids_fn

    def _get_ids(self) -> set[int]:
        """Get current set of user IDs (static or dynamic)"""
        if self._user_ids_fn is not None:
            return set(self._user_ids_fn())
        return self.user_ids

    async def __call__(self, ctx: Context) -> bool:
        """Check if message sender ID matches any of the registered IDs"""
        if not hasattr(ctx, "user_id"):
            return False

        uid = ctx.user_id
        if uid is None:
            return False

        return uid in self._get_ids()


class CallbackDataFilter(Filter):
    """Match callback button data by regex pattern

    Supports transparent alias resolution for data > 64 bytes.
    """

    def __init__(self, pattern: str):
        """Initialize with regex pattern

        Args:
            pattern: Regex pattern to match against decoded callback data
        """
        self._pattern: Pattern = re.compile(pattern)

    async def __call__(self, ctx: Context) -> bool:
        """Check if callback data matches the regex pattern

        Data is decoded from bytes and aliases are resolved before matching.
        On match, stores the re.Match object on ctx._callback_match for handler access.
        """
        if not isinstance(ctx,CallbackQueryCtx):
            return False
        else:
            ctx:CallbackQueryCtx

        if not hasattr(ctx, "data_str"):
            return False

        data_str = ctx.data_str
        if data_str is None:
            return False

        # Resolve callback alias if present
        from grathon.high_level.callback_db import resolve_callback
        resolved = resolve_callback(data_str)
        if resolved is not None:
            data_str = resolved

        m = self._pattern.search(data_str)
        if m:
            ctx._callback_match = m
        return bool(m)


class QueryFilter(Filter):
    """Match inline query text by regex pattern"""

    def __init__(self, pattern: str):
        """Initialize with regex pattern

        Args:
            pattern: Regex pattern to match against inline query text
        """
        self._pattern: Pattern = re.compile(pattern)

    async def __call__(self, ctx: Context) -> bool:
        """Check if query text matches the regex pattern"""
        from grathon.core.contexts.InlineQueryCtx import InlineQueryCtx

        if not isinstance(ctx, InlineQueryCtx):
            return False

        if not hasattr(ctx, "query"):
            return False

        query = ctx.query
        if query is None:
            return False

        return bool(self._pattern.search(query))


class ChatFilter(Filter):
    """Match message by chat ID"""

    def __init__(self, *chat_ids: int):
        """Initialize with chat ID(s)

        Args:
            *chat_ids: One or more chat IDs to match
        """
        self.chat_ids: set[int] = set(chat_ids)

    async def __call__(self, ctx: Context) -> bool:
        """Check if message chat ID matches any of the registered IDs"""
        if not hasattr(ctx, "chat_id") or ctx.chat_id is None:
            return False
        return ctx.chat_id in self.chat_ids


class PrivateChatFilter(Filter):
    """Match only private/direct chats (user-to-bot)"""

    async def __call__(self, ctx: Context) -> bool:
        """Check if message is from a private chat"""
        if not hasattr(ctx, "chat_id") or ctx.chat_id is None:
            return False
        if not hasattr(ctx, "message") or ctx.message is None:
            return False
        return ctx.chat_id > 0 and not ctx.message.is_channel_post


class GroupChatFilter(Filter):
    """Match group and supergroup chats"""

    async def __call__(self, ctx: Context) -> bool:
        """Check if message is from a group/supergroup"""
        if not hasattr(ctx, "chat_id") or ctx.chat_id is None:
            return False
        if not hasattr(ctx, "message") or ctx.message is None:
            return False
        return ctx.chat_id < 0 and not ctx.message.is_channel_post


class ChannelPostFilter(Filter):
    """Match channel posts"""

    async def __call__(self, ctx: Context) -> bool:
        """Check if message is a channel post"""
        if not hasattr(ctx, "message") or ctx.message is None:
            return False
        return bool(ctx.message.is_channel_post)


class HasMediaFilter(Filter):
    """Match messages with any media content"""

    async def __call__(self, ctx: Context) -> bool:
        """Check if message contains any media"""
        if not hasattr(ctx, "is_photo"):
            return False
        return bool(
            ctx.is_photo
            or ctx.is_video
            or ctx.is_audio
            or ctx.is_document
            or ctx.is_voice
            or ctx.is_animation
            or ctx.is_sticker
        )


class ContentTypeFilter(Filter):
    """Match messages by specific content type"""

    _TYPE_MAP = {
        "text": lambda ctx: bool(ctx.text and not getattr(ctx, "command", None)),
        "photo": lambda ctx: bool(ctx.is_photo),
        "video": lambda ctx: bool(ctx.is_video),
        "audio": lambda ctx: bool(ctx.is_audio),
        "voice": lambda ctx: bool(ctx.is_voice),
        "document": lambda ctx: bool(ctx.is_document),
        "sticker": lambda ctx: bool(ctx.is_sticker),
        "animation": lambda ctx: bool(ctx.is_animation),
    }

    def __init__(self, *types: str):
        """Initialize with content type(s)

        Args:
            *types: Content type names (text, photo, video, audio, voice,
                   document, sticker, animation)
        """
        self.types: set[str] = set(types)

    async def __call__(self, ctx: Context) -> bool:
        """Check if message content matches any of the registered types"""
        if not hasattr(ctx, "is_photo"):
            return False
        for t in self.types:
            checker = self._TYPE_MAP.get(t)
            if checker and checker(ctx):
                return True
        return False


def _get_message(ctx: Context):
    """Helper: Extract message from NewMessageCtx or Context[updateNewMessage]"""
    msg = getattr(ctx, "message", None)
    if msg is None:
        update = getattr(ctx, "update", None)
        if update is not None:
            msg = getattr(update, "message", None)
    return msg


class IncomingFilter(Filter):
    """Match only incoming messages (not sent by current user)"""

    async def __call__(self, ctx: Context) -> bool:
        msg = _get_message(ctx)
        if msg is None:
            return False
        return not bool(getattr(msg, "is_outgoing", False))


class OutgoingFilter(Filter):
    """Match only outgoing messages (sent by current user)"""

    async def __call__(self, ctx: Context) -> bool:
        msg = _get_message(ctx)
        if msg is None:
            return False
        return bool(getattr(msg, "is_outgoing", False))


class IsForwardedFilter(Filter):
    """Match forwarded messages"""

    async def __call__(self, ctx: Context) -> bool:
        """Check if message is forwarded"""
        if not hasattr(ctx, "message") or ctx.message is None:
            return False
        return ctx.message.forward_info is not None


class IsReplyFilter(Filter):
    """Match reply messages"""

    async def __call__(self, ctx: Context) -> bool:
        """Check if message is a reply"""
        if not hasattr(ctx, "reply_to"):
            return False
        return ctx.reply_to is not None


class IsPinnedFilter(Filter):
    """Match pinned messages"""

    async def __call__(self, ctx: Context) -> bool:
        """Check if message is pinned"""
        if not hasattr(ctx, "message") or ctx.message is None:
            return False
        return bool(ctx.message.is_pinned)


class IsAlbumFilter(Filter):
    """Match messages in an album/media group"""

    async def __call__(self, ctx: Context) -> bool:
        """Check if message is part of an album"""
        if not hasattr(ctx, "message") or ctx.message is None:
            return False
        return ctx.message.media_album_id != 0


class ExactTextFilter(Filter):
    """Match exact message text"""

    def __init__(self, *texts: str, case_sensitive: bool = False):
        """Initialize with exact text(s)

        Args:
            *texts: One or more exact text strings to match
            case_sensitive: If False, comparison is case-insensitive
        """
        self.case_sensitive = case_sensitive
        if case_sensitive:
            self.texts: set[str] = set(texts)
        else:
            self.texts = {t.lower() for t in texts}

    async def __call__(self, ctx: Context) -> bool:
        """Check if message text matches exactly"""
        if not hasattr(ctx, "text") or not ctx.text:
            return False
        text = ctx.text if self.case_sensitive else ctx.text.lower()
        return text in self.texts


class StartsWithFilter(Filter):
    """Match messages starting with prefix"""

    def __init__(self, *prefixes: str, case_sensitive: bool = False):
        """Initialize with prefix(es)

        Args:
            *prefixes: One or more prefixes to match
            case_sensitive: If False, comparison is case-insensitive
        """
        self.case_sensitive = case_sensitive
        if case_sensitive:
            self.prefixes: tuple = tuple(prefixes)
        else:
            self.prefixes = tuple(p.lower() for p in prefixes)

    async def __call__(self, ctx: Context) -> bool:
        """Check if message text starts with any prefix"""
        if not hasattr(ctx, "text") or not ctx.text:
            return False
        text = ctx.text if self.case_sensitive else ctx.text.lower()
        return any(text.startswith(p) for p in self.prefixes)


class EndsWithFilter(Filter):
    """Match messages ending with suffix"""

    def __init__(self, *suffixes: str, case_sensitive: bool = False):
        """Initialize with suffix(es)

        Args:
            *suffixes: One or more suffixes to match
            case_sensitive: If False, comparison is case-insensitive
        """
        self.case_sensitive = case_sensitive
        if case_sensitive:
            self.suffixes: tuple = tuple(suffixes)
        else:
            self.suffixes = tuple(s.lower() for s in suffixes)

    async def __call__(self, ctx: Context) -> bool:
        """Check if message text ends with any suffix"""
        if not hasattr(ctx, "text") or not ctx.text:
            return False
        text = ctx.text if self.case_sensitive else ctx.text.lower()
        return any(text.endswith(s) for s in self.suffixes)


class ContainsFilter(Filter):
    """Match messages containing keyword(s)"""

    def __init__(
        self,
        *keywords: str,
        all_required: bool = False,
        case_sensitive: bool = False,
    ):
        """Initialize with keyword(s)

        Args:
            *keywords: One or more keywords to search for
            all_required: If True, all keywords must be present; if False, any
            case_sensitive: If False, comparison is case-insensitive
        """
        self.case_sensitive = case_sensitive
        self.all_required = all_required
        if case_sensitive:
            self.keywords: tuple = tuple(keywords)
        else:
            self.keywords = tuple(k.lower() for k in keywords)

    async def __call__(self, ctx: Context) -> bool:
        """Check if message contains keyword(s)"""
        if not hasattr(ctx, "text") or not ctx.text:
            return False
        text = ctx.text if self.case_sensitive else ctx.text.lower()
        if self.all_required:
            return all(k in text for k in self.keywords)
        return any(k in text for k in self.keywords)


class LengthFilter(Filter):
    """Match messages by text length"""

    def __init__(self, min_len: int = 0, max_len: Optional[int] = None):
        """Initialize with length constraints

        Args:
            min_len: Minimum text length (inclusive)
            max_len: Maximum text length (inclusive), None = unlimited
        """
        self.min_len = min_len
        self.max_len = max_len if max_len is not None else 2147483647

    async def __call__(self, ctx: Context) -> bool:
        """Check if message text length is in range"""
        if not hasattr(ctx, "text") or not ctx.text:
            return False
        return self.min_len <= len(ctx.text) <= self.max_len


class RateLimitFilter(Filter):
    """Rate limit messages per user"""

    def __init__(self, limit: int, period: float):
        """Initialize rate limiter

        Args:
            limit: Maximum number of messages allowed
            period: Time period in seconds
        """
        self.limit = limit
        self.period = period
        self._hits: dict[int, list[float]] = {}

    async def __call__(self, ctx: Context) -> bool:
        """Check if message exceeds rate limit"""
        user_id = None
        if hasattr(ctx, "sender_id") and ctx.sender_id:
            if hasattr(ctx.sender_id, "user_id"):
                user_id = ctx.sender_id.user_id

        if user_id is None:
            return True

        now = time.monotonic()
        hits = self._hits.setdefault(user_id, [])
        self._hits[user_id] = [t for t in hits if now - t < self.period]

        if len(self._hits[user_id]) >= self.limit:
            return False

        self._hits[user_id].append(now)
        return True


class TimeRangeFilter(Filter):
    """Match messages within a time range (UTC)"""

    def __init__(self, start_hour: int, end_hour: int):
        """Initialize time range filter

        Args:
            start_hour: Start hour (0-23, UTC)
            end_hour: End hour (0-23, UTC); wraps midnight if start > end
        """
        self.start_hour = start_hour
        self.end_hour = end_hour

    async def __call__(self, ctx: Context) -> bool:
        """Check if current time is within range"""
        hour = datetime.datetime.utcnow().hour
        if self.start_hour <= self.end_hour:
            return self.start_hour <= hour < self.end_hour
        return hour >= self.start_hour or hour < self.end_hour


class WeekdayFilter(Filter):
    """Match messages by weekday"""

    def __init__(self, *days: int):
        """Initialize weekday filter

        Args:
            *days: Weekday numbers (0=Monday, 6=Sunday)
        """
        self.days: set[int] = set(days)

    async def __call__(self, ctx: Context) -> bool:
        """Check if current weekday matches"""
        return datetime.datetime.utcnow().weekday() in self.days


class LambdaFilter(Filter):
    """Custom async predicate filter"""

    def __init__(self, func):
        """Initialize with async function

        Args:
            func: Async function that takes Context and returns bool
        """
        self.func = func

    async def __call__(self, ctx: Context) -> bool:
        """Execute custom predicate"""
        return bool(await self.func(ctx))


class StateFilter(Filter):
    """Match conversation state from session"""

    def __init__(self, *states: str):
        """Initialize with state(s)

        Args:
            *states: Expected state values from ctx.session.get("state")
        """
        self.states: set[str] = set(states)

    async def __call__(self, ctx: Context) -> bool:
        """Check if session state matches"""
        if not hasattr(ctx, "session"):
            return False
        current_state = ctx.session.get("state")
        return current_state in self.states


class TextTypeFilter(Filter):
    """Match text by format/type (number, email, url, phone, etc.)"""

    def __init__(self, type_name: str):
        """Initialize with text type

        Args:
            type_name: Type name (number, integer, email, url, phone,
                      username, persian)
        """
        self.type_name = type_name

    async def __call__(self, ctx: Context) -> bool:
        """Check if text matches the specified type"""
        if not hasattr(ctx, "text") or not ctx.text:
            return False

        validators = {
            "number": InputValidator.is_number,
            "integer": InputValidator.is_integer,
            "email": InputValidator.is_email,
            "url": InputValidator.is_url,
            "phone": InputValidator.is_phone,
            "username": InputValidator.is_username,
            "persian": InputValidator.is_persian,
        }

        validator = validators.get(self.type_name)
        if validator is None:
            return False
        return bool(validator(ctx.text))


class F:
    """Filter builder namespace — factory for creating common filters

    Usage:
        F.text(r"hello|سلام")
        F.command("start", "begin")
        F.from_user(12345, 67890)

    Composition:
        F.command("start") | F.command("help")    # OR
        F.command("ban") & F.from_user(12345)     # AND
        ~F.command("start")                        # NOT
    """

    @staticmethod
    def text(pattern: str) -> TextFilter:
        """Create regex text filter

        Args:
            pattern: Regex pattern to match against message text

        Returns:
            TextFilter instance

        Examples:
            >>> F.text(r"hello|hi")
            >>> F.text(r"^/")  # starts with /
            >>> F.text(r"[0-9]+")  # contains digits
        """
        return TextFilter(pattern)

    @staticmethod
    def incoming() -> IncomingFilter:
        """Match only incoming messages (not sent by current user)

        Examples:
            >>> F.incoming()
        """
        return IncomingFilter()

    @staticmethod
    def outgoing() -> OutgoingFilter:
        """Match only outgoing messages (sent by current user)

        Examples:
            >>> F.outgoing()
        """
        return OutgoingFilter()

    @staticmethod
    def command(*commands: str) -> CommandFilter:
        """Create command filter

        Args:
            *commands: One or more command names (without /)

        Returns:
            CommandFilter instance

        Examples:
            >>> F.command("start")
            >>> F.command("start", "begin")
            >>> F.command("help", "?")
        """
        return CommandFilter(*commands)

    @staticmethod
    def from_user(*user_ids: int, user_ids_fn=None) -> FromUserFilter:
        """Create user ID filter

        Args:
            *user_ids: One or more user IDs to match (static)
            user_ids_fn: Optional callable returning iterable of user IDs (dynamic)
                        Called on every update, so admins added at runtime are recognized.

        Returns:
            FromUserFilter instance

        Examples:
            >>> F.from_user(12345)
            >>> F.from_user(12345, 67890)  # admin IDs
            >>> F.from_user(user_ids_fn=lambda: config.ADMINS)  # dynamic
        """
        return FromUserFilter(*user_ids, user_ids_fn=user_ids_fn)

    @staticmethod
    def callback(pattern: str) -> CallbackDataFilter:
        """Create callback button data filter

        Args:
            pattern: Regex pattern to match against decoded callback data

        Returns:
            CallbackDataFilter instance

        Examples:
            >>> F.callback(r"^confirm$")
            >>> F.callback(r"delete_\\d+")
            >>> F.callback(r"action:.*")
        """
        return CallbackDataFilter(pattern)

    @staticmethod
    def query(pattern: str) -> QueryFilter:
        """Create inline query text filter

        Args:
            pattern: Regex pattern to match against inline query text

        Returns:
            QueryFilter instance

        Examples:
            >>> F.query(r"^dog")
            >>> F.query(r"cat|kitten")
        """
        return QueryFilter(pattern)

    @staticmethod
    def chat(*chat_ids: int) -> ChatFilter:
        """Create chat ID filter

        Args:
            *chat_ids: One or more chat IDs to match

        Returns:
            ChatFilter instance

        Examples:
            >>> F.chat(12345)
            >>> F.chat(12345, 67890)  # multiple chats
        """
        return ChatFilter(*chat_ids)

    @staticmethod
    def private() -> PrivateChatFilter:
        """Create private chat filter

        Returns:
            PrivateChatFilter instance

        Examples:
            >>> F.private()  # match only user-to-bot messages
        """
        return PrivateChatFilter()

    @staticmethod
    def group() -> GroupChatFilter:
        """Create group chat filter

        Returns:
            GroupChatFilter instance

        Examples:
            >>> F.group()  # match only group/supergroup messages
        """
        return GroupChatFilter()

    @staticmethod
    def channel() -> ChannelPostFilter:
        """Create channel post filter

        Returns:
            ChannelPostFilter instance

        Examples:
            >>> F.channel()  # match only channel posts
        """
        return ChannelPostFilter()

    @staticmethod
    def has_media() -> HasMediaFilter:
        """Create media presence filter

        Returns:
            HasMediaFilter instance

        Examples:
            >>> F.has_media()  # match messages with photo, video, audio, etc.
        """
        return HasMediaFilter()

    @staticmethod
    def content(*types: str) -> ContentTypeFilter:
        """Create content type filter

        Args:
            *types: Content type names (text, photo, video, audio, voice,
                   document, sticker, animation)

        Returns:
            ContentTypeFilter instance

        Examples:
            >>> F.content("photo")
            >>> F.content("video", "animation")
        """
        return ContentTypeFilter(*types)

    @staticmethod
    def is_forwarded() -> IsForwardedFilter:
        """Create forwarded message filter

        Returns:
            IsForwardedFilter instance

        Examples:
            >>> F.is_forwarded()
        """
        return IsForwardedFilter()

    @staticmethod
    def is_reply() -> IsReplyFilter:
        """Create reply message filter

        Returns:
            IsReplyFilter instance

        Examples:
            >>> F.is_reply()
        """
        return IsReplyFilter()

    @staticmethod
    def is_pinned() -> IsPinnedFilter:
        """Create pinned message filter

        Returns:
            IsPinnedFilter instance

        Examples:
            >>> F.is_pinned()
        """
        return IsPinnedFilter()

    @staticmethod
    def is_album() -> IsAlbumFilter:
        """Create album/media group filter

        Returns:
            IsAlbumFilter instance

        Examples:
            >>> F.is_album()  # match messages in an album
        """
        return IsAlbumFilter()

    @staticmethod
    def exact(*texts: str, case_sensitive: bool = False) -> ExactTextFilter:
        """Create exact text match filter

        Args:
            *texts: Exact text(s) to match
            case_sensitive: If False, comparison is case-insensitive

        Returns:
            ExactTextFilter instance

        Examples:
            >>> F.exact("hello")
            >>> F.exact("hello", "سلام", case_sensitive=False)
        """
        return ExactTextFilter(*texts, case_sensitive=case_sensitive)

    @staticmethod
    def starts_with(*prefixes: str, case_sensitive: bool = False) -> StartsWithFilter:
        """Create prefix match filter

        Args:
            *prefixes: One or more prefixes to match
            case_sensitive: If False, comparison is case-insensitive

        Returns:
            StartsWithFilter instance

        Examples:
            >>> F.starts_with("/")
            >>> F.starts_with("Hello", "Hi", case_sensitive=False)
        """
        return StartsWithFilter(*prefixes, case_sensitive=case_sensitive)

    @staticmethod
    def ends_with(*suffixes: str, case_sensitive: bool = False) -> EndsWithFilter:
        """Create suffix match filter

        Args:
            *suffixes: One or more suffixes to match
            case_sensitive: If False, comparison is case-insensitive

        Returns:
            EndsWithFilter instance

        Examples:
            >>> F.ends_with("?")
            >>> F.ends_with("!", "?", case_sensitive=False)
        """
        return EndsWithFilter(*suffixes, case_sensitive=case_sensitive)

    @staticmethod
    def contains(
        *keywords: str, all_required: bool = False, case_sensitive: bool = False
    ) -> ContainsFilter:
        """Create keyword match filter

        Args:
            *keywords: One or more keywords to search for
            all_required: If True, all keywords must be present
            case_sensitive: If False, comparison is case-insensitive

        Returns:
            ContainsFilter instance

        Examples:
            >>> F.contains("hello")
            >>> F.contains("foo", "bar", all_required=True)  # must have both
        """
        return ContainsFilter(
            *keywords, all_required=all_required, case_sensitive=case_sensitive
        )

    @staticmethod
    def length(min_len: int = 0, max_len: Optional[int] = None) -> LengthFilter:
        """Create text length filter

        Args:
            min_len: Minimum text length
            max_len: Maximum text length (None = unlimited)

        Returns:
            LengthFilter instance

        Examples:
            >>> F.length(1, 100)  # between 1 and 100 characters
            >>> F.length(min_len=10)  # at least 10 characters
        """
        return LengthFilter(min_len, max_len)

    @staticmethod
    def rate_limit(limit: int, period: float) -> RateLimitFilter:
        """Create rate limit filter

        Args:
            limit: Maximum number of messages allowed
            period: Time period in seconds

        Returns:
            RateLimitFilter instance

        Examples:
            >>> F.rate_limit(5, 60)  # max 5 messages per minute per user
        """
        return RateLimitFilter(limit, period)

    @staticmethod
    def time_range(start_hour: int, end_hour: int) -> TimeRangeFilter:
        """Create time range filter (UTC)

        Args:
            start_hour: Start hour (0-23)
            end_hour: End hour (0-23); wraps midnight if start > end

        Returns:
            TimeRangeFilter instance

        Examples:
            >>> F.time_range(9, 17)  # 9am to 5pm UTC
            >>> F.time_range(22, 8)  # 10pm to 8am UTC (wraps midnight)
        """
        return TimeRangeFilter(start_hour, end_hour)

    @staticmethod
    def weekday(*days: int) -> WeekdayFilter:
        """Create weekday filter

        Args:
            *days: Weekday numbers (0=Monday, 6=Sunday)

        Returns:
            WeekdayFilter instance

        Examples:
            >>> F.weekday(0, 1, 2, 3, 4)  # weekdays only
            >>> F.weekday(5, 6)  # weekends only
        """
        return WeekdayFilter(*days)

    @staticmethod
    def custom(func) -> LambdaFilter:
        """Create custom async predicate filter

        Args:
            func: Async function(ctx) -> bool

        Returns:
            LambdaFilter instance

        Examples:
            >>> async def is_admin(ctx):
            ...     return ctx.sender_id.user_id in ADMINS
            >>> F.custom(is_admin)
        """
        return LambdaFilter(func)

    @staticmethod
    def state(*states: str) -> StateFilter:
        """Create conversation state filter

        Args:
            *states: Expected state value(s) from ctx.session.get("state")

        Returns:
            StateFilter instance

        Examples:
            >>> F.state("waiting_name")
            >>> F.state("step_1", "step_2")
        """
        return StateFilter(*states)

    @staticmethod
    def text_type(type_name: str) -> TextTypeFilter:
        """Create text format/type filter

        Args:
            type_name: Format type (number, integer, email, url, phone,
                      username, persian)

        Returns:
            TextTypeFilter instance

        Examples:
            >>> F.text_type("email")
            >>> F.text_type("phone")
        """
        return TextTypeFilter(type_name)
