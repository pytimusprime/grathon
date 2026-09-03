# Grathon — Python Telegram Bot Framework (TDLib)

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

## Documentation

The `.ai-context/` directory contains the **authoritative, up-to-date documentation** for the Grathon framework. It is maintained alongside the source code and reflects the current state of the project. Do not rely on scattered README files or inline comments alone.

### Reading Order

1. [`.ai-context/README.md`](https://github.com/pytimusprime/grathon/blob/master/.ai-context/README.md) — Project overview, structure, and key concepts
2. [`.ai-context/API.md`](https://github.com/pytimusprime/grathon/blob/master/.ai-context/API.md) — Full API reference for all classes and methods
3. [`.ai-context/ARCHITECTURE.md`](https://github.com/pytimusprime/grathon/blob/master/.ai-context/ARCHITECTURE.md) — Architecture layers and data flow
4. [`.ai-context/RULES.md`](https://github.com/pytimusprime/grathon/blob/master/.ai-context/RULES.md) — Coding rules and conventions (must follow)
5. [`.ai-context/FAQ.md`](https://github.com/pytimusprime/grathon/blob/master/.ai-context/FAQ.md) — Common questions and troubleshooting
6. [`.ai-context/EXAMPLES.md`](https://github.com/pytimusprime/grathon/blob/master/.ai-context/EXAMPLES.md) — Usage examples

## Running the Bot

> **IMPORTANT**: The `await bot.start()` pattern in Quick Start is only for quick testing.
> For production use, you **MUST** use `asyncio.create_task(bot.start())` as a background
> runner, then `await runner` to block until shutdown. See the full pattern below.

### Correct `main.py` Pattern

```python
"""Your Bot — main entry point."""
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "libs"))  # if using local libs

import config
from grathon import GrathonBot
from grathon.high_level import PluginManager
from grathon.high_level.helpers.message_send_middleware import install_message_send_middleware
from grathon.high_level.helpers.rate_limit_manager import install_rate_limit_manager, RateLimitManager
from db.manager import db
from plugins import load_plugins

async def main():
    if not config.validate_config():
        print("\n❌ Invalid configuration. Check your .env file.")
        sys.exit(1)

    await db.init()

    bot = GrathonBot(
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=config.BOT_TOKEN,
        database_directory="bot_db",
    )

    # Required: install message send middleware for wait_for_confirmation
    install_message_send_middleware(bot._client)
    install_rate_limit_manager(bot._client)
    RateLimitManager.get_instance()._min_interval = 2.5

    # Setup plugins
    plugin_manager = PluginManager(
        target=bot,
        admin_ids=[config.SUDO] + list(config.ADMINS),
        plugin_dir=str(ROOT / "plugins"),
    )
    load_plugins(bot, plugin_manager)

    print("🚀 Bot starting...")

    # ⭐ CRITICAL: Use asyncio.create_task, NOT await bot.start()
    # bot.start() is an infinite coroutine — it never returns.
    # create_task runs it in the background so we can do other work
    # (like get_me() with retry) before blocking on it.
    runner = asyncio.create_task(bot.start())

    # Fetch bot info with retry — TDLib may not be initialized yet
    try:
        for _ in range(20):
            try:
                me = await bot.api.get_me()
                break
            except Exception:
                await asyncio.sleep(0.5)
        else:
            me = await bot.api.get_me()

        username = ""
        if hasattr(me, 'usernames') and me.usernames and me.usernames.active_usernames:
            username = me.usernames.active_usernames[0]
        elif hasattr(me, 'username') and me.username:
            username = me.username
        if username:
            config.BOT_USERNAME = username
            print(f"[BOT INFO] Bot username: {username}")
        if hasattr(me, 'id') and me.id:
            config.BOT_USER_ID = me.id
            print(f"[BOT INFO] Bot user_id: {me.id}")
    except Exception as e:
        print(f"[BOT WARN] Could not fetch bot info: {e}")

    # Block until interrupted (Ctrl+C)
    try:
        await bot.api.set_log_verbosity_level(0)
        await runner
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\n\n Shutting down...")
    except Exception as e:
        print(f"\n Error: {e}")
    finally:
        # Graceful shutdown: 3 steps
        runner.cancel()      # 1. Cancel the runner task
        await bot.stop()     # 2. Stop TDLib client (closes all tasks + api.close())
        await db.close()     # 3. Close database connections
        print("Goodbye!")

if __name__ == "__main__":
    asyncio.run(main())
```

### Why `asyncio.create_task(bot.start())`?

| Pattern | Behavior | Use Case |
|---|---|---|
| `await bot.start()` | Blocks forever — never returns | Quick testing only |
| `runner = asyncio.create_task(bot.start())` then `await runner` | Runs in background, then blocks | **Production** — allows `get_me()` with retry before blocking |

`bot.start()` internally calls `TdClient.run_forever()` which runs two infinite loops
(`process_update_queue_loop` and `process_extra_queue_loop`) via `asyncio.gather`.
This never returns on its own — it only stops when cancelled.

### TDLib Initialization Flow (inside `runner`)

When `runner` starts, it triggers TDLib's authentication state machine:

```
authorizationStateWaitTdlibParameters
  → set_tdlib_parameters(api_id, api_hash, database_directory, ...)
authorizationStateWaitPhoneNumber
  → check_authentication_bot_token(bot_token)
authorizationStateReady  ✅
  → Bot is ready to send/receive messages
```

This happens asynchronously in the background while `runner` is running.
That's why `get_me()` needs a retry loop — TDLib may not be ready yet.

### Graceful Shutdown

```python
finally:
    runner.cancel()      # Cancel the runner task (triggers CancelledError in runner)
    await bot.stop()     # TdClient.stop() — cancels all tasks, closes TDLib
    await db.close()     # Close database connections
```

## Database

Grathon works with **PicoDB** (available separately at [github.com/pytimusprime/picodb](https://github.com/pytimusprime/picodb)) which supports both SQLite and PostgreSQL.

## License

MIT