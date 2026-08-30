"""GrathonBot — User-facing entry point wrapping TdClient, ClientManager, and AuthRouter"""

from pathlib import Path

from grathon.core.TLSchema_Manager.tltypes import updateNewMessage
from grathon.core.clientmanager import ClientManager
from grathon.core.eventhandler import EventHandler
from grathon.core.routers.auth import AuthRouter
from grathon.core.routers.callback_query import CallbackQueryRouter
from grathon.core.routers.inline_query import InlineQueryRouter
from grathon.core.routers.newmessage import NewMessageRouter
from grathon.core.tdclient import TdClient
from grathon.high_level.error_handler import ErrorHandler
from grathon.high_level.filters import F
from grathon.high_level.helpers.file_optimizer import FileOptimizer
from grathon.high_level.helpers.files import FileHelper
from grathon.high_level.session import SessionStore


class GrathonBot:
    """Simple bot API hiding Layer 1 complexity

    Usage:
        bot = GrathonBot(api_id=12345, api_hash="hash", bot_token="TOKEN")

        @bot.on_command("start")
        async def start_handler(ctx):
            await ctx.reply("Welcome!")

        await bot.start()
    """

    def __init__(
            self,
            api_id: int,
            api_hash: str,
            bot_token: str,
            database_directory: str = "bot_db",
            *,
            system_language_code: str = "en",
            device_model: str = "Bot",
            application_version: str = "1.0",
    ):
        """Initialize bot with TDLib parameters and auto-wired authentication

        Args:
            api_id: TDLib API ID
            api_hash: TDLib API hash
            bot_token: Telegram bot token
            database_directory: Path for TDLib database (default: "bot_db")
            system_language_code: System language for TDLib (default: "en")
            device_model: Device model string (default: "Bot")
            application_version: App version for TDLib (default: "1.0")
        """
        self._api_id = api_id
        self._api_hash = api_hash
        self._bot_token = bot_token
        self._database_directory = database_directory
        self._system_language_code = system_language_code
        self._device_model = device_model
        self._application_version = application_version

        # Layer 1 setup
        self._manager = ClientManager()
        self._client = TdClient(self._manager)

        # Auth auto-wired: on_params → set_tdlib_parameters, on_token → check_authentication_bot_token
        self._auth_router = AuthRouter()
        self._auth_router.on_params(self._handle_params)
        self._auth_router.on_token(self._handle_token)
        self._auth_router.on_ready(self._handle_on_ready)
        self._client.include_router(self._auth_router)

        self._new_message_router = NewMessageRouter()
        self._client.include_router(self._new_message_router)

        self.callback_query_router = CallbackQueryRouter()
        self._client.include_router(self.callback_query_router)

        self.inline_query_router = InlineQueryRouter()
        self._client.include_router(self.inline_query_router)

        # Session management
        self.session = SessionStore()
        self._client.session = self.session

        # Error handling
        self._error_handler = ErrorHandler()
        self._client.error_handler = self._error_handler  # Inject into TdClient

        # File optimization
        self.file_optimizer = FileOptimizer()

    @property
    def api(self):
        """
        """
        return self._client.api

    async def _handle_on_ready(self, ctx):
        print("Handle On-Ready", ctx)

    async def _handle_params(self, ctx) -> None:  # pyright: ignore [reportReturnType]
        """Called by TDLib when it needs initialization parameters"""

        await ctx.api.set_tdlib_parameters(
            api_id=self._api_id,
            api_hash=self._api_hash,
            database_directory=self._database_directory,
            files_directory=str(Path(self._database_directory) / "files"),
            system_language_code=self._system_language_code,
            device_model=self._device_model,
            application_version=self._application_version,
            use_file_database=True,
            use_message_database=True,
            use_secret_chats=False,
        )

    async def _handle_token(self, ctx) -> None:
        """Called by TDLib when it needs the bot token"""
        print("....Handle Token....")
        await ctx.api.check_authentication_bot_token(token=self._bot_token)

    def on_command(self, command: str):
        """Register command handler

        Usage:
            @bot.on_command("start")
            async def start_handler(ctx):
                await ctx.reply("Welcome!")

        Args:
            *commands: One or more command names (without /)
        """

        def decorator(func):
            self._client.add_handler(
                EventHandler(
                    updateNewMessage,
                    filters=[F.command(command)],
                    callback=func,
                )
            )

            return func

        return decorator

    def on_message(self, filters=None):
        """Register message handler

        Usage:
            @bot.on_message(filters=[F.text(r"hello")])
            async def hello_handler(ctx):
                await ctx.reply("Hi!")

        Args:
            filters: Filter or list of filters to match messages
        """

        def decorator(func):
            self._new_message_router.on(
                updateNewMessage,
                filters=filters,
                callback=func
            )
            self._client.reload_routers()
            return func

        return decorator

    def on_callback(self, pattern: str | None = None):
        """Register inline button callback handler

        Usage:
            @bot.on_callback(r"^confirm$")
            async def confirm_handler(ctx):
                await ctx.answer("Confirmed!")

        Args:
            pattern: Regex pattern to match callback data
        """

        if pattern is None:
            filter = []
        else:
            filter = [F.callback(pattern)]

        def decorator(func):
            self.callback_query_router.on_callback_query(
                func,
                filters=filter,  # pyright: ignore [reportArgumentType]
            )
            print("reload for callback query")
            self._client.reload_routers()
            return func

        return decorator

    def on_inline_query(self, pattern: str | None = None):
        """Register inline query handler

        Usage:
            @bot.on_inline_query(r"^dog")
            async def search_dogs(ctx):
                results = [...]
                await ctx.answer_results(results)

        Args:
            pattern: Optional regex pattern to match query text
        """

        if pattern is None:
            filter = []
        else:
            filter = [F.query(pattern)]

        def decorator(func):
            self.inline_query_router.on_inline_query(
                func,
                filters=filter,  # pyright: ignore [reportArgumentType]
            )
            self._client.reload_routers()
            return func

        return decorator

    def on(self, event_type: type, filters=None):
        """Register handler for any TDLib update type

        Usage:
            from grathon.core.TLSchema_Manager.tltypes import updateConnectionState

            @bot.on(updateConnectionState)
            async def on_conn(ctx):
                print(f"Connection state: {ctx.update.state}")

        Args:
            event_type: Update type to handle (e.g., updateConnectionState, updateFile)
            filters: Optional filter or list of filters to match the update
        """

        def decorator(func):
            self._client.add_handler(
                EventHandler(
                    event_type,
                    filters=filters or [],
                    callback=func)
            )
            return func

        return decorator

    def include_router(self, router) -> None:
        """Include router from another module

        Args:
            router: Router instance to include
        """
        self._client.include_router(router)

    def use(self, middleware) -> None:
        """Register middleware (logging, conversations, etc.)

        Args:
            middleware: Middleware function to install
        """
        self._client.use(middleware)

    async def start(self) -> None:
        """Start the bot (blocks forever until interrupted)"""
        # Initialize the DB-backed callback store (replaces old compression).
        from grathon.high_level.callback_db import init_callback_db
        try:
            await init_callback_db()
        except Exception as e:
            print(f"[WARN] CallbackDB init failed (callbacks may not resolve): {e}")
        await self._client.run_forever()

    async def stop(self) -> None:
        """Stop the bot gracefully (cancels background tasks, closes TDLib)"""
        await self._client.stop()

    def error_handler(self):
        """Register an error handler for all events

        Usage:
            @bot.error_handler()
            async def handle_error(error, ctx):
                await ctx.reply(f"Error: {error}")

        Args:
            None

        Returns:
            Decorator function
        """

        def decorator(func):
            self._error_handler.add_handler(func)
            return func

        return decorator

    async def send_file(self, chat_id: int, file_path: str, caption: str = "", file_type: str = "auto") -> bool:
        """Send file to a chat

        Usage:
            success = await bot.send_file(chat_id, "/tmp/report.pdf", caption="Report")

        Args:
            chat_id: ID of chat to send file to
            file_path: Path to file
            caption: Optional caption for file
            file_type: Type of file ("auto", "photo", "video", "audio", "document", etc.)

        Returns:
            True if successful, False otherwise
        """

        # Create a temporary context for FileHelper
        class _TempCtx:
            def __init__(self, client, chat_id):
                self.client = client
                self.api = client.api
                self.chat_id = chat_id

        ctx = _TempCtx(self._client, chat_id)
        return await FileHelper.send_file(ctx, file_path, caption, file_type)  # pyright: ignore [reportArgumentType]

    async def download_file(self, file_id: int, output_path: str = "") -> str:
        """Download file from Telegram

        Usage:
            path = await bot.download_file(file_id, "/tmp/myfile.pdf")
            path = await bot.download_file(file_id)  # returns cache path

        Args:
            file_id: TDLib file ID
            output_path: Optional path to save file

        Returns:
            Path to downloaded file, or None if failed
        """

        # Create a temporary context for FileHelper
        class _TempCtx:
            def __init__(self, client):
                self.client = client
                self.api = client.api

        ctx = _TempCtx(self._client)
        return await FileHelper.download_file(ctx, file_id,  # pyright: ignore [reportArgumentType, reportReturnType]
                                              output_path)  # pyright: ignore [reportReturnType, reportArgumentType]

    def set_bandwidth_limit(self, limit_mbps: int) -> None:
        """Set bandwidth limit for file operations

        Usage:
            bot.set_bandwidth_limit(5)  # Limit to 5 MB/s

        Args:
            limit_mbps: Limit in MB/s (0 = unlimited)
        """
        self.file_optimizer.bandwidth_limit = limit_mbps * 1024 * 1024 if limit_mbps > 0 else 0

    def set_chunk_size(self, chunk_size: int) -> None:
        """Set chunk size for file operations

        Usage:
            bot.set_chunk_size(512 * 1024)  # 512KB chunks

        Args:
            chunk_size: Chunk size in bytes (minimum 4KB)
        """
        self.file_optimizer.chunk_size = max(chunk_size, 4096)

    async def get_me(self):
        """Get bot user info from Telegram

        Returns:
            User object with bot information
        """
        return await self._client.api.get_me()
