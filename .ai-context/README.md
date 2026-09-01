# Grathon — Telegram Bot Framework (TDLib)

Grathon is a Python framework for building Telegram bots on top of **TDLib** (via `tdjson`).
It wraps the raw TDLib C++ library with a clean, async Python API and a plugin-based architecture.

## Why Grathon?

- **Full Telegram access** — TDLib gives access to every Telegram feature (forwarding, file download, media editing, etc.) that the Bot API cannot provide.
- **Async-first** — Built on `asyncio` from the ground up.
- **Plugin system** — Load, unload, reload plugins at runtime without restarting the bot.
- **Filter DSL** — Declarative, composable filters (`&`, `|`, `~`) for event matching.
- **Type-safe** — Uses generated TDLib type stubs (`tltypes`, `tlmethods`).

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

## Running the Bot

The following pattern is used in production projects (Babone, FileHolder). It covers the full lifecycle: setup, middleware installation, plugin loading, scheduling, and graceful shutdown.

### Minimal `main.py`

```python
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "libs"))

from grathon import GrathonBot
from grathon.high_level import PluginManager
from grathon.high_level.helpers.message_send_middleware import install_message_send_middleware
from grathon.high_level.helpers.rate_limit_manager import install_rate_limit_manager


async def main():
    bot = GrathonBot(
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=config.BOT_TOKEN,
        database_directory="bot_db",
    )

    # Install middleware to track message send status
    install_message_send_middleware(bot._client)

    # Install rate limiter (optional but recommended)
    install_rate_limit_manager(bot._client)

    # Initialize plugin manager (auto-loads ./plugins)
    plugin_manager = PluginManager(
        target=bot,
        admin_ids=config.ADMINS,
        plugin_dir=str(ROOT / "plugins"),
    )

    print("🚀 Bot starting...")

    runner = asyncio.create_task(bot.start())

    try:
        await bot.api.set_log_verbosity_level(0)
        await runner
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\n⏹️ Shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        try:
            runner.cancel()
        except asyncio.CancelledError:
            pass
        await bot.stop()
        print("✓ Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())
```

### With Scheduler

```python
from grathon.high_level.scheduler import BotScheduler

async def main():
    bot = GrathonBot(...)
    install_message_send_middleware(bot._client)
    install_rate_limit_manager(bot._client)

    plugin_manager = PluginManager(target=bot, admin_ids=config.ADMINS)

    scheduler = BotScheduler(bot)

    @scheduler.cron("0 0 * * 1", name="weekly_reset")
    async def weekly_reset():
        await db.reset_search_counts()

    await scheduler.start()

    runner = asyncio.create_task(bot.start())
    # ... same try/except/finally as above
```

### With Database (PicoDB / PostgreSQL)

```python
from db.manager import db

async def main():
    await db.init()
    await db.load_admins()

    bot = GrathonBot(...)
    install_message_send_middleware(bot._client)
    install_rate_limit_manager(bot._client)

    plugin_manager = PluginManager(target=bot, admin_ids=config.ADMINS)

    runner = asyncio.create_task(bot.start())
    # ... same try/except/finally as above, plus db.close() in finally
```

### Graceful Shutdown Order

Always shut down in this order to avoid data loss:

1. Cancel the `bot.start()` runner task
2. Call `await bot.stop()` — closes TDLib connection
3. Call `await scheduler.stop()` — stops scheduled tasks
4. Call `await db.close()` — closes database connections

## Project Structure

```
libs/grathon/
├── __init__.py                  # Public exports (GrathonBot, F, RateLimitManager, etc.)
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
│   │   └── SendMessageException.py
│   ├── functions/               # TDLib API function wrappers
│   │   ├── __init__.py
│   │   ├── send_message.py
│   │   ├── edit_message.py
│   │   ├── delete_message.py
│   │   ├── forward_message.py
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
    ├── callback_store.py        # CallbackStore — alias/compression for large callback data
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
        ├── message_send_middleware.py  # Tracks message send status
        ├── message_tracker.py   # Tracks sent messages
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
| `ConversationStore` | Multi-step conversation state management |
| `KeyboardBuilder` | Fluent builder for inline keyboards |
| `CallbackStore` | Compresses large callback data (>64 bytes) via zlib+base64 |
| `RateLimitManager` | Per-user rate limiting for message frequency control |
| `BotScheduler` | Cron-based background task scheduling |
| `FileHelper` | Send/download files by path or TDLib file_id |
| `TextFormatter` | Convert Markdown/HTML to TDLib `formattedText` |
| `SessionStore` | Per-chat key-value storage for user state |

## Installation

```bash
pip install tdjson>=1.8.66
```

Or add to your project via `pyproject.toml`:

```toml
dependencies = [
    "tdjson>=1.8.66",
    "grathon @ file:///path/to/libs/grathon",
]
```

## TDLib Schema

The file `core/TLSchema_Manager/td_api.tl.txt` must match the installed `tdjson` version.
To regenerate `tltypes.py` and `tlmethods.py`, run `app.py` in the TLSchema_Manager directory.