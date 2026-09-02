"""
Download Monitor Router
Monitor updateFileDownloads and updateOption updates
"""

from typing import TypeAlias, Callable, List
from grathon.core.TLSchema_Manager.tltypes import (
    updateFileDownloads,
    updateOption,
)
from grathon.core.contexts.context import Context


# Type aliases
FileDownloadCtx: TypeAlias = Context[updateFileDownloads]
OptionCtx: TypeAlias = Context[updateOption]


class DownloadMonitorRouter:
    """Monitor download and settings updates"""

    def __init__(self):
        self._download_handlers: List[Callable] = []
        self._option_handlers: List[Callable] = []
        self._all_handlers: List[Callable] = []

    def on_file_download(self, handler: Callable) -> Callable:
        """Register handler for updateFileDownloads"""
        self._download_handlers.append(handler)
        self._all_handlers.append(handler)
        return handler

    def on_option_update(self, handler: Callable) -> Callable:
        """Register handler for updateOption"""
        self._option_handlers.append(handler)
        self._all_handlers.append(handler)
        return handler

    def on_any(self, handler: Callable) -> Callable:
        """Register handler for any update"""
        self._all_handlers.append(handler)
        return handler

    async def handle_update(self, update) -> None:
        """Process updates"""

        if isinstance(update, updateFileDownloads):
            ctx = Context(update, None)  # Context with update
            for handler in self._download_handlers + self._all_handlers:
                try:
                    result = handler(ctx)
                    if hasattr(result, "__await__"):
                        await result
                except Exception as e:
                    print(f"❌ Download handler error: {e}")

        elif isinstance(update, updateOption):
            ctx = Context(update, None)
            for handler in self._option_handlers + self._all_handlers:
                try:
                    result = handler(ctx)
                    if hasattr(result, "__await__"):
                        await result
                except Exception as e:
                    print(f"❌ Option handler error: {e}")
