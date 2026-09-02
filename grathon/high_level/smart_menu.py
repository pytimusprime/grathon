"""SmartMenu — fluent builder for navigational menus (stub).

This is a temporary stub to silence ImportError while the full
implementation lands. The real SmartMenu will add:
- automatic pagination for .items()
- breadcrumb path (.show_path)
- home/back buttons (.show_home, .back_button)
- depth limiting (.max_depth)
"""

from __future__ import annotations

from typing import List, Optional, Tuple


class SmartMenu:
    """Minimal stub — method-chaining API that sends a plain text message."""

    def __init__(self, ctx):
        self._ctx = ctx
        self._text = ""

    def text(self, text: str) -> "SmartMenu":
        self._text = text
        return self

    def item(self, label: str, callback: str) -> "SmartMenu":
        return self

    def items(
        self,
        items: List[Tuple[str, str]],
        per_page: int = 5,
    ) -> "SmartMenu":
        return self

    def show_path(self, enabled: bool = True) -> "SmartMenu":
        return self

    def show_home(self, enabled: bool = True, label: str = "🏠 خانه") -> "SmartMenu":
        return self

    def back_button(self, label: str = "🔙 بازگشت") -> "SmartMenu":
        return self

    def max_depth(self, depth: int) -> "SmartMenu":
        return self

    async def send(self):
        await self._ctx.reply(self._text)
