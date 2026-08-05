"""Callback data compression system for handling Telegram's 64-byte limit

Uses zlib compression + base64 encoding:
- Fully reversible without server-side storage
- Stable across bot restarts
- Deterministic (same input = same output)
- Works with any length of data
"""

import zlib
import base64
import json
from typing import Optional


class CallbackStore:
    """Reversible callback data compression for Telegram's 64-byte limit

    Uses zlib + base64 compression:
    - `register()`: Compress and encode callback data
    - `resolve()`: Decompress and decode to original data
    - `is_encoded()`: Check if a string looks like encoded callback data
    """

    # Marker to identify encoded callback data (base64-like but with marker)
    ENCODING_PREFIX = "__cb_"
    MAGIC_PREFIX = "__GR_COMPRESSED__"

    @classmethod
    def register(cls, data: str | bytes | dict) -> str:
        """Compress and encode callback data

        Args:
            data: String, bytes, or dict to compress

        Returns:
            Encoded string that can be reversed with resolve()
        """
        data_str = _to_str(data)

        # Compress with zlib
        compressed = zlib.compress(data_str.encode('utf-8'))

        # Encode to base64 for safe transmission
        encoded = base64.b64encode(compressed).decode('ascii')

        # Add magic prefix so resolve() can distinguish from plain data
        return cls.MAGIC_PREFIX + encoded

    @classmethod
    def resolve(cls, encoded_id: str) -> Optional[str]:
        """Decompress and decode callback data

        Args:
            encoded_id: The encoded string returned by register()

        Returns:
            Original data as string, or None if decompression fails
        """
        # Check for magic prefix first
        if not encoded_id.startswith(cls.MAGIC_PREFIX):
            return None

        try:
            # Strip magic prefix and decode from base64
            b64_data = encoded_id[len(cls.MAGIC_PREFIX):]
            compressed = base64.b64decode(b64_data.encode('ascii'))

            # Decompress with zlib
            data_str = zlib.decompress(compressed).decode('utf-8')

            return data_str
        except Exception:
            return None

    @classmethod
    def clear(cls, encoded_id: str) -> None:
        """No-op for compatibility. Compression doesn't require storage."""
        pass

    @classmethod
    def is_encoded(cls, data: str) -> bool:
        """Check if a string looks like encoded callback data

        Returns True if:
        - Starts with MAGIC_PREFIX
        - Can be successfully decoded as base64 and decompressed
        """
        if not isinstance(data, str) or len(data) < len(cls.MAGIC_PREFIX) + 10:
            return False

        # Check for magic prefix first
        if not data.startswith(cls.MAGIC_PREFIX):
            return False

        result = cls.resolve(data)
        return result is not None


def _to_str(data: str | bytes | dict) -> str:
    """Convert any callback data to string for compression"""
    if isinstance(data, dict):
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    if isinstance(data, bytes):
        return data.decode('utf-8', errors='replace')
    return data
