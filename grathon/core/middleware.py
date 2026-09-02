"""
Middleware pipeline for event processing

Middleware wraps the entire dispatch pipeline using the onion/decorator pattern.
Each middleware receives (ctx, next) and can run code before/after calling next().
"""

from __future__ import annotations
from typing import Awaitable, Callable, TypeAlias, Any

# Middleware type: async function that receives context and next() callable
Middleware: TypeAlias = Callable[
    [Any, Callable[[Any], Awaitable[None]]],
    Awaitable[None]
]


def build_chain(
    middlewares: list[Middleware],
    endpoint: Callable[[Any], Awaitable[None]],
) -> Callable[[Any], Awaitable[None]]:
    """Build recursive middleware chain using onion pattern

    Middlewares are applied in order: first registered -> first to run.
    Each middleware wraps the previous one.

    Args:
        middlewares: List of middleware functions
        endpoint: Terminal function (notify_handlers)

    Returns:
        Chain function: (ctx) -> Awaitable[None]

    Example:
        >>> chain = build_chain([mw1, mw2], notify_handlers)
        >>> await chain(ctx)
        # Calls: mw1 -> mw2 -> notify_handlers

    Execution order (mw1 registered first):
        - mw1 runs (before next)
        - mw2 runs (before next)
        - notify_handlers runs
        - mw2 continues (after next)
        - mw1 continues (after next)
    """
    # Start with the endpoint
    chain = endpoint

    # Wrap in reverse order (so first registered middleware is outermost)
    for mw in reversed(middlewares):
        # Capture current chain iteration value
        prev = chain

        async def wrapped(ctx: Any, _mw: Middleware = mw, _prev: Callable = prev) -> None:
            """Wrapper that calls middleware with next pointing to previous chain"""
            await _mw(ctx, _prev)

        chain = wrapped

    return chain
