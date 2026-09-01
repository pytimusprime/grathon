# Grathon — Usage Examples

Practical examples showing how to use the Grathon framework for building Telegram bots.

## 1. Basic Bot Setup

```python
from grathon import GrathonBot, F

bot = GrathonBot(
    api_id=12345,
    api_hash="your_api_hash",
    bot_token="your_bot_token",
)

@bot.on_command("start")
async def start(ctx):
    await ctx.reply("Welcome!")

await bot.start()
```

## 2. Command Handler with Filters

```python
@bot.on_command("help")
async def help_cmd(ctx):
    await ctx.reply("Available commands:\n/start - Start the bot\n/help - Show this message")

@bot.on_command("settings")
async def settings(ctx):
    await ctx.reply("Settings page here")
```

## 3. Message Filtering with `F`

```python
from grathon import F

# Match text messages only
@bot.on_message(filters=[F.text()])
async def handle_text(ctx):
    await ctx.reply(f"You said: {ctx.text}")

# Match commands from private chats only
@bot.on_message(filters=[F.command("admin") & F.private()])
async def admin_cmd(ctx):
    await ctx.reply("Admin command")

# Match messages from specific users
@bot.on_message(filters=[F.from_user(12345)])
async def specific_user(ctx):
    await ctx.reply("Hello, special user!")

# Match messages containing a keyword
@bot.on_message(filters=[F.contains("hello", case_sensitive=False)])
async def hello_handler(ctx):
    await ctx.reply("Hi there!")
```

## 4. Callback Query Handler

```python
@bot.on_callback(r"^action_(.+)$")
async def handle_action(ctx):
    if not ctx.match:
        return
    action_id = ctx.match.group(1)
    await ctx.answer(f"Action: {action_id}")
    await ctx.edit_message(text=f"Performed action: {action_id}")
```

## 5. Inline Keyboard Builder

```python
from grathon.high_level import KeyboardBuilder

kb = KeyboardBuilder()
kb.button("Option A", {"action": "a"})
kb.button("Option B", {"action": "b"})
kb.row()
kb.button("Cancel", {"action": "cancel"})

await ctx.reply("Choose an option:", reply_markup=kb.build())
```

## 6. Sending Files

```python
# Send a file by local path
await ctx.reply(file="/path/to/document.pdf", file_type="document", caption="Here is the file")

# Send a photo
await ctx.reply(file="/path/to/photo.jpg", file_type="photo", caption="Check this out")

# Download a file from Telegram
path = await bot.download_file(file_id, "/tmp/downloaded.pdf")
```

## 7. Plugin Development

```python
# plugins/hello/__init__.py
PLUGIN_NAME = "hello"
PLUGIN_VERSION = "1.0.0"
PLUGIN_DESCRIPTION = "A simple hello plugin"

def setup(router):
    from grathon.high_level import F
    from grathon.core.TLSchema_Manager.tltypes import updateNewMessage

    @router.on(updateNewMessage, filters=[F.command("hello")])
    async def hello(ctx):
        await ctx.reply("Hello from plugin!")
```

## 8. Middleware Usage

```python
from grathon.high_level.middlewares.retry import retry_middleware

bot.use(retry_middleware(max_retries=3, base_delay=1.0))
```

## 9. Error Handling

```python
@bot.error_handler()
async def handle_error(error, ctx):
    if ctx:
        await ctx.reply(f"⚠️ An error occurred: {type(error).__name__}")
```

## 10. Rate Limiting

```python
@bot.on_message(filters=[F.command("spam") & F.rate_limit(3, 60)])
async def limited_cmd(ctx):
    await ctx.reply("Slow down!")
```

## 11. Session Management

```python
# Store data per chat
bot.session.set(chat_id, "last_action", "search")
value = bot.session.get_value(chat_id, "last_action", default=None)
bot.session.delete(chat_id, "last_action")
```

## 12. Scheduled Tasks

```python
from grathon.high_level.scheduler import BotScheduler

scheduler = BotScheduler(bot)

@scheduler.cron("0 9 * * *", name="daily_greeting")
async def daily_greeting():
    await bot.send_file(chat_id, "/path/to/greeting.pdf", caption="Good morning!")

await scheduler.start()
```

## 13. Sending Media with TDLib

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

## 14. Editing Messages

```python
# Edit text message
await ctx.edit_message(text="Updated text")

# Edit media caption (use this for photos/videos)
await ctx.edit_message_caption(text="New caption")

# Delete a message
await ctx.delete_message()
```