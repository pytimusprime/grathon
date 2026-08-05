"""Session state management for per-user/chat persistent data"""

import os
import json
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class SessionStore:
    """In-memory session storage with optional JSON file persistence

    Stores key-value data per chat_id. Useful for tracking user state across messages
    without modifying the bot or adding database complexity.

    Usage:
        # In-memory only
        session = SessionStore()

        # With optional file persistence
        session = SessionStore(persist_path="sessions.json")
        session.save()  # Write to disk
        session.load()  # Load from disk

    Accessing in handlers:
        @bot.on_command("start")
        async def start(ctx):
            ctx.session["step"] = 1
            await ctx.reply("Step 1 of 3")

        @bot.on_message()
        async def next_step(ctx):
            step = ctx.session.get("step", 0)
            if step == 1:
                ctx.session["step"] = 2

        # Or using the session store directly:
        step = bot.session.get_value(chat_id, "step", default=0)
    """

    def __init__(self, persist_path: Optional[str] = None, auto_save: bool = False):
        """Initialize session store

        Args:
            persist_path: Optional path to JSON file for persistence.
                         If provided and file exists, load() is called automatically.
            auto_save: If True, automatically save to file after set/delete operations
        """
        self._data: dict[int, dict[str, Any]] = {}
        self._path = persist_path
        self._auto_save = auto_save
        if self._path:
            self.load()

    def get(self, chat_id: int) -> dict[str, Any]:
        """Get session dict for chat_id (creates if not exists)

        Args:
            chat_id: Chat ID

        Returns:
            Session dict for that chat (may be empty)
        """
        return self._data.setdefault(chat_id, {})

    def get_value(self, chat_id: int, key: str, default: Any = None) -> Any:
        """Get a specific value from session for chat_id

        Args:
            chat_id: Chat ID
            key: Session key
            default: Default value if key doesn't exist

        Returns:
            Session value for that key, or default if not found
        """
        return self._data.get(chat_id, {}).get(key, default)

    def set(self, chat_id: int, key: str, value: Any) -> None:
        """Set a key in the session for chat_id

        Args:
            chat_id: Chat ID
            key: Session key
            value: Value to store
        """
        self._data.setdefault(chat_id, {})[key] = value
        if self._auto_save:
            self.save()

    def delete(self, chat_id: int, key: Optional[str] = None) -> None:
        """Delete a key or entire session for chat_id

        Args:
            chat_id: Chat ID
            key: Key to delete. If None, deletes entire session for that chat.
        """
        if key is None:
            self._data.pop(chat_id, None)
        else:
            self._data.get(chat_id, {}).pop(key, None)
        if self._auto_save:
            self.save()

    def clear(self) -> None:
        """Clear all session data"""
        self._data.clear()

    def save(self) -> None:
        """Save session data to JSON file

        Only works if persist_path was set during initialization.
        Converts chat IDs (ints) to strings for JSON compatibility.
        """
        if not self._path:
            return
        try:
            with open(self._path, 'w', encoding='utf-8') as f:
                json.dump({str(k): v for k, v in self._data.items()}, f, indent=2)
            logger.info(f"Sessions saved to {self._path}")
        except (OSError, TypeError) as e:
            logger.error(f"Failed to save sessions: {e}")

    def load(self) -> None:
        """Load session data from JSON file

        Only works if persist_path was set during initialization.
        Converts string keys back to int chat IDs.
        Silently ignores if file doesn't exist.
        """
        if not self._path or not os.path.exists(self._path):
            return
        try:
            with open(self._path, encoding='utf-8') as f:
                data = json.load(f)
            self._data = {int(k): v for k, v in data.items()}
            logger.info(f"Sessions loaded from {self._path}")
        except (OSError, json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to load sessions: {e}")
