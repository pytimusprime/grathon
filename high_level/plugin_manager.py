"""Plugin system for Grathon bot framework.

Allows dynamic loading, unloading, and reloading of Telegram bot handlers
from Python files with a simple convention (PLUGIN_NAME, PLUGIN_VERSION,
PLUGIN_DESCRIPTION, and setup function).
"""

from __future__ import annotations

import asyncio
import importlib
import importlib.util
import os
import re
import shutil
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Any

from grathon.core.router import Router
from grathon.core.eventhandler import EventHandler
from grathon.core.TLSchema_Manager.tltypes import Update, updateNewMessage
from grathon.high_level.filters import F
from grathon.high_level.conversations import conversation_middleware, ConversationStore

if TYPE_CHECKING:
    from grathon.grathon_bot import GrathonBot
    from grathon.core.tdclient import TdClient

# Type alias: Can be GrathonBot or TdClient
PluginTarget = Any  # GrathonBot | TdClient


class PluginState(Enum):
    """State of a plugin (loaded, unloaded, or error)"""
    LOADED = auto()
    UNLOADED = auto()
    ERROR = auto()


@dataclass
class PluginRecord:
    """Metadata and state for a loaded/unloaded plugin"""
    name: str
    version: str
    description: str
    file_path: str
    state: PluginState
    handlers: list[EventHandler] = field(default_factory=list)
    error_message: Optional[str] = None
    module_name: str = ""   # sys.modules key for importlib.reload()


@dataclass
class PluginManagerTexts:
    """Customizable text strings for the plugin manager admin UI."""
    welcome: str = "Plugin Manager ready. Send /plugins to see installed plugins."
    plugins_empty: str = "No plugins installed yet."
    plugins_header: str = "Installed plugins:\n"
    plugin_row_loaded: str = "  • {name} v{version} — LOADED\n    {description}\n"
    plugin_row_unloaded: str = "  • {name} v{version} — UNLOADED\n"
    plugin_row_error: str = "  • {name} — ERROR: {error}\n"
    upload_prompt: str = (
        "Send me the plugin file.\n\n"
        "Accepted:\n"
        "  • Single `.py` file (simple plugin)\n"
        "  • `.zip` archive (multi-file plugin — must contain exactly **one**\n"
        "    top-level folder with `__init__.py` inside, no loose files)\n\n"
        "Plugin entry-point format:\n"
        "```\n"
        "PLUGIN_NAME = \"my_plugin\"\n"
        "PLUGIN_VERSION = \"1.0.0\"\n"
        "PLUGIN_DESCRIPTION = \"My description\"\n\n"
        "def setup(router):\n"
        "    from grathon.high_level import F\n"
        "    from grathon.core.TLSchema_Manager.tltypes import updateNewMessage\n"
        "    \n"
        "    @router.on(updateNewMessage, filters=[F.command(\"hello\")])\n"
        "    async def hello(ctx):\n"
        "        await ctx.reply(\"Hello from plugin!\")\n"
        "```"
    )
    upload_not_py: str = "Only .py or .zip files are accepted."
    upload_zip_invalid: str = "ZIP rejected: {reason}"
    upload_zip_success: str = "Plugin folder '{name}' extracted"
    upload_success: str = "Plugin '{name}' saved"
    upload_timeout: str = "Upload timed out. Send /upload again."
    reload_success: str = "Plugin '{name}' reloaded. {count} handler(s) active."
    reload_not_found: str = "Plugin '{name}' not found. Upload it first with /upload."
    reload_error: str = "Failed to reload '{name}':\n{error}"
    reload_all_success: str = "✅ Reloaded {count} plugin(s). {loaded} loaded, {errors} error(s)."
    reload_all_empty: str = "No plugins to reload."
    rescan_success: str = "🔄 Rescanned {total} plugins. {new} new, {reloaded} reloaded, {loaded} loaded, {errors} error(s)."
    rescan_empty: str = "No plugin files found."
    unload_success: str = "Plugin '{name}' unloaded."
    unload_not_found: str = "Plugin '{name}' not found."
    delete_success: str = "Plugin '{name}' deleted successfully."
    delete_not_found: str = "Plugin '{name}' not found to delete."
    delete_error: str = "Failed to delete plugin '{name}': {error}"
    export_success: str = "Plugin '{name}' exported."
    export_not_found: str = "Plugin '{name}' not found to export."
    export_error: str = "Failed to export plugin '{name}': {error}"
    not_admin: str = "You are not authorized to manage plugins."
    download_error: str = "Failed to download the file from Telegram."


class PluginManager:
    """Manages plugin lifecycle with built-in Telegram admin commands.

    Args:
        target: GrathonBot OR TdClient instance to attach to.
        admin_ids: Telegram user IDs allowed to manage plugins.
        plugin_dir: Directory where plugin .py files are stored.
        texts: Optional PluginManagerTexts for customizing messages.
        conversation_timeout: Seconds to wait during file upload (default 120).
    """

    def __init__(
        self,
        target: PluginTarget,
        admin_ids: list[int],
        plugin_dir: str = "./plugins",
        texts: Optional[PluginManagerTexts] = None,
        conversation_timeout: float = 120.0,
    ) -> None:
        # Duck typing: GrathonBot has _client, TdClient is the client itself
        if hasattr(target, '_client') and hasattr(target._client, 'add_handler'):
            # It's a GrathonBot
            self._bot = target
            self._client = target._client
        elif hasattr(target, 'add_handler') and hasattr(target, 'include_router'):
            # It's a TdClient
            self._bot = None
            self._client = target
        else:
            raise TypeError(
                f"PluginManager target must be GrathonBot or TdClient, got {type(target).__name__}"
            )

        self._admin_ids = set(admin_ids)
        self._plugin_dir = plugin_dir
        self._texts = texts or PluginManagerTexts()
        self._conversation_timeout = conversation_timeout
        self._plugins: dict[str, PluginRecord] = {}

        os.makedirs(plugin_dir, exist_ok=True)

        # Install conversation middleware once (guard against duplicate)
        if conversation_middleware not in self._client._middlewares:
            self._client.use(conversation_middleware)

        # Create router for admin commands (protected from reload)
        self._admin_router = Router(name="plugin_manager_admin")
        self._register_admin_commands()

        # Include admin router to protect from reload
        if hasattr(self._client, 'include_router'):
            self._client.include_router(self._admin_router)

        self._autoload_existing()

    # ── Public API ───────────────────────────────────────────────────

    def load(self, file_path: str) -> PluginRecord:
        """Load a plugin from file path.

        Returns PluginRecord (check .state for LOADED vs ERROR).
        """
        try:
            # Load the module
            module, module_name = self._load_module(file_path)

            # Validate plugin structure
            self._validate_plugin_module(module)

            # Extract metadata
            name = module.PLUGIN_NAME
            version = module.PLUGIN_VERSION
            description = module.PLUGIN_DESCRIPTION

            # Check for duplicate already loaded
            if name in self._plugins and self._plugins[name].state == PluginState.LOADED:
                return PluginRecord(
                    name=name,
                    version=version,
                    description=description,
                    file_path=file_path,
                    state=PluginState.ERROR,
                    error_message=f"Plugin '{name}' is already loaded",
                    module_name=module_name,
                )

            # Create isolated router for this plugin
            plugin_router = Router(name=f"plugin:{name}")

            # Call plugin's setup function
            module.setup(plugin_router)

            # Add handlers to client dispatch list
            for handler in plugin_router.handlers:
                self._client.add_handler(handler)

            # Create and store PluginRecord
            record = PluginRecord(
                name=name,
                version=version,
                description=description,
                file_path=file_path,
                state=PluginState.LOADED,
                handlers=list(plugin_router.handlers),  # Same objects, tracked by identity
                module_name=module_name,
            )

            self._plugins[name] = record
            return record

        except (ImportError, ValueError, AttributeError, TypeError) as e:
            # Fallback name from filename
            name = Path(file_path).stem
            error_msg = f"{type(e).__name__}: {str(e)}"

            record = PluginRecord(
                name=name,
                version="",
                description="",
                file_path=file_path,
                state=PluginState.ERROR,
                error_message=error_msg,
                module_name="",
            )

            if name not in self._plugins or self._plugins[name].state != PluginState.LOADED:
                self._plugins[name] = record

            return record

    def unload(self, name: str) -> bool:
        """Unload a plugin by removing its handlers.

        Returns True if unloaded, False if not found.
        """
        if name not in self._plugins:
            return False

        record = self._plugins[name]

        # Remove all handlers belonging to this plugin
        for handler in record.handlers:
            self._client.remove_handler(handler)

        record.handlers.clear()
        record.state = PluginState.UNLOADED
        return True

    def reload(self, name: str) -> PluginRecord:
        """Reload a plugin (unload + remove from cache + reload).

        If plugin doesn't exist, treats first load as reload.
        Returns updated PluginRecord.
        """
        if name not in self._plugins:
            return PluginRecord(
                name=name,
                version="",
                description="",
                file_path="",
                state=PluginState.ERROR,
                error_message=f"Plugin '{name}' not found",
            )

        record = self._plugins[name]
        file_path = record.file_path

        # Unload old version
        self.unload(name)

        # Remove module + submodules from sys.modules cache to force reimport
        self._purge_module(record.module_name)

        # Load fresh (will reimport from file or folder)
        return self.load(file_path)

    def reload_all(self) -> list[PluginRecord]:
        """Reload all plugins and return their records."""
        results = []
        for name in list(self._plugins.keys()):
            record = self.reload(name)
            results.append(record)
        return results

    def rescan_all(self) -> tuple[list[PluginRecord], int, int, int]:
        """Rescan plugin directory for new files and reload all.

        Returns:
            (all_results, new_count, reloaded_count, error_count)
        """
        if not os.path.isdir(self._plugin_dir):
            return [], 0, 0, 0

        discovered = self._discover_plugins()  # {plugin_name: path}

        new_count = 0
        reloaded_count = 0
        results = []

        # Reload existing plugins
        for name in list(self._plugins.keys()):
            if name in discovered:
                record = self.reload(name)
                results.append(record)
                reloaded_count += 1

        # Load new plugins
        for plugin_name, plugin_path in discovered.items():
            if plugin_name not in self._plugins:
                record = self.load(plugin_path)
                results.append(record)
                new_count += 1

        loaded_count = sum(1 for r in results if r.state == PluginState.LOADED)
        error_count = sum(1 for r in results if r.state == PluginState.ERROR)

        return results, new_count, reloaded_count, error_count

    def get(self, name: str) -> Optional[PluginRecord]:
        """Get PluginRecord by name or None."""
        return self._plugins.get(name)

    def list_all(self) -> list[PluginRecord]:
        """Return all plugins sorted by name."""
        return sorted(self._plugins.values(), key=lambda r: r.name)

    # ── Private helpers ──────────────────────────────────────────────

    def _load_module(self, plugin_path: str) -> tuple[object, str]:
        """Import a plugin from either a .py file OR a package folder.

        For folders, the entry point is `<folder>/__init__.py` and the package's
        own directory is added as a submodule search path so relative imports
        inside the package (e.g. `from .helpers import x`) resolve correctly.

        Returns (module, module_name) where module_name is the sys.modules key.
        """
        p = Path(plugin_path)

        if p.is_dir():
            init_file = p / "__init__.py"
            if not init_file.is_file():
                raise ValueError(
                    f"Plugin folder '{p.name}' is missing __init__.py"
                )
            module_name = f"grathon_plugin_{p.name}"
            spec = importlib.util.spec_from_file_location(
                module_name,
                str(init_file),
                submodule_search_locations=[str(p)],
            )
        else:
            module_name = f"grathon_plugin_{p.stem}"
            spec = importlib.util.spec_from_file_location(module_name, str(p))

        if spec is None or spec.loader is None:
            raise ValueError(f"Cannot load module from {plugin_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        return module, module_name

    @staticmethod
    def _is_zip_metadata(name: str) -> bool:
        """Filter macOS / editor noise that often shows up inside ZIPs."""
        if not name:
            return True
        if name.startswith("__MACOSX/") or name == "__MACOSX":
            return True
        base = name.rsplit("/", 1)[-1]
        return base in (".DS_Store", "Thumbs.db")

    @classmethod
    def _validate_zip(cls, zip_path: str) -> str:
        """Verify the ZIP is a single-folder plugin package; return folder name.

        Rules (rejected with a clear reason if violated):
          • Must be a real, readable ZIP file
          • Top level must contain exactly ONE directory and no loose files
          • That directory must contain `__init__.py`
          • No path traversal (`..`, absolute paths)
        """
        try:
            zf = zipfile.ZipFile(zip_path)
        except zipfile.BadZipFile as e:
            raise ValueError(f"not a valid ZIP archive ({e})")

        with zf:
            names = [n for n in zf.namelist() if not cls._is_zip_metadata(n)]
            if not names:
                raise ValueError("archive is empty")

            top_dirs: set[str] = set()
            top_files: list[str] = []
            for name in names:
                # Reject path traversal up front
                if name.startswith("/") or ".." in Path(name).parts:
                    raise ValueError(f"unsafe path in archive: '{name}'")
                parts = name.split("/")
                if len(parts) == 1 or (len(parts) == 2 and parts[1] == ""):
                    if name.endswith("/"):
                        top_dirs.add(parts[0])
                    else:
                        top_files.append(name)
                else:
                    top_dirs.add(parts[0])

            if top_files:
                raise ValueError(
                    "archive must contain a single top-level folder, "
                    f"but loose file(s) were found at the root: {top_files[:3]}"
                )
            if len(top_dirs) != 1:
                raise ValueError(
                    f"archive must contain exactly one top-level folder, "
                    f"found {len(top_dirs)}: {sorted(top_dirs)[:5]}"
                )

            folder = next(iter(top_dirs))
            if not re.match(r"^[a-z][a-z0-9_]*$", folder):
                raise ValueError(
                    f"folder name '{folder}' must match ^[a-z][a-z0-9_]*$"
                )

            init_path = f"{folder}/__init__.py"
            if init_path not in names:
                raise ValueError(
                    f"top-level folder '{folder}' is missing __init__.py"
                )

            return folder

    @staticmethod
    def _extract_zip(zip_path: str, dest_dir: str, expected_folder: str) -> None:
        """Extract a pre-validated ZIP into dest_dir.

        Uses a temp dir as a staging area so a half-extracted archive never
        ends up in the live plugin directory.
        """
        with tempfile.TemporaryDirectory() as staging:
            with zipfile.ZipFile(zip_path) as zf:
                # Re-check zip-slip on extraction in case namelist() lied
                staging_root = os.path.realpath(staging)
                for member in zf.namelist():
                    target = os.path.realpath(os.path.join(staging, member))
                    if not target.startswith(staging_root + os.sep) and target != staging_root:
                        raise ValueError(f"unsafe path during extraction: {member}")
                zf.extractall(staging)

            staged_folder = os.path.join(staging, expected_folder)
            if not os.path.isdir(staged_folder):
                raise ValueError(
                    f"expected folder '{expected_folder}' not present after extraction"
                )
            shutil.move(staged_folder, os.path.join(dest_dir, expected_folder))

    @staticmethod
    def _purge_module(module_name: str) -> None:
        """Remove a module and all its submodules from sys.modules.

        Folder plugins import submodules (`grathon_plugin_foo.helpers` etc.);
        on reload we must clear the whole subtree so the next import is fresh.
        """
        if not module_name:
            return
        prefix = module_name + "."
        for key in list(sys.modules.keys()):
            if key == module_name or key.startswith(prefix):
                del sys.modules[key]

    def _validate_plugin_module(self, module: object) -> None:
        """Validate that a plugin module has required attributes.

        Raises ValueError if missing required structure.
        """
        # Check PLUGIN_NAME
        if not hasattr(module, "PLUGIN_NAME"):
            raise ValueError("Plugin missing 'PLUGIN_NAME'")
        if not isinstance(module.PLUGIN_NAME, str):
            raise ValueError("PLUGIN_NAME must be a string")
        if not re.match(r"^[a-z][a-z0-9_]*$", module.PLUGIN_NAME):
            raise ValueError(
                f"PLUGIN_NAME must match ^[a-z][a-z0-9_]*$ (got '{module.PLUGIN_NAME}')"
            )

        # Check PLUGIN_VERSION
        if not hasattr(module, "PLUGIN_VERSION"):
            raise ValueError("Plugin missing 'PLUGIN_VERSION'")
        if not isinstance(module.PLUGIN_VERSION, str):
            raise ValueError("PLUGIN_VERSION must be a string")

        # Check PLUGIN_DESCRIPTION
        if not hasattr(module, "PLUGIN_DESCRIPTION"):
            raise ValueError("Plugin missing 'PLUGIN_DESCRIPTION'")
        if not isinstance(module.PLUGIN_DESCRIPTION, str):
            raise ValueError("PLUGIN_DESCRIPTION must be a string")

        # Check setup function
        if not hasattr(module, "setup"):
            raise ValueError("Plugin missing 'setup' function")
        if not callable(module.setup):
            raise ValueError("'setup' must be callable")

    def _autoload_existing(self) -> None:
        """Load every plugin (single .py file or package folder) in plugin_dir."""
        if not os.path.isdir(self._plugin_dir):
            return
        for plugin_path in self._discover_plugins().values():
            self.load(plugin_path)  # Errors are recorded on the PluginRecord, not raised

    def _discover_plugins(self) -> dict[str, str]:
        """Scan plugin_dir for plugin entries.

        A plugin entry is either:
        - A `.py` file (not starting with `_`), name = stem
        - A directory containing `__init__.py` (not starting with `_` or `.`,
          and not `__pycache__`), name = folder name

        Returns: {plugin_name: absolute_path}
        """
        found: dict[str, str] = {}
        for entry in os.listdir(self._plugin_dir):
            if entry.startswith("_") or entry.startswith("."):
                continue
            full = os.path.join(self._plugin_dir, entry)
            if os.path.isfile(full) and entry.endswith(".py"):
                found[entry[:-3]] = full
            elif os.path.isdir(full) and entry != "__pycache__":
                if os.path.isfile(os.path.join(full, "__init__.py")):
                    found[entry] = full
        return found

    def _register_admin_commands(self) -> None:
        """Wire /plugins, /upload, /reload, /reload_all, /unload, /rescan_plugins, /plugin_help commands via router."""
        admin_filter = F.from_user(*self._admin_ids)

        @self._admin_router.on(updateNewMessage, filters=[F.command("plugins") & admin_filter])
        async def cmd_plugins(ctx):
            await self._cmd_plugins(ctx)

        @self._admin_router.on(updateNewMessage, filters=[F.command("upload") & admin_filter])
        async def cmd_upload(ctx):
            await self._cmd_upload(ctx)

        @self._admin_router.on(updateNewMessage, filters=[F.command("reload") & admin_filter])
        async def cmd_reload(ctx):
            await self._cmd_reload(ctx)

        @self._admin_router.on(updateNewMessage, filters=[F.command("reload_all") & admin_filter])
        async def cmd_reload_all(ctx):
            await self._cmd_reload_all(ctx)

        @self._admin_router.on(updateNewMessage, filters=[F.command("rescan_plugins") & admin_filter])
        async def cmd_rescan(ctx):
            await self._cmd_rescan_plugins(ctx)

        @self._admin_router.on(updateNewMessage, filters=[F.command("unload") & admin_filter])
        async def cmd_unload(ctx):
            await self._cmd_unload(ctx)

        @self._admin_router.on(updateNewMessage, filters=[F.command("plugin_help") & admin_filter])
        async def cmd_help(ctx):
            await self._cmd_plugin_help(ctx)

        @self._admin_router.on(updateNewMessage, filters=[F.command("delete") & admin_filter])
        async def cmd_delete(ctx):
            await self._cmd_delete(ctx)

        @self._admin_router.on(updateNewMessage, filters=[F.command("export_plugin") & admin_filter])
        async def cmd_export(ctx):
            await self._cmd_export_plugin(ctx)

    def _is_admin(self, ctx) -> bool:
        """Check if ctx sender is in admin_ids."""
        return ctx.sender_id.user_id in self._admin_ids

    # ── Admin command handlers ────────────────────────────────────────

    async def _cmd_plugins(self, ctx) -> None:
        """Handle /plugins — list all plugins with state."""
        if not self._is_admin(ctx):
            return await ctx.reply(self._texts.not_admin)

        plugins = self.list_all()
        if not plugins:
            return await ctx.reply(self._texts.plugins_empty)

        message = self._texts.plugins_header
        for record in plugins:
            if record.state == PluginState.LOADED:
                message += self._texts.plugin_row_loaded.format(
                    name=record.name,
                    version=record.version,
                    description=record.description,
                )
            elif record.state == PluginState.UNLOADED:
                message += self._texts.plugin_row_unloaded.format(
                    name=record.name,
                    version=record.version,
                )
            else:  # ERROR
                message += self._texts.plugin_row_error.format(
                    name=record.name,
                    error=record.error_message or "Unknown error",
                )

        await ctx.reply_markdown(message)

    async def _cmd_upload(self, ctx) -> None:
        """Handle /upload — Conversation flow for file upload."""
        if not self._is_admin(ctx):
            return await ctx.reply(self._texts.not_admin)

        await ctx.reply_markdown(self._texts.upload_prompt)

        # Use ConversationStore directly to wait for document
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        ConversationStore.register_message(ctx.chat_id, ctx.sender_id.user_id, future)

        try:
            doc_ctx = await asyncio.wait_for(future, timeout=self._conversation_timeout)
        except asyncio.TimeoutError:
            return await ctx.reply(self._texts.upload_timeout)

        # Check if message is a document
        if not doc_ctx.is_document:
            return await ctx.reply(self._texts.upload_not_py)

        # Extract filename and file_id
        try:
            msg_content = doc_ctx.update.message.content  # messageDocument
            doc = msg_content.document  # document class
            filename = doc.file_name
            file_id = doc.document.id  # file class
            print(f"📥 Upload: filename={filename}, file_id={file_id}")
        except (AttributeError, IndexError) as e:
            print(f"❌ Extract error: {e}")
            return await ctx.reply(self._texts.download_error)

        is_py = filename.endswith(".py")
        is_zip = filename.endswith(".zip")
        if not (is_py or is_zip):
            return await ctx.reply(self._texts.upload_not_py)

        # Download file from Telegram
        try:
            print(f"📥 Getting file info for file_id={file_id}")
            # First get file info
            file_info = await doc_ctx.api.get_file(file_id=file_id)
            print(f"✅ File info: {file_info}")

            print(f"📥 Downloading file...")
            # Download file
            file_result = await doc_ctx.api.download_file(
                file_id=file_id,
                priority=32,
                offset=0,
                limit=0,
                synchronous=True,
            )
            print(f"✅ Download result: {file_result}")

            downloaded_path = file_result.local.path
            print(f"✅ Downloaded to: {downloaded_path}")
        except (asyncio.TimeoutError, OSError, RuntimeError, AttributeError) as e:
            print(f"❌ Download error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return await ctx.reply(
                self._texts.download_error + f"\n({type(e).__name__}: {str(e)})"
            )

        if is_py:
            save_path = os.path.join(self._plugin_dir, filename)
            try:
                shutil.copy(downloaded_path, save_path)
            except OSError as e:
                return await ctx.reply(f"Failed to save file: {str(e)}")
            finally:
                # Clean up the temporary downloaded file
                try:
                    if os.path.isfile(downloaded_path):
                        os.remove(downloaded_path)
                except OSError:
                    pass  # Ignore cleanup errors

            plugin_name = filename[:-3]
            await ctx.reply(
                self._texts.upload_success.format(name=plugin_name)
            )
            # Auto-reload the uploaded plugin
            print(f"🔄 Auto-reloading plugin: {plugin_name}")
            record = self.load(save_path)
            if record.state == PluginState.LOADED:
                await ctx.reply(f"✅ Plugin '{plugin_name}' loaded successfully! ({len(record.handlers)} handlers)")
            else:
                await ctx.reply(f"⚠️ Plugin '{plugin_name}' saved but failed to load: {record.error_message}")
            return

        # ── ZIP path: validate strictly, then extract ───────────────────
        try:
            folder_name = self._validate_zip(downloaded_path)
        except ValueError as e:
            return await ctx.reply(
                self._texts.upload_zip_invalid.format(reason=str(e))
            )

        # Conflict: a plugin with this name is currently loaded → unload first
        # so handlers don't double-up after extraction + /reload.
        if folder_name in self._plugins and self._plugins[folder_name].state == PluginState.LOADED:
            self.unload(folder_name)
            self._purge_module(self._plugins[folder_name].module_name)

        # Replace any existing folder/file with the same name
        target_dir = os.path.join(self._plugin_dir, folder_name)
        target_py = target_dir + ".py"
        try:
            if os.path.isdir(target_dir):
                shutil.rmtree(target_dir)
            if os.path.isfile(target_py):
                os.remove(target_py)
            self._extract_zip(downloaded_path, self._plugin_dir, folder_name)
        except (OSError, zipfile.BadZipFile) as e:
            return await ctx.reply(f"Failed to extract zip: {str(e)}")
        finally:
            # Clean up the zip file after extraction (success or failure)
            try:
                if os.path.isfile(downloaded_path):
                    os.remove(downloaded_path)
            except OSError:
                pass  # Ignore cleanup errors

        await ctx.reply(
            self._texts.upload_zip_success.format(name=folder_name)
        )

        # Auto-reload the uploaded plugin
        plugin_path = os.path.join(self._plugin_dir, folder_name)
        print(f"🔄 Auto-reloading plugin: {folder_name}")
        record = self.load(plugin_path)
        if record.state == PluginState.LOADED:
            await ctx.reply(f"✅ Plugin '{folder_name}' loaded successfully! ({len(record.handlers)} handlers)")
        else:
            await ctx.reply(f"⚠️ Plugin '{folder_name}' extracted but failed to load: {record.error_message}")

    async def _cmd_reload(self, ctx) -> None:
        """Handle /reload <name> — reload plugin by name."""
        if not self._is_admin(ctx):
            return await ctx.reply(self._texts.not_admin)

        args = ctx.args
        if not args:
            return await ctx.reply("Usage: /reload <plugin_name>")

        plugin_name = args[0]
        record = self.reload(plugin_name)

        if record.state == PluginState.LOADED:
            await ctx.reply(
                self._texts.reload_success.format(
                    name=record.name,
                    count=len(record.handlers),
                )
            )
        elif record.state == PluginState.UNLOADED:
            await ctx.reply(self._texts.reload_not_found.format(name=plugin_name))
        else:  # ERROR
            await ctx.reply(
                self._texts.reload_error.format(
                    name=plugin_name,
                    error=record.error_message or "Unknown error",
                )
            )

    async def _cmd_reload_all(self, ctx) -> None:
        """Handle /reload_all — reload all plugins."""
        if not self._is_admin(ctx):
            return await ctx.reply(self._texts.not_admin)

        records = self.reload_all()
        if not records:
            return await ctx.reply(self._texts.reload_all_empty)

        loaded = sum(1 for r in records if r.state == PluginState.LOADED)
        errors = sum(1 for r in records if r.state == PluginState.ERROR)

        await ctx.reply(
            self._texts.reload_all_success.format(
                count=len(records),
                loaded=loaded,
                errors=errors,
            )
        )

    async def _cmd_rescan_plugins(self, ctx) -> None:
        """Handle /rescan_plugins — scan for new plugins and reload all."""
        if not self._is_admin(ctx):
            return await ctx.reply(self._texts.not_admin)

        results, new_count, reloaded_count, error_count = self.rescan_all()
        if not results:
            return await ctx.reply(self._texts.rescan_empty)

        loaded = sum(1 for r in results if r.state == PluginState.LOADED)

        await ctx.reply(
            self._texts.rescan_success.format(
                total=len(results),
                new=new_count,
                reloaded=reloaded_count,
                loaded=loaded,
                errors=error_count,
            )
        )

    async def _cmd_unload(self, ctx) -> None:
        """Handle /unload <name> — unload plugin by name."""
        if not self._is_admin(ctx):
            return await ctx.reply(self._texts.not_admin)

        args = ctx.args
        if not args:
            return await ctx.reply("Usage: /unload <plugin_name>")

        plugin_name = args[0]
        success = self.unload(plugin_name)

        if success:
            await ctx.reply(self._texts.unload_success.format(name=plugin_name))
        else:
            await ctx.reply(self._texts.unload_not_found.format(name=plugin_name))

    async def _cmd_delete(self, ctx) -> None:
        """Handle /delete <name> — delete plugin file/folder from disk."""
        if not self._is_admin(ctx):
            return await ctx.reply(self._texts.not_admin)

        args = ctx.args
        if not args:
            return await ctx.reply("Usage: /delete <plugin_name>")

        plugin_name = args[0]

        if plugin_name not in self._plugins:
            return await ctx.reply(self._texts.delete_not_found.format(name=plugin_name))

        record = self._plugins[plugin_name]

        # Unload first if loaded
        if record.state == PluginState.LOADED:
            self.unload(plugin_name)

        # Remove from cache
        self._purge_module(record.module_name)

        # Delete file or folder
        try:
            file_path = Path(record.file_path)
            if file_path.is_dir():
                shutil.rmtree(file_path)
            elif file_path.is_file():
                file_path.unlink()

            # Remove from plugins dict
            del self._plugins[plugin_name]

            await ctx.reply(self._texts.delete_success.format(name=plugin_name))
        except Exception as e:
            await ctx.reply(
                self._texts.delete_error.format(name=plugin_name, error=str(e))
            )

    async def _cmd_export_plugin(self, ctx) -> None:
        """Handle /export_plugin <name> — send plugin file or zipped folder."""
        if not self._is_admin(ctx):
            return await ctx.reply(self._texts.not_admin)

        args = ctx.args
        if not args:
            return await ctx.reply("Usage: /export_plugin <plugin_name>")

        plugin_name = args[0]

        if plugin_name not in self._plugins:
            return await ctx.reply(self._texts.export_not_found.format(name=plugin_name))

        record = self._plugins[plugin_name]
        file_path = Path(record.file_path)

        try:
            if file_path.is_file():
                # Send single .py file directly
                await ctx.reply_file(str(file_path), caption=f"Plugin: {plugin_name}")
            elif file_path.is_dir():
                # Create ZIP for folder
                with tempfile.TemporaryDirectory() as tmpdir:
                    zip_path = Path(tmpdir) / f"{plugin_name}.zip"
                    shutil.make_archive(str(zip_path.with_suffix('')), 'zip', file_path.parent, file_path.name)
                    await ctx.reply_file(str(zip_path), caption=f"Plugin: {plugin_name} (zipped)")
            else:
                return await ctx.reply(self._texts.export_not_found.format(name=plugin_name))

            await ctx.reply(self._texts.export_success.format(name=plugin_name))
        except Exception as e:
            await ctx.reply(
                self._texts.export_error.format(name=plugin_name, error=str(e))
            )

    async def _cmd_plugin_help(self, ctx) -> None:
        """Handle /plugin_help — show admin commands for plugin management."""
        if not self._is_admin(ctx):
            return await ctx.reply(self._texts.not_admin)

        help_text = (
            "🔐 **Admin commands (your user only):**\n\n"
            "  • /plugins — list loaded plugins\n"
            "  • /reload <name> — reload a plugin without restart\n"
            "  • /reload_all — reload all plugins at once\n"
            "  • /rescan_plugins — scan for NEW plugins + reload all\n"
            "  • /upload — upload a plugin (`.py` file or `.zip` archive)\n"
            "  • /export_plugin <name> — download plugin file or folder as ZIP\n"
            "  • /unload <name> — unload a plugin\n"
            "  • /delete <name> — delete a plugin file/folder\n"
            "  • /plugin_help — show this help message"
        )
        await ctx.reply_markdown(help_text)
