"""
Connection Monitor Middleware

Display connection state updates from TDLib
Shows when bot connects, disconnects, waits for network, etc.

This helps understand the bot's connection lifecycle and detect network issues.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from grathon.core.middleware import Middleware

logger = logging.getLogger(__name__)


def create_connection_monitor_middleware():
    """
    Create middleware to monitor and display connection state changes

    Usage:
        client.use(create_connection_monitor_middleware())
    """

    async def connection_monitor_middleware(ctx, next_fn):
        """Monitor connection state updates"""

        from grathon.core.TLSchema_Manager.tltypes import (
            updateConnectionState,
            connectionStateWaitingForNetwork,
            connectionStateConnectingToProxy,
            connectionStateConnecting,
            connectionStateUpdating,
            connectionStateReady,
        )

        # Only process connection state updates
        if isinstance(ctx.update, updateConnectionState):
            state = ctx.update.state

            if isinstance(state, connectionStateWaitingForNetwork):
                print("⚠️  Waiting for network connection...")
                logger.info("Connection state: WAITING_FOR_NETWORK")

            elif isinstance(state, connectionStateConnectingToProxy):
                print("🔄 Connecting to proxy...")
                logger.info("Connection state: CONNECTING_TO_PROXY")

            elif isinstance(state, connectionStateConnecting):
                print("🔌 Connecting to Telegram...")
                logger.info("Connection state: CONNECTING")

            elif isinstance(state, connectionStateUpdating):
                print("📡 Synchronizing with Telegram (updating)...")
                logger.info("Connection state: UPDATING")

            elif isinstance(state, connectionStateReady):
                print("✅ Connected and ready!")
                logger.info("Connection state: READY")

            else:
                state_name = type(state).__name__
                print(f"🔗 Connection state: {state_name}")
                logger.info(f"Connection state: {state_name}")

        # Continue to next middleware
        await next_fn(ctx)

    return connection_monitor_middleware


# Optional: Create a version with logging callback
class ConnectionStateTracker:
    """
    Track connection state changes with optional callback

    Usage:
        tracker = ConnectionStateTracker()
        tracker.on_state_change(my_callback)
        middleware = tracker.create_middleware()
        client.use(middleware)
    """

    def __init__(self):
        self._callbacks = []
        self._current_state = None

    def on_state_change(self, callback):
        """Register callback for state changes"""
        self._callbacks.append(callback)
        return self

    async def _notify_callbacks(self, state_name: str, state_type):
        """Call all registered callbacks"""
        for callback in self._callbacks:
            try:
                if callable(callback):
                    result = callback(state_name, state_type)
                    if hasattr(result, '__await__'):
                        await result
            except Exception as e:
                logger.error(f"Error in connection state callback: {e}")

    def create_middleware(self):
        """Create middleware using this tracker"""

        async def middleware(ctx, next_fn):
            from grathon.core.TLSchema_Manager.tltypes import (
                updateConnectionState,
                connectionStateWaitingForNetwork,
                connectionStateConnectingToProxy,
                connectionStateConnecting,
                connectionStateUpdating,
                connectionStateReady,
            )

            if isinstance(ctx.update, updateConnectionState):
                state = ctx.update.state
                state_name = type(state).__name__

                # Map state to user-friendly name
                state_display = {
                    'connectionStateWaitingForNetwork': ('⚠️  Waiting for network', 'WAITING_FOR_NETWORK'),
                    'connectionStateConnectingToProxy': ('🔄 Connecting to proxy', 'CONNECTING_TO_PROXY'),
                    'connectionStateConnecting': ('🔌 Connecting', 'CONNECTING'),
                    'connectionStateUpdating': ('📡 Synchronizing', 'UPDATING'),
                    'connectionStateReady': ('✅ Connected', 'READY'),
                }.get(state_name, (f'🔗 {state_name}', state_name))

                display_msg, internal_name = state_display

                # Print to console
                print(display_msg)
                logger.info(f"Connection: {internal_name}")

                # Update current state
                self._current_state = internal_name

                # Notify callbacks
                await self._notify_callbacks(internal_name, state)

            # Continue to next middleware
            await next_fn(ctx)

        return middleware

    @property
    def current_state(self) -> str:
        """Get current connection state"""
        return self._current_state or "UNKNOWN"

    def is_ready(self) -> bool:
        """Check if currently connected"""
        return self._current_state == "READY"

    def is_connecting(self) -> bool:
        """Check if currently connecting"""
        return self._current_state in ["CONNECTING", "CONNECTING_TO_PROXY", "UPDATING"]

    def is_offline(self) -> bool:
        """Check if currently offline"""
        return self._current_state in ["WAITING_FOR_NETWORK", "UNKNOWN"]


# Convenience function to install with default settings
def install_connection_monitor(client):
    """
    Install connection monitor middleware with default settings

    Usage:
        from grathon.high_level.helpers.connection_monitor import install_connection_monitor
        install_connection_monitor(bot._client)
    """
    middleware = create_connection_monitor_middleware()
    client.use(middleware)
    logger.info("✅ Connection Monitor middleware installed")
