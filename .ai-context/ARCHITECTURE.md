# Grathon Architecture

## Overview

Grathon is a layered architecture that wraps TDLib's C++ client with an async Python API. The design follows a **pipeline** pattern: updates flow from TDLib → transport → client → middleware → router → handler.

```
┌─────────────────────────────────────────────────────────┐
│                    TDLib (C++)                          │
│              tdjson shared library                      │
└──────────────────────┬──────────────────────────────────┘
                       │ td_send / td_receive
                       ▼
┌─────────────────────────────────────────────────────────┐
│               TdjsonTransport                          │
│         (core/transport_tdjson.py)                     │
│  Sends JSON strings to/from tdjson                    │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│               ClientManager                            │
│         (core/clientmanager.py)                        │
│  Single global poll loop (td_receive)                  │
│  Routes updates to correct TdClient by @client_id     │
│  Routes API responses (@extra) back to waiters        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│               TdClient                                 │
│         (core/tdclient.py)                             │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Update Queue (_update_queue)                     │ │
│  │  Extra Queue (_extra_queue)                       │ │
│  └───────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Middleware Chain (_dispatch)                     │ │
│  │  Built via build_chain() (onion pattern)         │ │
│  └───────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Router → Handlers (EventHandler[])              │ │
│  │  include_router() / add_handler() / remove_handler()│ │
│  └───────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Waiters (asyncio.Future for API calls)          │ │
│  └───────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│            Context Objects                             │
│  ┌─────────────┐ ┌──────────────────┐ ┌────────────┐  │
│  │ NewMessageCtx│ │CallbackQueryCtx  │ │InlineQuery │  │
│  └─────────────┘ └──────────────────┘ └────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Layer 1: Transport

**Purpose:** Abstract communication with TDLib.

| Class | File | Description |
|---|---|---|
| `ITdTransport` | `core/transport.py` | Protocol interface (abstract) |
| `TdjsonTransport` | `core/transport_tdjson.py` | Real tdjson implementation |
| (mock) | `core/transport_mock.py` | Mock for testing |

The transport layer is pluggable — you can swap `TdjsonTransport` for a mock in tests.

## Layer 2: Client & Routing

**Purpose:** Manage TDLib client lifecycle and route updates to handlers.

### `ClientManager`

- Single global poll loop calling `tdjson.td_receive()`
- Routes updates to the correct `TdClient` by `@client_id`
- Routes API responses (with `@extra`) to waiting futures

### `TdClient`

- Created per bot instance
- Owns the update queue, extra queue, middleware chain, and handler registry
- `process_update_queue_loop()` — drains updates, constructs context objects, dispatches via middleware chain
- `process_extra_queue_loop()` — resolves API call futures
- `run_forever()` — runs both loops concurrently

### `Router`

- Registry of `EventHandler` instances
- Supports sub-routers (nested routing)
- `include_router()` recursively adds all handlers from sub-routers

### Built-in Routers

| Router | File | Description |
|---|---|---|
| `AuthRouter` | `core/routers/auth.py` | Handles TDLib authentication flow (params, token, ready) |
| `NewMessageRouter` | `core/routers/newmessage.py` | Routes new message updates |
| `CallbackQueryRouter` | `core/routers/callback_query.py` | Routes callback query updates |
| `InlineQueryRouter` | `core/routers/inline_query.py` | Routes inline query updates |
| `DownloadMonitorRouter` | `core/routers/download_monitor.py` | Monitors file download progress |

### `EventHandler`

- Wraps an event type + filter list + callback
- `check_and_execute()` runs all filters, then the callback if all pass
- Errors are routed to `ErrorHandler`

## Layer 3: Context

**Purpose:** Provide a unified interface for handlers to interact with TDLib.

| Context Class | Update Type | Key Properties |
|---|---|---|
| `Context` (base) | Any | `client`, `update`, `api`, `chat_id`, `user_id`, `session` |
| `NewMessageCtx` | `updateNewMessage` | `message`, `text`, `command`, `args`, `reply_to`, `is_photo`, etc. |
| `CallbackQueryCtx` | `updateNewCallbackQuery` | `query_id`, `sender_user_id`, `data_str`, `match`, `chat_id`, `message_id` |
| `InlineQueryCtx` | `updateNewInlineQuery` | `query`, `sender_user_id` |

### Context Methods

Each context provides methods for the most common actions:

- **`reply()`** — Send a reply message (text or file) with `wait_for_confirmation` support
- **`edit_message()`** — Edit the current message
- **`edit_message_caption()`** — Edit media caption
- **`edit_message_media()`** — Replace media content
- **`delete_message()`** — Delete a message
- **`send_message()`** — Send a new message to the same chat (with `wait_for_confirmation` on `CallbackQueryCtx`)
- **`send_file()`** — Send a file
- **`answer()`** — Answer a callback query (CallbackQueryCtx only)
- **`get_replied_message()`** — Get the replied message (NewMessageCtx only)
- **`forward()`** — Forward messages (with `wait_for_confirmation` support)

### Send Confirmation Flow

When sending messages, TDLib returns a temporary (pending) ID immediately and finalizes it later via `updateMessageSendSucceeded`. The framework handles this through:

1. **`send_message_base`** (`core/functions/send_message.py`) — sends the message and optionally waits for confirmation
2. **`MessageTracker`** (`high_level/helpers/message_tracker.py`) — tracks pending messages and correlates with final IDs
3. **`message_send_middleware`** (`high_level/helpers/message_send_middleware.py`) — listens for `updateMessageSendSucceeded` and resolves the tracker

```
send_message_base() → pending message (temp ID)
    ↓
MessageTracker.track_pending() → asyncio.Future
    ↓
TDLib sends updateMessageSendSucceeded (old_id → new_id)
    ↓
message_send_middleware → tracker.confirm_message()
    ↓
Future resolves with final ID
```

## Layer 4: Filter DSL (`F`)

**Purpose:** Declarative, composable event matching.

### Design

- `Filter` base class with `__call__(ctx) -> bool`
- Composition operators: `&` → `AndFilter`, `|` → `OrFilter`, `~` → `NotFilter`
- Each filter type checks a specific aspect of the context
- `F.callback(pattern)` stores the regex match on `ctx._callback_match`

### Filter Types

| Category | Filters |
|---|---|
| **Message content** | `TextFilter`, `CommandFilter`, `ExactTextFilter`, `StartsWithFilter`, `EndsWithFilter`, `ContainsFilter`, `LengthFilter` |
| **Sender** | `FromUserFilter`, `PrivateChatFilter`, `GroupChatFilter`, `ChannelPostFilter` |
| **Media** | `HasMediaFilter`, `ContentTypeFilter`, `IsForwardedFilter`, `IsReplyFilter`, `IsPinnedFilter`, `IsAlbumFilter` |
| **Callback/Query** | `CallbackDataFilter`, `QueryFilter` |
| **Time** | `RateLimitFilter`, `TimeRangeFilter`, `WeekdayFilter` |
| **State** | `StateFilter`, `TextTypeFilter` |
| **Custom** | `LambdaFilter` |

## Layer 5: Plugin System

**Purpose:** Dynamic plugin lifecycle without restarting the bot.

### Flow

```
PluginManager.__init__()
  ├── Create admin router (protected from reload)
  ├── Register admin commands (/plugins, /upload, /reload, etc.)
  └── _autoload_existing() → scan plugin_dir → load all .py files and folders

PluginManager.load(file_path)
  ├── _load_module() → importlib import
  ├── _validate_plugin_module() → check PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_DESCRIPTION, setup()
  ├── Create isolated Router for plugin
  ├── Call module.setup(plugin_router)
  ├── Add all handlers to TdClient
  └── Store PluginRecord

PluginManager.reload(name)
  ├── unload(name) → remove handlers
  ├── _purge_module() → clear sys.modules
  └── load(file_path) → fresh import
```

### Plugin Upload Flow

```
/admin uploads .py or .zip
  ├── Download file from Telegram
  ├── If .py: save to plugin_dir, auto-reload
  └── If .zip: validate (single folder, __init__.py, no path traversal)
      ├── Extract to plugin_dir
      ├── Auto-reload
      └── Confirm to admin
```

## Layer 6: Helpers & Utilities

### `KeyboardBuilder`

Fluent API for building inline keyboards. Handles callback data encoding (including compression for >64 bytes via `CallbackStore` or `CallbackDB`).

### `FileHelper`

Wraps TDLib's `sendMessage` with proper `inputMessagePhoto`, `inputMessageVideo`, etc. for sending files by local path.

### `TextFormatter`

Converts Markdown/HTML strings to TDLib `formattedText` objects.

### `ConversationStore`

Manages multi-step conversations using `asyncio.Future`. A handler registers a future, and the next matching message resolves it.

### `CallbackDB`

SQLite-backed short key storage for large callback data (>64 bytes). Replaces the legacy `CallbackStore`.

### `CallbackStore`

Legacy zlib+base64 compression for large callback data. Still available but `CallbackDB` is recommended.

### `SessionStore`

Per-chat key-value storage for tracking user state across messages.

### `MessageTracker`

Tracks pending messages and correlates with final IDs. Used by `send_message_base` and `forward_messages` when `wait_for_confirmation=True`.

### `BotScheduler`

Cron-based task scheduling with `@scheduler.cron("cron_expr", name="task_name")`.

### `ErrorHandler`

Centralized error handling. Handlers register via `bot.error_handler()` decorator. Errors from filters, handlers, and middleware all route here.

### `RateLimitManager`

Per-user rate limiting. Tracks message frequency per user and can block messages that exceed a configured limit within a time window. Installed via `install_rate_limit_manager(bot._client)`.

### `FloodWaitException`

Raised by `send_message_base` when a send fails due to flood wait. Includes `retry_after` attribute with the number of seconds to wait before retrying.

### `MessageSendMiddleware`

Listens for `updateMessageSendSucceeded` and `updateMessageSendFailed` updates and routes them to the `MessageTracker`. Must be installed via `install_message_send_middleware(bot._client)`.

### `ConnectionMonitor`

Monitors the TDLib connection state and provides callbacks for connection changes (connected, disconnected, reconnecting).

### `AutoDownloadManager`

Manages automatic downloading of Telegram files (photos, videos, documents) based on configured size limits and media types.

### `PaginationHelper`

Utility for paginating large lists of items, generating page navigation buttons and handling page transitions.

### `InputValidator`

Validates user input (emails, phone numbers, URLs, etc.) with built-in validation rules.

### `Retry Middleware`

Auto-retry middleware for failed message sends. Handles `FloodWaitError` and other transient errors with exponential backoff.

### `Debug Middleware`

Logs all incoming updates and outgoing sends for debugging purposes.

## Data Flow Diagram

```
TDLib update (JSON)
    │
    ▼
ClientManager._poll_loop()
    │
    ├── @client_id match → TdClient.put_update(data)
    └── @extra match → TdClient.put_extra(data)
            │
            ▼
    TdClient.process_update_queue_loop()
            │
            ├── object_factory(data) → typed TDLib object
            ├── Construct Context (NewMessageCtx / CallbackQueryCtx / InlineQueryCtx)
            └── _spawn_dispatch(ctx) → asyncio task
                    │
                    ▼
            Middleware Chain (onion pattern)
                    │
                    ▼
            Router.notify_handlers(ctx)
                    │
                    ├── EventHandler 1: check filters → run callback
                    ├── EventHandler 2: check filters → run callback
                    └── ... (all handlers run concurrently)
```

## Key Design Decisions

1. **TDLib over Bot API** — Full access to all Telegram features including forwarding, file management, and media editing.
2. **Asyncio-first** — All I/O is async. The update queue loop never blocks, ensuring all updates are processed promptly.
3. **Onion middleware pattern** — Middlewares wrap each other, allowing pre- and post-processing of every event.
4. **Plugin isolation** — Each plugin gets its own `Router` instance, so handlers can be loaded/unloaded/reloaded independently.
5. **Callback data compression** — `CallbackStore` and `CallbackDB` transparently handle the 64-byte Telegram callback limit.
6. **Live filters** — `F.from_user(user_ids_fn=config.ADMINS)` reads admin lists dynamically on every update, so runtime changes (like `/add_admin`) are immediately effective.
7. **Send confirmation** — `MessageTracker` + `message_send_middleware` automatically correlate pending message IDs with final IDs.
8. **FloodWait handling** — `FloodWaitException` provides structured retry logic for flood wait errors.
