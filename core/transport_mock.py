"""
Mock TDLib transport for testing
"""

import asyncio




class MockTransport:
    """Mock transport for testing without real TDLib

    Allows injecting responses for unit tests.
    """

    def __init__(self):
        self.sent: list[tuple[int, str]] = []
        self._responses: asyncio.Queue = asyncio.Queue()
        self._next_client_id: int = 1

    async def send(self, client_id: int, data: str) -> None:
        """Record sent data

        Args:
            client_id: TDLib client ID
            data: JSON string (recorded for assertions)
        """
        self.sent.append((client_id, data))

    async def receive(self, timeout: float) -> str | None:
        """Get next injected response

        Args:
            timeout: Timeout in seconds

        Returns:
            Injected response or None if timeout
        """
        try:
            return await asyncio.wait_for(self._responses.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None

    def push_response(self, data: str) -> None:
        """Inject a response for testing

        Args:
            data: JSON response to return on next receive()
        """
        self._responses.put_nowait(data)

    def create_client_id(self) -> int:
        """Create a new client ID

        Returns:
            New mock client ID
        """
        client_id = self._next_client_id
        self._next_client_id += 1
        return client_id

    def destroy_client(self, client_id: int) -> None:
        """Destroy a client (no-op in mock)

        Args:
            client_id: Client ID to destroy
        """
        pass

    def clear_sent(self) -> None:
        """Clear sent messages history (for testing)"""
        self.sent.clear()

    def clear_responses(self) -> None:
        """Clear response queue (for testing)"""
        self._responses = asyncio.Queue()
