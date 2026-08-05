"""
Abstract transport protocol for TDLib communication
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class ITdTransport(Protocol):
    """Abstract transport for TDLib communication

    Allows swapping between real TDLib (tdjson) and mock implementations for testing.
    """

    async def send(self, client_id: int, data: str) -> None:
        """Send data to TDLib

        Args:
            client_id: TDLib client ID
            data: JSON string to send
        """
        ...

    async def receive(self, timeout: float) -> str | None:
        """Receive data from TDLib

        Args:
            timeout: Timeout in seconds

        Returns:
            JSON string or None if timeout
        """
        ...

    def create_client_id(self) -> int:
        """Create a new TDLib client ID

        Returns:
            New client ID
        """
        ...

    def destroy_client(self, client_id: int) -> None:
        """Destroy a TDLib client

        Args:
            client_id: Client ID to destroy
        """
        ...
