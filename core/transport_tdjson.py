"""
Real TDLib transport using tdjson
"""

import asyncio
import tdjson



class TdjsonTransport:
    """Real TDLib transport using tdjson library

    Communicates with actual TDLib through tdjson.
    """

    async def send(self, client_id: int, data: str) -> None:
        """Send data to TDLib

        Args:
            client_id: TDLib client ID
            data: JSON string to send
        """
        tdjson.td_send(client_id, data)  # pyright: ignore [reportArgumentType]

    async def receive(self, timeout: float) -> str | None:
        """Receive data from TDLib

        Args:
            timeout: Timeout in seconds

        Returns:
            JSON string or None if timeout
        """
        loop = asyncio.get_event_loop()
        try:
            return await asyncio.wait_for(  # pyright: ignore [reportReturnType]
                loop.run_in_executor(None, tdjson.td_receive, timeout),
                timeout=timeout + 0.1
            )
        except asyncio.TimeoutError:
            return None

    def create_client_id(self) -> int:
        """Create a new TDLib client ID

        Returns:
            New client ID
        """
        return tdjson.td_create_client_id()

    def destroy_client(self, client_id: int) -> None:
        """Destroy a TDLib client

        Args:
            client_id: Client ID to destroy (TDLib auto-destroys)
        """
        pass
