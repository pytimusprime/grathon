# Grathon — Telegram Bot Framework (TDLib)

Grathon is a Python framework for building Telegram bots on top of **TDLib** (via `tdjson`).
It wraps the raw TDLib C++ library with a clean, async Python API and a plugin-based architecture.

## Why Grathon?

- **Full Telegram access** — TDLib gives access to every Telegram feature (forwarding, file download, media editing, etc.) that the Bot API cannot provide.
- **Async-first** — Built on `asyncio` from the ground up.
- **Plugin system** — Load, unload, reload plugins at runtime without restarting the bot.
- **Filter DSL** — Declarative, composable filters (`&`, `|`, `~`) for event matching.
- **Type-safe** — Uses generated TDLib type stubs (`tltypes`, `tlmethods`).
- **Send confirmation** — Automatic tracking of pending → final message IDs via `MessageTracker`.
- **FloodWait handling** — Built-in `FloodWaitException` for retry logic.

## Quick Start

```python
from grathon import GrathonBot, F

bot = GrathonBot(
    api_id=12345,
    api_hash="your_api_hash",
    bot_token="your_bot_token",
)

@bot.on_command("start")
async def start(ctx):
    await ctx.reply("Hello!")

@bot.on_callback(r"^confirm$")
async def confirm(ctx):
    await ctx.answer("Confirmed!")

await bot.start()
```

## Installation

```bash
pip install tdjson>=1.8.66
pip install grathon @ git+https://github.com/pytimusprime/grathon.git
```

## Running the Bot

See the "Running the Bot" section in `.ai-context/README.md` for the full `main.py` pattern including middleware installation, plugin manager setup, scheduler, and graceful shutdown.

## Project Structure

```
grathon/
├── __init__.py                  # Public exports (GrathonBot, F, RateLimitManager, FloodWaitException, etc.)
├── grathon_bot.py               # GrathonBot — user-facing entry point
├── cli.py                       # CLI tool
├── core/
│   ├── tdclient.py              # TdClient — low-level TDLib client
│   ├── clientmanager.py         # ClientManager — routes updates to clients
│   ├── router.py                # Router — handler registry
│   ├── eventhandler.py          # EventHandler — filter + callback wrapper
│   ├── middleware.py            # Middleware pipeline (onion pattern)
│   ├── transport.py             # ITdTransport protocol (abstract)
│   ├── transport_tdjson.py      # TdjsonTransport — real tdjson impl
│   ├── transport_mock.py        # Mock transport for testing
│   ├── contexts/                # Context classes per update type
│   │   ├── __init__.py
│   │   ├── context.py           # Base Context
│   │   ├── NewMessageCtx.py     # Context for new messages
│   │   ├── CallbackQueryCtx.py  # Context for callback queries
│   │   └── InlineQueryCtx.py    # Context for inline queries
│   ├── errors/                  # Error classes
│   │   ├── __init__.py
│   │   ├── TDLibError.py
│   │   ├── SendMessageException.py
│   │   └── FloodWaitException.py
│   ├── functions/               # TDLib API function wrappers
│   │   ├── __init__.py
│   │   ├── send_message.py      # send_message_base with wait_for_confirmation
│   │   ├── edit_message.py
│   │   ├── delete_message.py
│   │   ├── forward_message.py   # forward_messages with wait_for_confirmation
│   │   └── global_search.py
│   ├── routers/                 # Built-in routers (auth, callback, inline, newmessage, download_monitor)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── callback_query.py
│   │   ├── inline_query.py
│   │   ├── newmessage.py
│   │   └── download_monitor.py
│   └── TLSchema_Manager/        # Generated TDLib types & methods
│       ├── tltypes.py
│       ├── tlmethods.py
│       ├── app.py
│       └── td_api.tl.txt
└── high_level/
    ├── __init__.py              # Public exports (KeyboardBuilder, F, PluginManager, etc.)
    ├── filters.py               # F — Filter DSL (F.command, F.from_user, etc.)
    ├── keyboards.py             # KeyboardBuilder — fluent inline keyboard builder
    ├── plugin_manager.py        # PluginManager — dynamic plugin lifecycle
    ├── conversations.py         # ConversationStore — multi-step conversations
    ├── callback_db.py           # CallbackDB — SQLite-backed short key storage
    ├── callback_store.py        # CallbackStore — legacy zlib+base64 compression
    ├── session.py               # SessionStore — per-chat session data
    ├── error_handler.py         # ErrorHandler — centralized error handling
    ├── inline_query_builder.py  # Inline query result builder
    ├── close_button_handler.py  # Auto-close button handler
    ├── scheduler/               # BotScheduler — cron-based scheduling
    │   ├── __init__.py
    │   ├── scheduler.py
    │   ├── job_data.py
    │   ├── job_transfer.py
    │   ├── memory_transfer.py
    │   ├── picodb_transfer.py
    │   └── README.md
    ├── middlewares/             # Built-in middlewares
    │   └── retry.py
    └── helpers/                 # Utility helpers
        ├── __init__.py
        ├── files.py             # FileHelper — send/download files
        ├── formatted_text.py    # TextFormatter — markdown/html → formattedText
        ├── message_send_middleware.py  # Tracks message send status (pending → final)
        ├── message_tracker.py   # Tracks sent messages (pending → final ID correlation)
        ├── rate_limit_manager.py      # RateLimitManager — per-user rate limiting
        ├── auto_download_manager.py   # Auto-download manager
        ├── connection_monitor.py      # Connection state monitor
        ├── debug_middleware.py        # Debug logging middleware
        ├── file_optimizer.py          # File optimization settings
        ├── pagination.py              # Pagination helper
        ├── validation.py              # Input validation
        └── iterators.py               # Async iterators
```

## Key Concepts

| Concept | Description |
|---|---|
| `GrathonBot` | High-level bot class with decorator-based handler registration |
| `TdClient` | Low-level TDLib client; routes updates to handlers |
| `Router` | Registry of handlers; can be nested (sub-routers) |
| `EventHandler` | Wraps an event type + filter(s) + callback |
| `F` | Filter builder namespace (`F.command`, `F.from_user`, `F.callback`, etc.) |
| `Context` | Base context object passed to every handler |
| `CallbackQueryCtx` | Context for inline button clicks |
| `NewMessageCtx` | Context for new messages |
| `PluginManager` | Dynamic plugin loading/unloading/reloading |
| `ConversationStore` | Multi-step conversations using `asyncio.Future` |
| `KeyboardBuilder` | Fluent builder for inline keyboards |
| `CallbackDB` | SQLite-backed short key storage for large callback data |
| `CallbackStore` | Legacy zlib+base64 compression for large callback data |
| `RateLimitManager` | Per-user rate limiting for message frequency control |
| `BotScheduler` | Cron-based background task scheduling |
| `FileHelper` | Send/download files by path or TDLib file_id |
| `TextFormatter` | Convert Markdown/HTML to TDLib `formattedText` |
| `SessionStore` | Per-chat key-value storage for user state |
| `MessageTracker` | Tracks pending messages and correlates with final IDs |
| `FloodWaitException` | Raised when send fails due to flood wait (includes `retry_after`) |

## Database

Grathon works with **PicoDB** (available separately at [github.com/pytimusprime/picodb](https://github.com/pytimusprime/picodb)) which supports both SQLite and PostgreSQL.

## License

MIT
