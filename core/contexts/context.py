from __future__ import annotations
from typing import TYPE_CHECKING, Generic, TypeVar, Any, Optional

if TYPE_CHECKING:
    from grathon.core.tdclient import TdClient
    from grathon.core.TLSchema_Manager.tlmethods import GeneratedMethods

TUpdate = TypeVar("TUpdate")

class Context(Generic[TUpdate]):
    """
    Base context for all event handlers
    """
    def __init__(self, client: 'TdClient', update: TUpdate):
        super().__init__()
        self.client: 'TdClient' = client
        self.update: TUpdate = update
        self._stop_propagation: bool = False
        self.data: dict = {}  # Shared data dict for filter→handler data passing

    def stop_propagation(self) -> None:
        """Stop other handlers from being called for this event"""
        self._stop_propagation = True

    @property
    def api(self) -> GeneratedMethods:
        """Direct access to generated methods"""
        return self.client.api

    @property
    def chat_id(self) -> Optional[int]:
        """Get chat ID from context (override in subclasses)"""
        return None

    @property
    def user_id(self) -> Optional[int]:
        """Get the user ID of the sender/clicker (override in subclasses)

        Works uniformly across NewMessageCtx, CallbackQueryCtx, and InlineQueryCtx.
        Use this instead of accessing sender_id.user_id or sender_user_id directly.

        Examples:
            uid = ctx.user_id  # works in any handler
        """
        return None

    def get_session_value(self, key: str, default: Any = None) -> Any:
        """Get a specific value from session for this chat

        Args:
            key: Session key
            default: Default value if key doesn't exist

        Returns:
            Session value for that key, or default if not found
        """
        if self.client.session is not None and self.chat_id is not None:
            return self.client.session.get_value(self.chat_id, key, default)
        return default

    def set_session_value(self, key: str, value: Any) -> None:
        """Set a value in session for this chat

        Args:
            key: Session key
            value: Value to store
        """
        if self.client.session is not None and self.chat_id is not None:
            self.client.session.set(self.chat_id, key, value)

    def delete_session_value(self, key: str) -> None:
        """Delete a value from session for this chat

        Args:
            key: Session key to delete
        """
        if self.client.session is not None and self.chat_id is not None:
            self.client.session.delete(self.chat_id, key)