# Grathon — Python Telegram Bot Framework (TDLib)

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

## Installation

```bash
pip install tdjson>=1.8.66
pip install grathon @ git+https://github.com/pytimusprime/grathon.git
```

## Documentation

See the `.ai-context/` directory for comprehensive project documentation.

## License

MIT
