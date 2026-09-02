"""
Universal debug middleware — logs every TDLib update to diagnose issues.
Install in main.py: install_debug_middleware(bot._client)
"""

from __future__ import annotations

import logging
from grathon.core.TLSchema_Manager.tltypes import Update

logger = logging.getLogger(__name__)


async def debug_middleware(ctx, next_fn):
    update = ctx.update
    update_type = type(update).__name__ if update else "None"
    logger.debug(f"[TDLib UPDATE] type={update_type}")
    print(f"[TDLib] {update_type}: {update}")
    await next_fn(ctx)


def install_debug_middleware(client) -> None:
    client.use(debug_middleware)
    logger.info("✅ Debug middleware installed — all TDLib updates will be logged")
