"""
Centralized manager for TDLib clients.
"""

import asyncio
import json
import tdjson
from typing import Dict, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from grathon.tdclient import TdClient  # pyright: ignore [reportMissingImports]

class ClientManager:
    """
    Centralized manager to poll updates from TDLib and route them to correct clients.
    """
    def __init__(self):
        # Dictionary to map client_id to its TdClient instance
        super().__init__()
        self.clients: Dict[int, 'TdClient'] = {}
        self.task: Optional[asyncio.Task[None]] = None

    def add_client(self, client_id: int, client_instance: 'TdClient'):
        """Registers a new client to the manager's routing table."""
        self.clients[client_id] = client_instance

    async def _poll_loop(self) -> None:
        """The single global loop for td_receive."""
        loop = asyncio.get_running_loop()
        while True:
            # Global receive from the shared TDLib queue via executor
            result = await loop.run_in_executor(None, tdjson.td_receive, 0.0)
            if not result:
                await asyncio.sleep(0.01)
                continue

            # Process single result (no inner loop to block event loop)
            data = json.loads(result)
            client_id = data.get("@client_id")

            if client_id in self.clients:
                if "@extra" in data:
                    self.clients[client_id].put_extra(data)
                else:
                    self.clients[client_id].put_update(data)
            elif not client_id and self.clients:
                # Broadcast global updates (no client_id) to all registered clients
                for c in self.clients.values():
                    if "@extra" in data:
                        c.put_extra(data)
                    else:
                        c.put_update(data)

    def start(self):
        """Starts the global polling if not already running."""
        if not self.task:
            self.task = asyncio.create_task(self._poll_loop())