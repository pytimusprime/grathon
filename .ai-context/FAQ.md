# Grathon FAQ

## General

### What is Grathon?
Grathon is a Python framework for building Telegram bots on top of TDLib (via `tdjson`). It provides a clean async API, plugin system, filter DSL, and high-level helpers for common bot tasks.

### Why TDLib instead of Bot API?
TDLib gives access to the full Telegram client API, including:
- Forwarding messages (including media)
- Downloading files by TDLib file_id
- Editing message media (not just text)
- Accessing message content types (photo, video, document, etc.)
- Reading messages from any chat the user has access to
- Channel posts, scheduled messages, and more

The Bot API is limited to what a bot can do via the Bot Token. TDLib gives you full client-level access.

### What Python versions are supported?
Python >= 3.13 is required.

### How do I install Grathon?
Grathon is designed to be used as a local library within your project (in `libs/grathon/`). Add `libs/` to your `sys.path` or install it as a package.

```python
import sys
from pathlib import Path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "libs"))
```

## Installation & Setup

### I get `ModuleNotFoundError: No module named 'tdjson'`
Install the `tdjson` Python package:
```bash
pip install tdjson>=1.8.66
```

You also need the native `tdjson` shared library installed on your system. See the [tdjson documentation](https://github.com/tdlib/tdjson) for installation instructions.

### How do I get API_ID and API_HASH?
1. Go to https://my.telegram.org
2. Log in with your phone number
3. Navigate to "API development tools"
4. Create a new application
5. Copy the `api_id` and `api_hash`

### The bot doesn't start — what should I check?
1. Verify `API_ID`, `API_HASH`, and `BOT_TOKEN` are correct in your `.env` or config
2. Verify `tdjson` native library is installed and accessible
3. Run `python -c "import tdjson; print(tdjson.td_create_client_id())"` to test tdjson

## Architecture

### What is the difference between `GrathonBot` and `TdClient`?
- `GrathonBot` is the high-level, user-friendly API with decorators (`@bot.on_command`, `@bot.on_callback`, etc.)
- `TdClient` is the low-level client that handles the TDLib communication, routing, and dispatch
- `GrathonBot` wraps `TdClient` internally — you normally only need `GrathonBot`

### How does the plugin system work?
1. `PluginManager` scans a directory for `.py` files and folders with `__init__.py`
2. Each plugin must define `PLUGIN_NAME`, `PLUGIN_VERSION`, `PLUGIN_DESCRIPTION`, and a `setup(router)` function
3. `setup(router)` registers handlers on an isolated `Router` instance
4. Plugin handlers are added to the client's dispatch list
5. Plugins can be loaded, unloaded, reloaded, and uploaded at runtime via admin commands

### What is the middleware system?
Middleware wraps the entire dispatch pipeline using the **onion pattern**. Each middleware receives `(ctx, next)` and can run code before and/or after calling `next(ctx)`. Middlewares are applied in registration order — the first registered middleware is the outermost.

### How are callback queries routed?
Callback queries (`updateNewCallbackQuery`) are handled by `CallbackQueryRouter`, which is a separate router from the message router. Use `@bot.on_callback(pattern)` to register handlers.

### What is `CallbackStore`?
Telegram limits inline button callback data to 64 bytes. `CallbackStore` transparently handles larger data by:
1. Compressing data with zlib + base64 when registering
2. Storing the compressed alias
3. Resolving aliases back to original data when a callback is received

### How does `F.callback(pattern)` work?
`F.callback(pattern)` creates a `CallbackDataFilter` that:
1. Checks if the context is a `CallbackQueryCtx`
2. Gets the decoded callback data from `ctx.data_str`
3. Resolves any aliases via `CallbackStore`
4. Matches the data against the regex pattern
5. On match, stores the `re.Match` object on `ctx.match`

You can access the regex match directly via `ctx.match` on `CallbackQueryCtx`:

```python
@bot.on_callback(r"^my_action_(.+)$")
async def handler(ctx):
    if not ctx.match:
        return
    value = ctx.match.group(1)
```

## Filters

### How to access regex match groups from `F.callback`?
`CallbackQueryCtx` exposes a `match` property with the `re.Match` object when `F.callback(pattern)` is used:

```python
@bot.on_callback(r"^my_action_(.+)$")
async def handler(ctx):
    if not ctx.match:
        return
    value = ctx.match.group(1)
```

### Why doesn't `ctx.sender_id.user_id` work on callbacks?
On `CallbackQueryCtx`, use `ctx.sender_user_id` or `ctx.user_id` instead:

```python
uid = ctx.sender_user_id  # works on CallbackQueryCtx
# or
uid = ctx.user_id  # unified accessor, works on all context types
```

### Why doesn't `ctx.replied` work?
Use `ctx.get_replied_message()` instead:

```python
replied = await ctx.get_replied_message()
if not replied:
    await ctx.reply("No replied message found.")
    return
```

### Why doesn't `ctx.is_group` exist?
Use the `F.group()` filter on the decorator instead:

```python
@bot.on_message(filters=[F.command("setarchive") & F.group()])
async def set_archive(ctx):
    # This handler only runs in groups
    ...
```

### How do I check if a user is an admin at runtime?
Use `F.from_user` with a callable to read admins dynamically on every update:

```python
@bot.on_message(filters=[F.command("admin_cmd") & F.from_user(user_ids_fn=lambda: config.ADMINS)])
async def admin_cmd(ctx):
    ...
```

This reads `config.ADMINS` live on every update, so runtime changes (like `/add_admin`) are immediately effective.

Do NOT use `F.from_user(*config.ADMINS)` for admin checks — it snapshots the list at decorator evaluation time, so runtime changes won't take effect until plugins are reloaded.

### What is `ctx.data`?

`ctx.data` is a shared dictionary attached to the context object for passing data between filters and handlers:

```python
# Set in a filter
ctx.data["auth_passed"] = True

# Read in a handler
if ctx.data.get("auth_passed"):
    await show_vip_content(ctx)
```

### What is `ctx.session`?

`ctx.session` is per-chat key-value storage that persists across messages:

```python
# Store a value
ctx.session["step"] = 1

# Read a value
step = ctx.session.get("step", 0)
```

## File Handling

### How do I send a file by local path?
```python
await ctx.reply(file="/path/to/file.pdf", file_type="document", caption="Here is the file")
```

### How do I send a file by TDLib file_id?
Use `FileHelper.download_file()` or `bot.download_file()`:

```python
# Download a file by TDLib file_id
path = await bot.download_file(file_id, "/tmp/output.pdf")
```

For sending files by TDLib file_id, use the TDLib API directly via `ctx.api`:

```python
from grathon.core.TLSchema_Manager.tltypes import inputMessageDocument, inputDocument, inputFileId

content = inputMessageDocument(
    document=inputDocument(id=inputFileId(id=file_id)),
    caption=formattedText(text="Caption", entities=[]),
)
```

### How do I download a file?
```python
path = await bot.download_file(file_id, "/tmp/output.pdf")
```

### What is the correct way to send photos with TDLib?
In the new TDLib schema, `inputMessagePhoto` requires `inputPhoto` wrapping:

```python
from grathon.core.TLSchema_Manager.tltypes import (
    inputMessagePhoto, inputPhoto, inputFileLocal, formattedText,
)

content = inputMessagePhoto(
    photo=inputPhoto(
        photo=inputFileLocal(path=file_path),
        width=1,
        height=1,
    ),
    caption=formattedText(text="Caption", entities=[]),
    has_spoiler=False,
)
```

## Plugin Development

### How do I create a plugin?
1. Create a `.py` file or folder in `./plugins/`
2. Define `PLUGIN_NAME`, `PLUGIN_VERSION`, `PLUGIN_DESCRIPTION`
3. Define `setup(router)` function
4. Register handlers using `@router.on(event_type, filters=[...])`
5. Reload the bot or use `/upload` to load the new plugin

### Can plugins import from each other?
Yes. Plugin folders support relative imports (e.g., `from .helpers import x`). The `PluginManager` adds the plugin's directory to `sys.path` so relative imports resolve correctly.

### How do I handle plugin conflicts?
If two plugins register handlers for the same event with the same filters, both will fire. Use specific filters to avoid conflicts.

### Can I hot-reload a plugin?
Yes. Use `/reload <plugin_name>` to reload a single plugin, or `/reload_all` to reload all plugins. The `PluginManager` handles removing old handlers, clearing module cache, and re-importing.

## Database

Grathon itself doesn't include a database layer. It's designed to work with any async database. You can integrate it with PostgreSQL (via asyncpg), SQLite (via aiosqlite), Redis, or any other async database of your choice.

## Performance

### How does Grathon handle concurrent updates?
All handlers run concurrently using `asyncio.create_task()`. The update queue loop never blocks, so new updates are always processed even while handlers are suspended.

### What happens if a handler raises an exception?
The error is caught and routed to `ErrorHandler`. If no error handler is registered, it's logged to the console.

### How can I rate-limit messages?
Use `F.rate_limit(limit, period)`:
```python
@bot.on_message(filters=[F.command("spam") & F.rate_limit(3, 60)])
async def limited_cmd(ctx):
    await ctx.reply("Slow down!")
```

## Troubleshooting

### `TDLib API error: 400 - There is no text in the message to edit`
This happens when you try to `edit_message_text` on a media message (photo, video, etc.). Use `edit_message_caption` instead:

```python
# Wrong — fails on media messages
await ctx.edit_message(text="New text")

# Right — works on all message types
await ctx.edit_message_caption(text="New caption")
```

### `File not found` errors when sending files
Make sure the file path is absolute and the file exists:
```python
import os
path = "/absolute/path/to/file.jpg"
assert os.path.exists(path), f"File not found: {path}"
await ctx.reply(file=path, file_type="photo")
```

### Plugin not loading after upload
Check the plugin's `PLUGIN_NAME` matches the filename (without `.py`). The name must match `^[a-z][a-z0-9_]*$`.

### `messageSendMiddleware` not installed
Install it in `main.py` before creating the `PluginManager`:
```python
from grathon.high_level.helpers.message_send_middleware import install_message_send_middleware
install_message_send_middleware(bot._client)
```