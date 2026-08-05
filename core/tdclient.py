from __future__ import annotations

import asyncio
import base64
import json
import logging
import uuid
from dataclasses import fields

from asyncio import Queue
from typing import Any, Dict, Optional, TYPE_CHECKING, Callable, Awaitable, List, Union
from typing_extensions import TypeIs
from grathon.core.TLSchema_Manager.tltypes import get_td_type, Update, updateNewMessage, updateNewCallbackQuery, updateNewInlineQuery, TdObject
from grathon.core.clientmanager import ClientManager
from grathon.core.errors.TDLibError import TDLibError
import tdjson
from grathon.core.TLSchema_Manager.tlmethods import GeneratedMethods
from grathon.core.contexts.context import Context
from grathon.core.contexts.NewMessageCtx import NewMessageCtx
from grathon.core.contexts.CallbackQueryCtx import CallbackQueryCtx
from grathon.core.contexts.InlineQueryCtx import InlineQueryCtx
from grathon.core.router import Router
from grathon.core.middleware import Middleware, build_chain
from grathon.high_level.error_handler import ErrorHandler
# Only for TYPE_CHECKING
if TYPE_CHECKING:
    from grathon.core.eventhandler import EventHandler

logger = logging.getLogger(__name__)


class TdObjectEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles TdObject and bytes"""

    def default(self, o: Any) -> Any:

        # 1. Handle TDLib objects
        if hasattr(o, 'to_dict'):
            return o.to_dict()

        if isinstance(o, bytes):
            return base64.b64encode(o).decode('utf-8')

        return super().default(o)


def is_list_of_any(value: object) -> TypeIs[list[Any]]:
    return isinstance(value, list)

def is_dict_with_any_value(value:object)-> TypeIs[Dict[str,Any]]:
    return isinstance(value,dict)

def is_tl_update(value: object) -> TypeIs[Update]:
    return isinstance(value, Update)


def object_factory(data: Any) -> Any:
    if is_list_of_any(data):
        return [object_factory(i) for i in data]

    if not isinstance(data, dict) or "@type" not in data:
        return data

    obj_type = data.get("@type")
    cls = get_td_type(obj_type)  # pyright: ignore [reportArgumentType]

    if not cls:
        return data

    clean_params = {}
    # Get fields with their types
    class_fields = {f.name: f.type for f in fields(cls)}

    for k, v in data.items():
        if k in class_fields:
            field_type = class_fields[k]

            # Check if field is bytes type (or Optional[bytes])
            # and input data is string (Base64)
            if isinstance(v, str) and _is_bytes_type(field_type):
                try:
                    v = base64.b64decode(v)
                except Exception:
                    pass  # If decode failed, keep original value

            # Recursive conversion for nested values
            clean_params[k] = object_factory(v)

    return cls(**clean_params)


def _is_bytes_type(t: Any) -> bool:
    """Check if type is bytes or not (even for Optional)"""
    if t is bytes:
        return True
    # Handle Optional[bytes] or Union[bytes, None]
    origin = getattr(t, "__origin__", None)
    if origin is Union:
        return bytes in getattr(t, "__args__", [])
    return False

class TdClient:

    def __init__(self, manager: ClientManager):
        super().__init__()
        # Lazy import to avoid circular dependency

        self._client_id = tdjson.td_create_client_id()

        self.manager = manager
        self.handlers: list[EventHandler[Update]] = []   # ← add here
        self.waiters: Dict[str, asyncio.Future[Any]] = {}
        self.api:GeneratedMethods = GeneratedMethods(self)


        self.routers:List[Router[Update]] = []
        self.router = Router[Update](name="MainClientRouter")

        # Wire router into handlers
        self.include_router(self.router)

        # Register this client in the manager
        self.manager.add_client(self._client_id, self)
        # Ensure the manager's loop is running
        self.manager.start()

        self._update_queue:Queue[Any] = asyncio.Queue()
        self._extra_queue: Queue[Any] = asyncio.Queue()

        # Middleware pipeline
        self._middlewares: list[Middleware] = []
        self._dispatch: Callable[[Context[Update]], Awaitable[None]] = self.notify_handlers

        # Session store (injected by GrathonBot, or user-supplied)
        self.session: Any = None

        # Error handler (centralized exception handling for all events)
        self.error_handler: ErrorHandler = ErrorHandler()

        # Background tasks for graceful shutdown
        self._tasks: list[asyncio.Task] = []

        # In-flight dispatch tasks (one per update). Kept as strong refs so
        # asyncio doesn't GC them mid-await; auto-removed on completion.
        self._dispatch_tasks: set[asyncio.Task[None]] = set()


    def put_update(self, data:Dict[str,Any]):
        # print("Putting update to queue :",data)
        self._update_queue.put_nowait(data)
        # print("Update-Qsize: ",self._update_queue.qsize())

    def put_extra(self, data:Dict[str,Any]):
        # print("Putting extra to queue :",data)
        self._extra_queue.put_nowait(data)
        # print("Extra-Qsize: ",self._extra_queue.qsize())

    async def send(self, query: Dict[str, Any]):
        """Send request as byte-encoded"""
        if "@extra" not in query:
            query["@extra"] = str(uuid.uuid4())

        encoded_query = json.dumps(query, cls=TdObjectEncoder).encode()
        tdjson.td_send(self._client_id, encoded_query)
        return query["@extra"]

    async def call_method(self, method_name: str,
                          params_dict: Optional[Dict[str, Any]] = None,
                          **params:Dict[str, Any]) -> Any:
        """
        Helper method to call TDLib methods and wait for the response.
        Handles both dictionary-style and keyword-style arguments.
        """
        # Merge dictionary params and keyword params
        actual_params = params_dict or {}
        actual_params.update(params)

        extra_id = str(uuid.uuid4())
        actual_params["@type"] = method_name
        actual_params["@extra"] = extra_id
        future = asyncio.get_running_loop().create_future()
        self.waiters[extra_id] = future

        try:
            _ = await self.send(actual_params)
            result = await asyncio.wait_for(future, timeout=30.0)
        finally:
            # Always remove the waiter. The extra-queue loop pops it on a
            # successful response, but on timeout / send error / cancellation
            # the entry would otherwise stay in self.waiters forever — a
            # slow leak that grows with every failed call.
            self.waiters.pop(extra_id, None)

        if isinstance(result, dict) and result.get("@type") == "error":
            error_code = result.get("code", 0)
            error_msg = result.get("message", "Unknown error")
            if error_code == 400 and "no text in the message to edit" in error_msg:
                logger.debug(
                    "editMessageText skipped (media message, falling back to caption): chat=%s msg=%s",
                    actual_params.get("chat_id"), actual_params.get("message_id"),
                )
            else:
                logger.error(
                    "TDLib API error %s in %s: %s", error_code, method_name, error_msg,
                )
            raise TDLibError(code=error_code, message=error_msg)

        if hasattr(result, '__td_type__') and result.__td_type__ == 'error':
            error_code = getattr(result, 'code', 0)
            error_msg = getattr(result, 'message', 'Unknown error')
            if error_code == 400 and "no text in the message to edit" in error_msg:
                logger.debug(
                    "editMessageText skipped (media message, falling back to caption): chat=%s msg=%s",
                    actual_params.get("chat_id"), actual_params.get("message_id"),
                )
            else:
                logger.error(
                    "TDLib API error %s in %s: %s", error_code, method_name, error_msg,
                )
            raise TDLibError(code=error_code, message=error_msg)

        return object_factory(result)

    def use(self, middleware: Middleware) -> None:
        """Register middleware in the dispatch pipeline

        Args:
            middleware: Async callable (ctx, next) -> Awaitable[None]

        Example:
            >>> async def logging_mw(ctx, next):
            ...     print(f"→ {type(ctx.update).__name__}")
            ...     await next(ctx)
            ...     print("← Done")
            >>> client.use(logging_mw)
        """
        self._middlewares.append(middleware)
        self._dispatch = build_chain(self._middlewares, self.notify_handlers)

    async def process_update_queue_loop(self):
        """Drain the update queue forever.

        This loop must stay alive even when individual updates blow up —
        if it dies, the bot becomes silently dead. So the outer except
        catches *any* Exception (CancelledError still breaks the loop).
        """
        while True:
            try:
                event = await self._update_queue.get()
                try:
                    typed_event = object_factory(event)
                except Exception as e:
                    logger.error(
                        "Failed to construct event object: %s", e, exc_info=True,
                    )
                    continue

                # Dispatch must NOT block this loop — handlers may suspend on
                # wait_message()/wait_callback() futures that only resolve when
                # *future* updates flow through this same loop. Spawning a
                # task per update lets the loop keep draining the queue.
                try:
                    if isinstance(typed_event, updateNewMessage):
                        self._spawn_dispatch(NewMessageCtx(self, typed_event))  # pyright: ignore [reportArgumentType]
                    elif isinstance(typed_event, updateNewCallbackQuery):
                        self._spawn_dispatch(CallbackQueryCtx(self, typed_event))  # pyright: ignore [reportArgumentType]
                    elif isinstance(typed_event, updateNewInlineQuery):
                        self._spawn_dispatch(InlineQueryCtx(self, typed_event))  # pyright: ignore [reportArgumentType]
                    elif isinstance(typed_event, Update):
                        self._spawn_dispatch(Context(self, typed_event))
                except Exception as e:
                    # ctx construction or _spawn_dispatch failed before the
                    # middleware chain could run — route through error_handler
                    # so it lands in the same place as handler failures.
                    logger.exception(
                        "Failed to spawn dispatch for %s",
                        type(typed_event).__name__,
                    )
                    try:
                        await self.error_handler.handle(e, None)
                    except Exception:
                        pass

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception("Unexpected error in update queue loop: %s", e)
                await asyncio.sleep(1)  # Prevent 100% CPU in error loop


    async def process_extra_queue_loop(self):
        """Resolve futures for outstanding API calls.

        If this loop dies, every future call_method() will hang until its
        own wait_for() timeout — so we keep it alive against any Exception.
        """
        while True:
            try:
                event = await self._extra_queue.get()
                typed_event = object_factory(event)
                extra_id = event.get("@extra")
                if extra_id and extra_id in self.waiters:
                    future = self.waiters.pop(extra_id)
                    if not future.done():
                        future.set_result(typed_event)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception("Unexpected error in extra queue loop: %s", e)
                await asyncio.sleep(1)  # Prevent 100% CPU in error loop

    async def run_forever(self):
        print(f"🚀 Client {self._client_id} is running...")

        task_update = asyncio.create_task(self.process_update_queue_loop())
        task_extra = asyncio.create_task(self.process_extra_queue_loop())
        self._tasks = [task_update, task_extra]
        try:
            await asyncio.gather(task_update, task_extra)
        except asyncio.CancelledError:
            pass

    async def stop(self) -> None:
        """Gracefully stop background tasks and close TDLib client"""
        for task in self._tasks:
            task.cancel()
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

        pending_dispatch = list(self._dispatch_tasks)
        for task in pending_dispatch:
            task.cancel()
        if pending_dispatch:
            await asyncio.gather(*pending_dispatch, return_exceptions=True)
        self._dispatch_tasks.clear()

        try:
            await self.api.close()
        except (asyncio.TimeoutError, RuntimeError) as e:
            logger.warning(f"Error closing TDLib client: {e}")

    def _spawn_dispatch(self, ctx: Context[Update]) -> None:
        """Run dispatch for one update on a background task.

        Why: the queue-processing loop must keep pulling new updates while
        a handler is suspended in wait_message()/wait_callback() — otherwise
        the very update that would resolve the waiting future can't reach
        the middleware, and the conversation deadlocks until timeout.
        """
        task = asyncio.create_task(self._safe_dispatch(ctx))
        self._dispatch_tasks.add(task)
        task.add_done_callback(self._dispatch_tasks.discard)

    async def _safe_dispatch(self, ctx: Context[Update]) -> None:
        """Run the middleware+handler chain for a single update."""
        try:
            await self._dispatch(ctx)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"[DISPATCH ERROR] {type(e).__name__}: {e}")
            try:
                await self.error_handler.handle(e, ctx)
            except Exception:
                logger.exception(
                    "error_handler itself failed for %s",
                    type(ctx.update).__name__,
                )

    async def notify_handlers(self, ctx: Context[Update]) -> None:
        """Dispatch context to handlers.

        All handlers run concurrently so long-running handlers don't block
        other updates from being processed. This allows middleware to intercept
        subsequent messages even while a handler is waiting.
        """
        tasks = []
        for handler in self.handlers:
            task = asyncio.create_task(handler.check_and_execute(ctx))
            tasks.append(task)

        # Run all tasks concurrently, but still respect stop_propagation
        # by cancelling remaining tasks if one signals to stop
        try:
            for completed in asyncio.as_completed(tasks):
                try:

                    await completed
                    if ctx._stop_propagation:
                        # Cancel remaining tasks when stop_propagation is set
                        for task in tasks:
                            if not task.done():
                                task.cancel()
                        break
                except asyncio.CancelledError:
                    pass
        except Exception:
            # Make sure all tasks are cancelled if anything fails
            for task in tasks:
                if not task.done():
                    task.cancel()
            raise

    def include_router(self, router: Router[Any],nostore=False) -> None:
        """Connect router handlers to the main client"""
        if not nostore:
            self.routers.append(router)
        self.handlers.extend(router.handlers)
        for sub_router in router.sub_routers:
            self.include_router(sub_router)  # Recursive call


    def remove_router(self,router: Router[Any]):
        """

        """
        self.routers.remove(router)

    def reload_routers(self):
        """Rebuild handler list from routers while preserving direct handlers"""
        router_handler_ids = set()
        for router in self.routers:
            for handler in router.handlers:
                router_handler_ids.add(id(handler))

        direct_handlers = [h for h in self.handlers if id(h) not in router_handler_ids]
        self.handlers = []
        for router in self.routers:
            self.include_router(router, True)
        self.handlers.extend(direct_handlers)


    def add_handler(self, handler: EventHandler[Any]) -> None:
        """Directly add a handler to dispatch list (for plugin system)"""
        self.handlers.append(handler)

    def remove_handler(self, handler: EventHandler[Any]) -> bool:
        """Remove a handler by object identity.
        Return True if found and removed, False otherwise."""
        try:
            self.handlers.remove(handler)
            return True
        except ValueError:
            return False

    # async def _on_update(self, event: Update):
    #     update_type = event.__td_type__
    #     print(f"🔄 New update: {update_type}")
    #
    #     if isinstance(event, updateAuthorizationState):
    #         auth_state = event.authorization_state
    #         if isinstance(auth_state, authorizationStateWaitTdlibParameters):
    #             await self.api.set_tdlib_parameters(
    #                 application_version="1.0",
    #                 database_directory="tdlib_db",
    #                 use_message_database=True,
    #                 api_id=0000,
    #                 api_hash="YOUR_API_HASH",  # Replace this
    #                 system_language_code="en",
    #                 device_model="Desktop",
    #             )

"""
async def my_simple_filter(ctx):
    return ctx.update.message.sender_id == 12345

@client.on(updateNewMessage, filters=my_simple_filter)
"""
# --- Test and execution section ---

# # --- Example of final usage ---
#
# async def test_execution():
#     # 1. Create the central manager
#     manager = ClientManager()
#
#     # 2. Create the client and pass the manager
#     client = TdClient(manager)
#
#     # 3. Register handlers from OUTSIDE
#     @client.on(updateAuthorizationState)
#     async def auth_handler(ctx: Context):
#         # Your login logic here
#         print(ctx)
#
#     # 4. Start the client runner
#     runner = asyncio.create_task(client.run_forever())
#
#     try:
#         # Test a basic method
#         version_data = await client.api.get_option(name="version")
#         print(f"✅ TDLib Version: {version_data}")
#         await asyncio.sleep(10)
#     finally:
#         runner.cancel()

# if __name__ == "__main__":
#     try:
#         asyncio.run(test_execution())
#     except KeyboardInterrupt:
#         pass
