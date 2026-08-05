from typing import Optional, Any, Callable, List

from grathon.core.router import Router
from grathon.core.TLSchema_Manager.tltypes import updateNewMessage


class NewMessageRouter(Router[updateNewMessage]):
    """Router for new message events with filter support"""

    def __init__(self) -> None:
        super().__init__(name="NewMessageRouter")

    def on_new_message(
        self,
        func: Optional[Callable[..., Any]] = None,
        filters: Optional[List[Any]] = None,
    ):
        """Register a handler for new messages with optional filters

        Usage:
            @router.on_new_message(filters=[F.command("start")])
            async def handle_start(ctx: NewMessageCtx):
                await ctx.reply("Hi!")

            @router.on_new_message()
            async def handle_all(ctx: NewMessageCtx):
                print(ctx.text)
        """
        if func is not None:
            return self.on(updateNewMessage, filters=filters, callback=func)
        return self.on(updateNewMessage, filters=filters)
