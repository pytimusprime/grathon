"""Database-backed callback data store for Grathon.

This replaces the old zlib+base64 compression scheme. Compression could never
guarantee callback_data stays under Telegram's 64-byte limit (proof: the set of
strings <= 64 bytes is finite, but the set of possible payloads is not, so no
lossless compression can be a bijection onto that space -- payloads in the
~33-200 byte range always *grow* under zlib+base64).

Instead we use indirection: a short, fixed-width key (``cb_<12 hex>`` = 15 bytes)
is stored in a SQLite database (via PicoDB) alongside the original payload. The
key is always <= 15 bytes, so it is always far under the 64-byte Telegram limit,
regardless of payload size.

Records expire after a configurable TTL (default 7 days) so the table stays
small. Expired keys resolve to None (callers should show a "session expired"
message, matching the existing page_state behaviour in plugins).

Sync bridge
-----------
``KeyboardBuilder.button()`` and ``CallbackQueryCtx.data_str`` are *synchronous*
(they cannot ``await``), but PicoDB is async. To keep those hot paths
synchronous we run the async PicoDB operations on a dedicated background thread
that owns its own event loop. The ``*_sync`` wrappers submit coroutines to that
thread via ``asyncio.run_coroutine_threadsafe`` and block for the result. This
avoids nesting event loops inside the bot's main loop.
"""

from __future__ import annotations

import asyncio
import secrets
import threading
import time
from dataclasses import dataclass
from typing import Optional

from picodb import AsyncPicodb

# Prefix for short callback keys. "cb_" + 12 hex chars = 15 bytes total,
# always far below Telegram's 64-byte limit.
CB_PREFIX = "cb_"
CB_ID_LEN = 12  # hex chars -> 12 bytes of entropy
CALLBACK_DB_PATH = "grathon_callbacks.sqlite"
DEFAULT_TTL_SECONDS = 7 * 24 * 60 * 60  # 7 days


@dataclass
class _CallbackRecord:
    record_id: str
    cbkey: str
    data: str
    expires_at: int


class _SyncLoop:
    """Runs an asyncio event loop on a dedicated daemon thread."""

    def __init__(self) -> None:
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._started = False
        self._lock = threading.Lock()

    def _run(self) -> None:
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def start(self) -> None:
        with self._lock:
            if not self._started:
                self._thread.start()
                self._started = True

    def run(self, coro):
        """Schedule a coroutine on the loop and block until it returns."""
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result()


class CallbackDB:
    """SQLite-backed store mapping short callback keys to original payloads."""

    _instance: "Optional[CallbackDB]" = None

    def __init__(self, path: str = CALLBACK_DB_PATH, ttl_seconds: int = DEFAULT_TTL_SECONDS):
        self._path = path
        self._ttl = ttl_seconds
        self._db: Optional[AsyncPicodb[_CallbackRecord]] = None
        self._initialized = False
        self._loop = _SyncLoop()
        self._loop.start()

    @classmethod
    def instance(cls) -> "CallbackDB":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def init(self) -> None:
        """Create the SQLite table. Idempotent."""
        if self._initialized:
            return
        self._db = AsyncPicodb(
            _CallbackRecord,
            f"sqlite+aiosqlite:///{self._path}",
            enable_fts=False,
        )
        await self._db.init_db()
        self._initialized = True

    def _gen_key(self) -> str:
        return CB_PREFIX + secrets.token_hex(CB_ID_LEN // 2)

    async def register(self, data: str) -> str:
        """Store payload and return a short callback key (always <= 15 bytes).

        If the same payload already exists, returns the existing key (get-or-create).
        """
        if self._db is None:
            raise RuntimeError("CallbackDB not initialized; call init() first")

        # Get-or-create: check if this exact payload already has a key
        existing = await self._db.query().eq("data", data).search()
        if existing:
            rec = existing[0]
            if rec.expires_at > int(time.time()):
                return rec.cbkey
            # Expired — delete so we can re-create fresh
            await self._db.delete(rec.cbkey)

        cbkey = self._gen_key()
        expires_at = int(time.time()) + self._ttl
        # Retry briefly on the astronomically unlikely key collision.
        for _ in range(3):
            rec = _CallbackRecord(
                record_id=cbkey, cbkey=cbkey, data=data, expires_at=expires_at
            )
            try:
                await self._db.insert(rec)
                return cbkey
            except Exception:
                cbkey = self._gen_key()
        raise RuntimeError("Failed to register callback key after retries")

    async def resolve(self, cbkey: str) -> "Optional[str]":
        """Return the original payload for a key, or None if missing/expired."""
        if self._db is None:
            return None
        if not cbkey.startswith(CB_PREFIX):
            return None
        recs = await self._db.query().eq("cbkey", cbkey).search()
        if not recs:
            return None
        rec = recs[0]
        if rec.expires_at <= int(time.time()):
            await self._db.delete(rec.cbkey)
            return None
        return rec.data

    async def purge_expired(self) -> int:
        """Delete all expired records. Returns count removed."""
        if self._db is None:
            return 0
        now = int(time.time())
        deleted = await self._db.query().lt("expires_at", now).delete()
        return deleted or 0

    # ---- Synchronous bridges (for button() and data_str) ----

    def _ensure_init_sync(self) -> None:
        """Lazily initialize the DB on the background thread if needed.

        This makes KeyboardBuilder.button() / data_str safe to use even if
        init_callback_db() was never called (e.g. in standalone scripts or
        before bot startup). Idempotent.
        """
        if not self._initialized:
            self._loop.run(self.init())

    def register_sync(self, data: str) -> str:
        self._ensure_init_sync()
        return self._loop.run(self.register(data))

    def resolve_sync(self, cbkey: str) -> "Optional[str]":
        self._ensure_init_sync()
        return self._loop.run(self.resolve(cbkey))


# Module-level convenience wrappers backed by the singleton instance.
_async_db = CallbackDB.instance()


async def init_callback_db() -> None:
    """Initialize the shared callback database (call once at bot startup)."""
    await _async_db.init()


def register_callback(data: str) -> str:
    """Synchronous: store payload, return a short key (always <= 15 bytes)."""
    return _async_db.register_sync(data)


def resolve_callback(cbkey: str) -> "Optional[str]":
    """Synchronous: resolve a short key to the original payload (or None)."""
    return _async_db.resolve_sync(cbkey)


async def register_callback_async(data: str) -> str:
    return await _async_db.register(data)


async def resolve_callback_async(cbkey: str) -> "Optional[str]":
    return await _async_db.resolve(cbkey)


async def purge_expired_callbacks() -> int:
    return await _async_db.purge_expired()
