# Grathon — Coding Rules & Conventions

## Overview

These rules define how to write code that works correctly with the Grathon framework. Violating these rules will cause bugs, crashes, or unexpected behavior.

---

## 1. Context Access Rules

### Use `ctx.match` on callback queries

`CallbackQueryCtx` exposes a `match` property with the `re.Match` object when `F.callback(pattern)` is used:

```python
# ✅ CORRECT
@bot.on_callback(r"^my_action_(.+)$")
async def handler(ctx):
    if not ctx.match:
        return
    value = ctx.match.group(1)
```

### NEVER use `ctx.sender_id.user_id` on callback queries

`CallbackQueryCtx` has `sender_user_id` (not `sender_id`). Use `ctx.user_id` or `ctx.sender_user_id`:

```python
# ❌ WRONG
uid = ctx.sender_id.user_id

# ✅ CORRECT
uid = ctx.sender_user_id  # or ctx.user_id
```

### NEVER use `ctx.replied` — always use `ctx.get_replied_message()`

```python
# ❌ WRONG
replied = ctx.replied

# ✅ CORRECT
replied = await ctx.get_replied_message()
```

### NEVER use `ctx.is_group` — use `F.group()` filter

```python
# ❌ WRONG
if ctx.is_group:
    ...

# ✅ CORRECT
@bot.on_message(filters=[F.command("cmd") & F.group()])
async def handler(ctx):
    ...
```

---

## 2. Media Message Editing Rules

### ALWAYS use `edit_message_caption` for media messages

`edit_message_text` / `edit_message` will fail with "There is no text in the message to edit" when the message contains media (photo, video, etc.). Use `edit_message_caption` instead:

```python
# ❌ WRONG — fails on photos/videos
await ctx.edit_message(text="New caption")

# ✅ CORRECT — works on all message types
await ctx.edit_message_caption(text="New caption")
```

### ALWAYS check message type before editing

When editing a message that might be text or media, use the pattern from `CallbackQueryCtx.edit_message()` — it automatically detects media and uses `edit_message_caption` when needed.

---

## 3. File Sending Rules

### ALWAYS use the correct `inputMessage*` structure for TDLib

The new TDLib schema requires wrapping file references in `inputPhoto`, `inputVideo`, etc.:

```python
# ✅ CORRECT — sending a photo
inputMessagePhoto(
    photo=inputPhoto(
        photo=inputFileLocal(path=file_path),
        width=1,
        height=1,
    ),
    caption=formattedText(text="Caption", entities=[]),
    has_spoiler=False,
)

# ✅ CORRECT — sending a video
inputMessageVideo(
    video=inputVideo(
        video=inputFileLocal(path=file_path),
        duration=0,
        width=0,
        height=0,
    ),
    caption=formattedText(text="Caption", entities=[]),
)

# ❌ WRONG — passing inputFileLocal directly
inputMessagePhoto(photo=inputFileLocal(path=file_path))
```

### ALWAYS use `FileHelper.send_file()` for sending files by path

```python
from grathon.high_level.helpers.files import FileHelper

await FileHelper.send_file(ctx, file_path, caption, file_type)
```

### Use `bot.download_file()` for downloading files by TDLib file_id

```python
path = await bot.download_file(file_id, "/tmp/output.pdf")
```

---

## 4. Filter Rules

### ALWAYS use live admin filters for runtime admin checks

Use `F.from_user` with a callable to read admins dynamically on every update:

```python
# ❌ WRONG — snapshots config.ADMINS at import time
@bot.on_message(filters=[F.from_user(*config.ADMINS)])
async def admin_cmd(ctx):
    ...

# ✅ CORRECT — reads config.ADMINS live on every update
@bot.on_message(filters=[F.command("admin_cmd") & F.from_user(user_ids_fn=lambda: config.ADMINS)])
async def admin_cmd(ctx):
    ...
```

### ALWAYS use `F.callback(pattern)` for inline button matching

```python
# ✅ CORRECT
@bot.on_callback(r"^dl_movie_(.+)$")
async def dl_movie(ctx):
    if not ctx.match:
        return
    value = ctx.match.group(1)
```

### ALWAYS handle `F.callback` match groups in handler

```python
# ✅ CORRECT — extract groups from ctx.match
@bot.on_callback(r"^rate_(movie|series)_(.+)$")
async def rate_handler(ctx):
    if not ctx.match:
        return
    media_type, key = ctx.match.group(1), ctx.match.group(2)
```

---

## 5. Plugin Rules

### Plugins MUST define all required metadata

```python
# ✅ CORRECT
PLUGIN_NAME = "my_plugin"       # lowercase, snake_case only
PLUGIN_VERSION = "1.0.0"
PLUGIN_DESCRIPTION = "Description"

def setup(router):
    ...
```

### Plugins MUST use isolated routers

Each plugin should create its own `Router` instance and register handlers on it:

```python
# ✅ CORRECT — PluginManager creates the router automatically
def setup(router):
    @router.on(updateNewMessage, filters=[F.command("hello")])
    async def hello(ctx):
        await ctx.reply("Hello!")
```

### Plugins MUST NOT import `config` directly for admin checks

Use `F.from_user(user_ids_fn=lambda: config.ADMINS)` for dynamic admin checks instead of importing config directly.

---

## 6. TDLib Schema Rules

### ALWAYS regenerate `tltypes.py` and `tlmethods.py` when upgrading `tdjson`

The `core/TLSchema_Manager/td_api.tl.txt` file must match the installed `tdjson` version. Run `app.py` in the TLSchema_Manager directory to regenerate.

### ALWAYS use the correct TDLib object constructors

```python
# ✅ CORRECT — new schema (inputPhoto wrapping inputFileLocal)
inputMessagePhoto(
    photo=inputPhoto(photo=inputFileLocal(path=path), width=1, height=1),
    caption=formattedText(text="Caption", entities=[]),
    has_spoiler=False,
)

# ❌ WRONG — old schema (passing inputFileLocal directly)
inputMessagePhoto(photo=inputFileLocal(path=path))
```

---

## 7. Callback Data Rules

### ALWAYS keep callback data under 64 bytes

If your callback data exceeds 64 bytes, use `KeyboardBuilder.button()` which auto-compresses via `CallbackStore`:

```python
# ✅ CORRECT — KeyboardBuilder handles compression automatically
kb.button("Long label", {"action": "view", "key": "some_long_access_key", "extra": "data"})
```

### NEVER hardcode callback data strings

Always use constants or generate them programmatically:

```python
# ❌ WRONG
kb.button("View", f"view_movie_{some_key}")

# ✅ CORRECT — use KeyboardBuilder which handles encoding
kb.button("View", f"view_movie_{some_key}")
# (KeyboardBuilder auto-encodes dicts as JSON and compresses if needed)
```

---

## 8. Error Handling Rules

### ALWAYS wrap TDLib API calls in try/except

```python
# ✅ CORRECT
try:
    result = await ctx.api.edit_message_text(...)
except Exception as e:
    # Fallback to caption edit for media messages
    await ctx.edit_message_caption(text="Fallback text")
```

### ALWAYS handle `MESSAGE_NOT_MODIFIED` gracefully

```python
# ✅ CORRECT
try:
    await ctx.edit_message(text=new_text)
except Exception as e:
    if "MESSAGE_NOT_MODIFIED" in str(e):
        pass  # Message already has this text
    else:
        raise
```

### ALWAYS use `ErrorHandler` for centralized error handling

```python
bot.error_handler()
async def handle_error(error, ctx):
    if ctx:
        await ctx.reply(f"⚠️ Error: {type(error).__name__}")
```

---

## 9. Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Plugin names | `snake_case`, lowercase | `movies`, `series`, `admin` |
| Plugin files | `snake_case.py` | `movies/__init__.py` |
| Plugin folders | `snake_case` | `plugins/admin/` |
| Callback patterns | `snake_case_with_prefix` | `dl_movie_{key}`, `view_movie_{key}` |
| Variable names | `snake_case` | `movie`, `series`, `access_key` |
| Function names | `snake_case` | `get_movie`, `add_movie`, `update_movie` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_PER_PAGE`, `DEFAULT_TEMPLATE` |
| Config variables | `UPPER_SNAKE_CASE` | `API_ID`, `BOT_TOKEN`, `SUDO` |

---

## 10. Import Rules

### ALWAYS import from `grathon.high_level` for public API

```python
# ✅ CORRECT
from grathon.high_level import F, KeyboardBuilder

# ❌ WRONG — don't import internal modules directly
from grathon.high_level.filters import F  # OK, but prefer top-level
```

### ALWAYS import TDLib types from `TLSchema_Manager`

```python
# ✅ CORRECT
from grathon.core.TLSchema_Manager.tltypes import (
    updateNewMessage,
    updateNewCallbackQuery,
    inputMessagePhoto,
    inputPhoto,
    inputFileLocal,
    formattedText,
)
```

### NEVER import `config` in plugin files for admin checks

```python
# ❌ WRONG
import config
if ctx.sender_user_id in config.ADMINS:
    ...

# ✅ CORRECT
# Use F.from_user with a callable for dynamic admin checks
@bot.on_message(filters=[F.command("admin_cmd") & F.from_user(user_ids_fn=lambda: config.ADMINS)])
async def admin_cmd(ctx):
    ...
```

---

## 11. Async Rules

### ALWAYS `await` async functions

```python
# ❌ WRONG
some_async_func(key)

# ✅ CORRECT
await some_async_func(key)
```

### NEVER block the event loop

```python
# ❌ WRONG — blocking call in async handler
import time
time.sleep(5)

# ✅ CORRECT — use asyncio.sleep
import asyncio
await asyncio.sleep(5)
```

### ALWAYS handle `asyncio.CancelledError` in long-running operations

```python
try:
    await some_long_operation()
except asyncio.CancelledError:
    # Clean up if needed
    raise  # Re-raise to propagate cancellation
```

---

## 12. Send Confirmation Rules

### ALWAYS use `wait_for_confirmation` when sending messages

When sending messages through `ctx.reply()`, `ctx.forward()`, or `ctx.send_message()`, TDLib returns a temporary (pending) ID immediately and finalizes it later via `updateMessageSendSucceeded`. The framework has a `MessageTracker` + `message_send_middleware` to handle this:

- `wait_for_confirmation=True` (default) → waits for final ID
- `wait_for_confirmation=False` → returns immediately with temp ID

```python
# ✅ CORRECT — wait for final ID (default behavior)
await ctx.reply("Hello!")  # message.id is FINAL

# ✅ CORRECT — explicitly wait
msg = await ctx.reply("Hello!", wait_for_confirmation=True)
# msg.id is FINAL

# ⚠️ Use with caution — temp ID may change
msg = await ctx.reply("Hello!", wait_for_confirmation=False)
# msg.id is TEMPORARY — may not match final Telegram ID
```

### ALWAYS use `wait_for_confirmation` on `CallbackQueryCtx.send_message`

`CallbackQueryCtx.send_message` also supports `wait_for_confirmation` and `confirmation_timeout`:

```python
# ✅ CORRECT
await ctx.send_message("Hello!", wait_for_confirmation=True)
await ctx.send_message("Hello!", confirmation_timeout=10.0)
```

### Install `message_send_middleware` for tracking to work

The `MessageTracker` requires the middleware to be installed:

```python
from grathon.high_level.helpers.message_send_middleware import install_message_send_middleware
install_message_send_middleware(bot._client)
```

### ALWAYS handle `FloodWaitException` for retry logic

When sending fails with a flood wait, `send_message_base` raises `FloodWaitException`:

```python
from grathon.core.errors.FloodWaitException import FloodWaitException

try:
    await ctx.reply("Hello!")
except FloodWaitException as e:
    await asyncio.sleep(e.retry_after)
    await ctx.reply("Hello!")  # retry
```

---

## 13. Testing Rules

### ALWAYS test with real TDLib before deploying

`py_compile` is not sufficient. The project requires a running TDLib native library for real testing.

### ALWAYS add tests for new utility functions

Create test files in `tests/` directory for any new utility function.