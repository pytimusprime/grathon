from __future__ import annotations

from typing import List, Any, Optional, Callable, TypeVar, Generic, Awaitable, TypeAlias, TYPE_CHECKING
from grathon.core.eventhandler import EventHandler

if TYPE_CHECKING:
    from grathon.core.contexts.context import Context

TUpdate = TypeVar("TUpdate")
FilterFunc: TypeAlias = "Callable[['Context[TUpdate]'], Awaitable[bool]]"

class Router(Generic[TUpdate]):
    """
    Router
    """
    def __init__(self, name: Optional[str] = None):
        super().__init__()
        self.name = name
        self.handlers: List[EventHandler[TUpdate]] = []
        self.sub_routers: List[Router[TUpdate]] = []   # ← Important! TUpdate must be same

    def on(
        self,
        event_type: type[TUpdate],
        filters: Optional[List[FilterFunc[TUpdate]]] = None,
        *,
        callback: Optional[Callable[['Context[TUpdate]'], Any]] = None,
    ) -> Callable[[Context[Any]], Any] | Callable[
        [Callable[['Context[TUpdate]'], Any]], Callable[['Context[TUpdate]'], Any]]:


        def decorator(func: Callable[['Context[TUpdate]'], Any]) -> Callable[['Context[TUpdate]'], Any]:
            handler = EventHandler[TUpdate](
                event_type=event_type,
                callback=func,
                filters=filters or [],
            )
            self.handlers.append(handler)

            return func
        if callback is not None:
            return decorator(callback)

        return decorator

    def append(self, router: 'Router[TUpdate]') -> None:
        self.sub_routers.append(router)

    def include_router(self, router: 'Router[TUpdate]') -> None:
        self.append(router)