# Grathon API Reference

## `GrathonBot`

The main entry point for building a Telegram bot.

### Constructor

```python
GrathonBot(
    api_id: int,
    api_hash: str,
    bot_token: str,
    database_directory: str = "bot_db",
    *,
    system_language_code: str = "en",
    device_model: str = "Bot",
    application_version: str = "1.0",
)
```

### Methods

| Method | Signature | Description |
|---|---|---|
| `on_command` | `on_command(command: str) -> decorator` | Register a command handler (without `/`) |
| `on_message` | `on_message(filters=None) -> decorator` | Register a message handler with optional filters |
| `on_callback` | `on_callback(pattern: str \| None = None) -> decorator` | Register an inline button callback handler |
| `on_inline_query` | `on_inline_query(pattern: str \| None = None) -> decorator` | Register an inline query handler |
| `on` | `on(event_type: type, filters=None) -> decorator` | Register a handler for any TDLib update type |
| `include_router` | `include_router(router) -> None` | Include a Router instance |
| `use` | `use(middleware) -> None` | Register a middleware function |
| `start` | `start() -> Awaitable[None]` | Start the bot (blocks forever) |
| `stop` | `stop() -> Awaitable[None]` | Stop the bot gracefully |
| `send_file` | `send_file(chat_id, file_path, caption="", file_type="auto") -> bool` | Send a file to a chat |
| `download_file` | `download_file(file_id, output_path="") -> str` | Download a file from Telegram |
| `set_bandwidth_limit` | `set_bandwidth_limit(limit_mbps: int) -> None` | Limit file operation bandwidth |
| `set_chunk_size` | `set_chunk_size(chunk_size: int) -> None` | Set chunk size for file operations |
| `get_me` | `get_me() -> Awaitable[User]` | Get bot user info |
| `error_handler` | `error_handler() -> decorator` | Register a global error handler |

### Properties

| Property | Type | Description |
|---|---|---|
| `api` | `GeneratedMethods` | Direct access to TDLib generated API methods |
| `session` | `SessionStore` | Session store for the bot |
| `file_optimizer` | `FileOptimizer` | File optimization settings |
| `callback_query_router` | `CallbackQueryRouter` | Router for callback queries |
| `inline_query_router` | `InlineQueryRouter` | Router for inline queries |

---

## `F` — Filter DSL

All filters are composable with `&` (AND), `\|` (OR), and `~` (NOT).

### Static Factory Methods

| Method | Returns | Description |
|---|---|---|
| `F.command(*commands)` | `CommandFilter` | Match message command name(s) |
| `F.text(pattern)` | `TextFilter` | Match message text with regex |
| `F.exact(*texts, case_sensitive=False)` | `ExactTextFilter` | Match exact text |
| `F.starts_with(*prefixes, case_sensitive=False)` | `StartsWithFilter` | Match text starting with prefix |
| `F.ends_with(*suffixes, case_sensitive=False)` | `EndsWithFilter` | Match text ending with suffix |
| `F.contains(*keywords, all_required=False, case_sensitive=False)` | `ContainsFilter` | Match text containing keyword(s) |
| `F.length(min_len, max_len=None)` | `LengthFilter` | Match text length range |
| `F.from_user(*user_ids, user_ids_fn=None)` | `FromUserFilter` | Match sender user ID(s) |
| `F.chat(*chat_ids)` | `ChatFilter` | Match chat ID(s) |
| `F.private()` | `PrivateChatFilter` | Match private chats only |
| `F.group()` | `GroupChatFilter` | Match group/supergroup chats |
| `F.channel()` | `ChannelPostFilter` | Match channel posts |
| `F.has_media()` | `HasMediaFilter` | Match messages with any media |
| `F.content(*types)` | `ContentTypeFilter` | Match specific content types (text, photo, video, etc.) |
| `F.callback(pattern)` | `CallbackDataFilter` | Match callback button data by regex |
| `F.query(pattern)` | `QueryFilter` | Match inline query text by regex |
| `F.incoming()` | `IncomingFilter` | Match incoming messages only |
| `F.outgoing()` | `OutgoingFilter` | Match outgoing messages only |
| `F.is_forwarded()` | `IsForwardedFilter` | Match forwarded messages |
| `F.is_reply()` | `IsReplyFilter` | Match reply messages |
| `F.is_pinned()` | `IsPinnedFilter` | Match pinned messages |
| `F.is_album()` | `IsAlbumFilter` | Match messages in an album |
| `F.rate_limit(limit, period)` | `RateLimitFilter` | Rate limit messages per user |
| `F.time_range(start_hour, end_hour)` | `TimeRangeFilter` | Match messages within UTC time range |
| `F.weekday(*days)` | `WeekdayFilter` | Match messages by weekday (0=Mon, 6=Sun) |
| `F.custom(func)` | `LambdaFilter` | Custom async predicate filter |
| `F.state(*states)` | `StateFilter` | Match conversation state from session |
| `F.text_type(type_name)` | `TextTypeFilter` | Match text by format (number, email, url, phone, username, persian) |

### Composition

```python
# AND
F.command("start") & F.from_user(12345)

# OR
F.command("start") | F.command("help")

# NOT
~F.command("start")

# Mixed
(F.command("start") | F.command("help")) & F.private()
```

---

## `KeyboardBuilder`

Fluent builder for inline keyboards (`replyMarkupInlineKeyboard`).

### Methods

| Method | Returns | Description |
|---|---|---|
| `button(text, callback_data, style=None)` | `KeyboardBuilder` | Add callback button to current row |
| `url_button(text, url, style=None)` | `KeyboardBuilder` | Add URL button |
| `switch_inline_button(text, query, ...)` | `KeyboardBuilder` | Add switch inline button |
| `primary_button(text, callback_data)` | `KeyboardBuilder` | Add primary (blue) callback button |
| `danger_button(text, callback_data)` | `KeyboardBuilder` | Add danger (red) callback button |
| `success_button(text, callback_data)` | `KeyboardBuilder` | Add success (green) callback button |
| `close_button(text="❌ بستن", closing_message=None)` | `KeyboardBuilder` | Add auto-close button |
| `row()` | `KeyboardBuilder` | Start a new row |
| `build()` | `replyMarkupInlineKeyboard` | Build final keyboard markup |

### Callback Data Encoding

- `str` → UTF-8 bytes
- `bytes` → used as-is
- `dict` → JSON-encoded
- If > 64 bytes → auto-compressed via zlib + base64, stored in `CallbackStore`

---

## `PluginManager`

Manages plugin lifecycle with built-in admin commands.

### Constructor

```python
PluginManager(
    target: PluginTarget,       # GrathonBot or TdClient
    admin_ids: list[int],
    plugin_dir: str = "./plugins",
    texts: Optional[PluginManagerTexts] = None,
    conversation_timeout: float = 120.0,
)
```

### Methods

| Method | Returns | Description |
|---|---|---|
| `load(file_path)` | `PluginRecord` | Load a plugin from file path |
| `unload(name)` | `bool` | Unload a plugin by name |
| `reload(name)` | `PluginRecord` | Reload a plugin |
| `reload_all()` | `list[PluginRecord]` | Reload all plugins |
| `rescan_all()` | `tuple[list, int, int, int]` | Rescan directory and reload all |
| `get(name)` | `Optional[PluginRecord]` | Get plugin record by name |
| `list_all()` | `list[PluginRecord]` | List all plugins sorted by name |

### Plugin Format

Each plugin must define:

```python
PLUGIN_NAME = "my_plugin"       # lowercase, snake_case
PLUGIN_VERSION = "1.0.0"
PLUGIN_DESCRIPTION = "Description"

def setup(router):
    from grathon.high_level import F
    from grathon.core.TLSchema_Manager.tltypes import updateNewMessage

    @router.on(updateNewMessage, filters=[F.command("hello")])
    async def hello(ctx):
        await ctx.reply("Hello!")
```

### Admin Commands (auto-registered)

| Command | Description |
|---|---|
| `/plugins` | List all loaded plugins |
| `/upload` | Upload a plugin file (`.py`) or archive (`.zip`) |
| `/reload <name>` | Reload a plugin |
| `/reload_all` | Reload all plugins |
| `/rescan_plugins` | Scan for new plugins + reload all |
| `/unload <name>` | Unload a plugin |
| `/delete <name>` | Delete a plugin file/folder |
| `/export_plugin <name>` | Download plugin as file or ZIP |
| `/plugin_help` | Show admin help |

---

## Context Classes

### `Context` (base)

| Property | Type | Description |
|---|---|---|
| `client` | `TdClient` | The TDLib client |
| `update` | `TUpdate` | The raw update object |
| `api` | `GeneratedMethods` | Direct TDLib API access |
| `chat_id` | `Optional[int]` | Chat ID (override in subclasses) |
| `user_id` | `Optional[int]` | Sender user ID (unified across contexts) |
| `session` | `dict` | Session data for this chat (persists across messages) |
| `data` | `dict` | Shared data dict for passing data between filters and handlers |

#### `ctx.data`

A shared dictionary attached to the context object. Useful for passing data from filters to handlers, or between functions that receive the same `ctx`:

```python
# Set in a filter
ctx.data["auth_passed"] = True
ctx.data["admin_level"] = "super"

# Read in a handler
if ctx.data.get("auth_passed"):
    await show_vip_content(ctx)
```

#### `ctx.session`

Per-chat key-value storage that persists across messages within the same chat:

```python
# Store a value
ctx.session["step"] = 1
ctx.session["user_name"] = "Ali"

# Read a value
step = ctx.session.get("step", 0)

# Delete a value
del ctx.session["step"]
```

`session` is backed by `SessionStore` (accessed via `bot.session`). If no session store is configured, `ctx.session` returns an empty dict.

### `NewMessageCtx`

For `updateNewMessage` events. Adds:

| Property | Type | Description |
|---|---|---|
| `message` | `Message` | The message object |
| `text` | `Optional[str]` | Message text |
| `command` | `Optional[str]` | Command name (without `/`) |
| `args` | `list[str]` | Command arguments |
| `reply_to` | `Optional[int]` | Replied message ID |
| `is_photo`, `is_video`, etc. | `bool` | Media type flags |
| `sender_id` | `Optional[MessageSender]` | Message sender |
| `sender_user_id` | `Optional[int]` | Sender user ID |

### `CallbackQueryCtx`

For `updateNewCallbackQuery` events. Adds:

| Property | Type | Description |
|---|---|---|
| `query_id` | `str` | Callback query ID |
| `sender_user_id` | `int` | User who clicked |
| `chat_id` | `Optional[int]` | Chat containing the message |
| `message_id` | `int` | Message ID with the button |
| `data_str` | `Optional[str]` | Decoded callback data (auto-resolves aliases) |
| `match` | `Optional[re.Match]` | Regex match from `F.callback()` |

### `InlineQueryCtx`

For `updateNewInlineQuery` events. Adds:

| Property | Type | Description |
|---|---|---|
| `query` | `Optional[str]` | Inline query text |
| `sender_user_id` | `Optional[int]` | User who sent the query |

---

## Context Methods

### `NewMessageCtx`

| Method | Signature | Description |
|---|---|---|
| `reply` | `reply(text=None, file=None, file_type="auto", reply_markup=None, parse_mode="markdown")` | Send a reply message |
| `reply_markdown` | `reply_markdown(text, reply_markup=None)` | Reply with Markdown formatting |
| `reply_html` | `reply_html(text, reply_markup=None)` | Reply with HTML formatting |
| `edit_message` | `edit_message(text, reply_markup=None, parse_mode="markdown")` | Edit the current message |
| `edit_message_caption` | `edit_message_caption(text, reply_markup=None, show_caption_above_media=False)` | Edit media caption |
| `edit_message_media` | `edit_message_media(input_message_content, reply_markup=None)` | Edit message media |
| `delete_message` | `delete_message(revoke=True)` | Delete a message |
| `get_replied_message` | `get_replied_message()` | Get the replied message object |
| `send_file` | `send_file(file_path, caption="", file_type="auto")` | Send a file |

### `CallbackQueryCtx`

| Method | Signature | Description |
|---|---|---|
| `answer` | `answer(text="", alert=False)` | Answer the callback query |
| `edit_message` | `edit_message(text, parse_mode="markdown", reply_markup=None)` | Edit the message with the button |
| `edit_message_caption` | `edit_message_caption(text, reply_markup=None, show_caption_above_media=False)` | Edit media caption |
| `edit_message_reply_markup` | `edit_message_reply_markup(reply_markup=None)` | Edit only the inline keyboard |
| `delete_message` | `delete_message(revoke=True)` | Delete the message |
| `send_message` | `send_message(text=None, file=None, file_type="auto", reply_markup=None)` | Send a new message to the same chat |
| `reply` | `reply(text=None, file=None, file_type="auto", reply_markup=None)` | Reply to the same chat |
| `send_file` | `send_file(file_path, caption="", file_type="auto")` | Send a file to the same chat |

---

## `TdClient` (Low-Level)

### Methods

| Method | Signature | Description |
|---|---|---|
| `send` | `send(query: dict) -> str` | Send raw JSON to TDLib, returns `@extra` ID |
| `call_method` | `call_method(method_name, params_dict=None, **params) -> Any` | Call TDLib method and wait for response |
| `use` | `use(middleware)` | Register middleware in dispatch pipeline |
| `include_router` | `include_router(router, nostore=False)` | Include router handlers |
| `remove_router` | `remove_router(router)` | Remove a router |
| `reload_routers` | `reload_routers()` | Rebuild handler list from all routers |
| `add_handler` | `add_handler(handler)` | Add handler directly |
| `remove_handler` | `remove_handler(handler) -> bool` | Remove handler by identity |
| `put_update` | `put_update(data)` | Put update into queue |
| `put_extra` | `put_extra(data)` | Put extra (API response) into queue |

---

## `Router`

### Methods

| Method | Signature | Description |
|---|---|---|
| `on` | `on(event_type, filters=None, callback=None)` | Register a handler for an event type |
| `append` | `append(router)` | Add sub-router |
| `include_router` | `include_router(router)` | Include router (recursive) |

---

## `EventHandler`

### Constructor

```python
EventHandler(
    event_type: type[TUpdate],
    callback: Callable[[Context[TUpdate]], Any],
    filters: List[Callable[[Context[TUpdate]], Awaitable[bool]]] | None = None,
)
```

### Methods

| Method | Signature | Description |
|---|---|---|
| `check_and_execute` | `check_and_execute(ctx) -> bool` | Run filters then callback |

---

## Middleware

### Type

```python
Middleware: TypeAlias = Callable[[Any, Callable[[Any], Awaitable[None]]], Awaitable[None]]
```

A middleware receives `(ctx, next)` and must call `await next(ctx)` to continue the chain.

### Built-in Middlewares

| Middleware | Location | Description |
|---|---|---|
| `retry_middleware` | `high_level/middlewares/retry.py` | Auto-retry failed sends |
| `message_send_middleware` | `high_level/helpers/message_send_middleware.py` | Tracks message send status |
| `debug_middleware` | `high_level/helpers/debug_middleware.py` | Logs all events |
| `conversation_middleware` | `high_level/conversations.py` | Manages conversation state with `Conversation` context manager |

---

## `Conversation` & `ConversationTimeout`

### `ConversationTimeout`

Exception raised when a conversation times out waiting for user input.

### `Conversation`

Context manager for multi-step conversations. Automatically manages state and waits for the next matching message or callback.

```python
from grathon.high_level.conversations import Conversation

async def handler(ctx):
    async with Conversation(ctx, timeout=60.0) as conv:
        await ctx.reply("What's your name?")
        name = await conv.wait_message()

        await ctx.reply(f"Nice to meet you, {name}! Now choose an option:")
        option = await conv.wait_callback()
        # option is the callback data string
```

### `Conversation` Methods

| Method | Signature | Description |
|---|---|---|
| `wait_message()` | `wait_message(only_text=True) -> str \| NewMessageCtx \| None` | Wait for the next message (any content type). Default `only_text=True` returns plain ``str`` (text/caption, ``""`` for media without caption). With `only_text=False` returns the full :class:`NewMessageCtx` exposing ``file_id``, ``is_photo``, ``content``, ``remote_file_id``, etc. Returns ``None`` when cancelled |
| `wait_callback()` | `wait_callback(only_data=True) -> str \| CallbackQueryCtx \| None` | Wait for the next callback query. Default `only_data=True` returns decoded ``str``. With `only_data=False` returns the full :class:`CallbackQueryCtx` exposing ``data_str``, ``message_id``, ``chat_instance``, ``sender_user_id``, etc. Returns ``None`` when cancelled |
| `ask(text, **kwargs)` | `ask(text, **kwargs) -> None` | Send a message and wait for the next message |
| `ask_buttons(text, reply_markup, **kwargs)` | `ask_buttons(text, reply_markup, **kwargs) -> None` | Send a message with inline keyboard and wait for callback |

Receiving a file (photo / video / document) in a conversation:

```python
from grathon.high_level.conversations import Conversation

async def handler(ctx):
    async with Conversation(ctx, timeout=120.0) as conv:
        await conv.ask("Send me a file:")
        reply = await conv.wait_message(only_text=False)  # full NewMessageCtx
        if reply is None:
            return  # cancelled (cancel button) — not a timeout
        if reply.is_document:
            # Media accessors come from NewMessageCtx
            file_id = reply.file_id          # TDLib file id (int)
            remote_id = reply.remote_file_id # persistent Telegram file_id (str)
        else:
            await ctx.reply(f"Got text: {reply.text}")
```

### `conversation_middleware`

Middleware that enables the `Conversation` context manager. Install it before creating the `PluginManager`:

```python
from grathon.high_level.conversations import conversation_middleware

bot.use(conversation_middleware)
```

---

## `PluginState`

Enum representing the state of a loaded plugin.

| Value | Description |
|---|---|
| `PluginState.LOADED` | Plugin is currently loaded and active |
| `PluginState.UNLOADED` | Plugin has been unloaded |
| `PluginState.ERROR` | Plugin failed to load or reload |

---

## `PluginRecord`

Metadata and state for a loaded plugin.

| Property | Type | Description |
|---|---|---|
| `name` | `str` | Plugin name (`PLUGIN_NAME`) |
| `version` | `str` | Plugin version (`PLUGIN_VERSION`) |
| `description` | `str` | Plugin description (`PLUGIN_DESCRIPTION`) |
| `state` | `PluginState` | Current state of the plugin |
| `file_path` | `str` | Path to the plugin file |
| `router` | `Router` | The plugin's isolated router |

---

## `PluginManagerTexts`

Customizable text strings for plugin admin commands. Allows localization of admin command messages.

```python
from grathon.high_level.plugin_manager import PluginManagerTexts

texts = PluginManagerTexts(
    plugins_list="📦 Plugins:",
    plugin_loaded="✅ Plugin loaded: {}",
    plugin_unloaded="❌ Plugin unloaded: {}",
    plugin_reloaded="🔄 Plugin reloaded: {}",
    # ... more customizable strings
)

pm = PluginManager(bot, admin_ids, texts=texts)
```

---

## `BotScheduler`

```python
scheduler = BotScheduler(bot)

@scheduler.cron("0 0 * * 1", name="weekly_task")
async def my_task():
    await db.reset_search_counts()

await scheduler.start()
await scheduler.stop()
```

---

## `SessionStore`

```python
bot.session.set(chat_id, key, value)
value = bot.session.get_value(chat_id, key, default=None)
bot.session.delete(chat_id, key)
```

---

## `CallbackStore`

```python
# Register large callback data, get short alias
alias = CallbackStore.register("very long callback data...")
# Resolve alias back to original data
resolved = CallbackStore.resolve(alias)
```

---

## `ConversationStore`

```python
from grathon.high_level.conversations import ConversationStore

# Register a waiting message
loop = asyncio.get_running_loop()
future = loop.create_future()
ConversationStore.register_message(chat_id, user_id, future)

# Wait for the message
msg_ctx = await asyncio.wait_for(future, timeout=120)

# Cancel a waiting conversation
ConversationStore.cancel_message(chat_id, user_id)
ConversationStore.clear(chat_id, user_id)
```

---

## `FileHelper`

```python
from grathon.high_level.helpers.files import FileHelper

# Send file by local path
await FileHelper.send_file(ctx, "/path/to/file.pdf", "Caption", "document")

# Download file by TDLib file_id
path = await FileHelper.download_file(ctx, file_id, "/tmp/output.pdf")
```

---

## `TextFormatter`

```python
from grathon.high_level.helpers.formatted_text import TextFormatter

formatter = TextFormatter(client)
html_text = await formatter.html("<b>Bold</b> and <i>italic</i>")
md_text = await formatter.markdown("**Bold** and __italic__")
```

---

## `ErrorHandler`

```python
bot.error_handler()
async def handle_error(error, ctx):
    await ctx.reply(f"Error: {error}")
```

---

## `Retry Middleware`

```python
from grathon.high_level.middlewares.retry import retry_middleware, auto_retry, FloodWaitError

bot.use(retry_middleware(max_retries=3, base_delay=1.0))
```

---

## `RateLimitManager`

Per-user rate limiting helper for tracking message frequency.

### Installation

```python
from grathon.high_level.helpers.rate_limit_manager import RateLimitManager, RateLimitEvent, install_rate_limit_manager

install_rate_limit_manager(bot._client)
```

### Usage

```python
# Check if a user is rate-limited
event = RateLimitManager.check(user_id, limit=5, period=60)
if event.blocked:
    await ctx.reply("Slow down!")
    return
```

### Properties

| Property | Type | Description |
|---|---|---|
| `blocked` | `bool` | Whether the user is currently rate-limited |
| `count` | `int` | Number of events in the current period |
| `remaining` | `int` | Remaining allowed events |
| `reset_in` | `float` | Seconds until the rate limit resets |

---

## `KeyboardBuilder` — Advanced

### `close_button(text, closing_message)`

Add an auto-close button that deletes the message after a delay:

```python
kb.close_button("❌ Close", closing_message="This message will be deleted")
```

---

## `FileHelper`

### `send_file(ctx, file_path, caption, file_type)`

Send a file by local path with automatic content type detection.

### `download_file(ctx, file_id, output_path)`

Download a file from Telegram by TDLib file_id.

---

## `TextFormatter`

```python
from grathon.high_level.helpers.formatted_text import TextFormatter

formatter = TextFormatter(client)
html_text = await formatter.html("<b>Bold</b> and <i>italic</i>")
md_text = await formatter.markdown("**Bold** and __italic__")
```

---

## `PaginationHelper`

```python
from grathon.high_level.helpers.pagination import PaginationHelper

pagination = PaginationHelper(items, page_size=10)
page = pagination.get_page(current_page)
```

---

## `InputValidator`

```python
from grathon.high_level.helpers.validation import InputValidator

validator = InputValidator()
is_valid = validator.validate_email(user_input)
```

---

## `InlineQueryResultBuilder`

Fluent builder for inline query results.

### Constructor

```python
from grathon.high_level.inline_query_builder import InlineQueryResultBuilder

builder = InlineQueryResultBuilder()
```

### Methods

| Method | Returns | Description |
|---|---|---|
| `article(title, description, input_message_content, reply_markup=None)` | `InlineQueryResultBuilder` | Add an article result |
| `photo(title, photo_url, thumbnail_url, caption=None, reply_markup=None)` | `InlineQueryResultBuilder` | Add a photo result |
| `video(title, video_url, mime_type, thumbnail_url, caption=None, reply_markup=None)` | `InlineQueryResultBuilder` | Add a video result |
| `audio(title, audio_url, mime_type, thumbnail_url, caption=None, reply_markup=None)` | `InlineQueryResultBuilder` | Add an audio result |
| `document(title, document_url, mime_type, thumbnail_url, caption=None, reply_markup=None)` | `InlineQueryResultBuilder` | Add a document result |
| `voice_note(title, voice_note_url, mime_type, thumbnail_url, caption=None, reply_markup=None)` | `InlineQueryResultBuilder` | Add a voice note result |
| `animation(title, animation_url, mime_type, thumbnail_url, caption=None, reply_markup=None)` | `InlineQueryResultBuilder` | Add an animation result |
| `contact(title, phone_number, first_name, last_name=None, reply_markup=None)` | `InlineQueryResultBuilder` | Add a contact result |
| `location(title, latitude, longitude, reply_markup=None)` | `InlineQueryResultBuilder` | Add a location result |
| `venue(title, latitude, longitude, address, foursquare_id=None, reply_markup=None)` | `InlineQueryResultBuilder` | Add a venue result |
| `sticker(sticker_url, mime_type, reply_markup=None)` | `InlineQueryResultBuilder` | Add a sticker result |
| `game(game_short_name, reply_markup=None)` | `InlineQueryResultBuilder` | Add a game result |
| `row()` | `InlineQueryResultBuilder` | Start a new row |
| `build()` | `list[InputInlineQueryResult]` | Build final list of results |

### Usage

```python
from grathon.high_level import InlineQueryResultBuilder

@bot.on_inline_query()
async def inline_search(ctx):
    builder = InlineQueryResultBuilder()
    builder.article("Result 1", "Description", input_message_content="You chose 1")
    builder.article("Result 2", "Description", input_message_content="You chose 2")
    await ctx.answer_results(builder.build())
```

---

## `auto_handle_close_button`

Convenience function to install an auto-close button handler on a context.

```python
from grathon.high_level.close_button_handler import auto_handle_close_button

# Auto-close button handler for callback queries
@bot.on_callback(r"^close$")
async def close_handler(ctx):
    await auto_handle_close_button(ctx)
```

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `ctx` | `CallbackQueryCtx` | The callback query context |

### Returns

`bool` — `True` if the close button was handled, `False` otherwise.

---

## Built-in Routers

### `AuthRouter`

Handles TDLib authentication flow automatically. Manages the `updateAuthorizationState` events including:
- `authWaitTdlibParameters` — sends `setTdlibParameters`
- `authWaitAuthenticationToken` — sends `checkAuthenticationBotToken`
- `authReady` — authentication complete

### `NewMessageRouter`

Routes `updateNewMessage` events. Handlers registered via `@bot.on_message()` are added to this router.

### `CallbackQueryRouter`

Routes `updateNewCallbackQuery` events. Handlers registered via `@bot.on_callback()` are added to this router.

### `InlineQueryRouter`

Routes `updateNewInlineQuery` events. Handlers registered via `@bot.on_inline_query()` are added to this router.

### `DownloadMonitorRouter`

Monitors file download progress events (`updateFile`). Useful for tracking download/upload status.

---

## Error Classes

### `TDLibError`

Base exception for TDLib-related errors. Raised when TDLib returns an error response.

### `SendMessageException`

Exception raised when a message fails to send. Contains details about the failure.

---

## `SearchResult`

Result object returned by `global_search()` for search queries across Telegram.

| Property | Type | Description |
|---|---|---|
| `query` | `str` | The search query |
| `results` | `list` | List of search result items |
| `total_count` | `int` | Total number of matching results |
| `next_offset` | `str` | Offset for pagination of results |

---

## Scheduler Classes

### `JobData`

Data class representing a scheduled job.

| Field | Type | Description |
|---|---|---|
| `job_id` | `str` | Unique job identifier |
| `name` | `str` | Human-readable job name |
| `trigger` | `str` | Cron expression or trigger type |
| `trigger_args` | `dict` | Arguments passed to the trigger |
| `status` | `JobStatus` | Current job status |
| `created_at` | `str` | ISO timestamp of creation |
| `last_run` | `str \| None` | ISO timestamp of last run |
| `next_run` | `str \| None` | ISO timestamp of next scheduled run |
| `error_count` | `int` | Number of consecutive errors |
| `last_error` | `str \| None` | Last error message |

### `JobStatus`

Enum representing the status of a scheduled job.

| Value | Description |
|---|---|
| `JobStatus.ACTIVE` | Job is scheduled and will run |
| `JobStatus.PAUSED` | Job is paused |
| `JobStatus.FAILED` | Job failed |
| `JobStatus.COMPLETED` | Job completed (one-shot) |

### `TriggerType`

Enum representing the type of job trigger (e.g., cron, interval, one-shot).

### `JobTransfer`

Abstract base class for job storage backends. Implement this to persist jobs across restarts.

### `InMemoryJobTransfer`

In-memory job storage backend. Jobs are lost on restart.

### `PicoDBJobTransfer`

Persistent job storage backend using PicoDB (AsyncPicodoPG). Jobs survive bot restarts.

```python
from picodb import AsyncPicodb
from grathon.high_level.scheduler.picodb_transfer import PicoDBJobTransfer
from grathon.high_level.scheduler import BotScheduler

db = AsyncPicodb(schema_cls=JobRecord, path="sqlite+aiosqlite:///bot_jobs.db")
await db.init_db()

scheduler = BotScheduler(bot, transfer=PicoDBJobTransfer(db))
```