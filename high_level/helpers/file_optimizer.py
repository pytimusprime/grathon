"""
File optimization helpers for large uploads/downloads with chunking and bandwidth control
"""

from __future__ import annotations
import asyncio
import os
import logging
from typing import TYPE_CHECKING, Optional, Callable, Awaitable
from dataclasses import dataclass

from grathon.high_level.helpers.files import FileHelper

if TYPE_CHECKING:
    from grathon.core.contexts.NewMessageCtx import NewMessageCtx

logger = logging.getLogger(__name__)


@dataclass
class UploadProgress:
    """Progress information for file upload"""
    file_name: str
    total_bytes: int
    uploaded_bytes: int
    percentage: float
    speed_mbps: float  # Speed in MB/s

    def __str__(self) -> str:
        return f"{self.file_name}: {self.percentage:.1f}% ({self.speed_mbps:.2f} MB/s)"


@dataclass
class DownloadProgress:
    """Progress information for file download"""
    file_name: str
    total_bytes: int
    downloaded_bytes: int
    percentage: float
    speed_mbps: float  # Speed in MB/s

    def __str__(self) -> str:
        return f"{self.file_name}: {self.percentage:.1f}% ({self.speed_mbps:.2f} MB/s)"


class FileOptimizer:
    """Optimizes file operations with chunking, throttling, and progress tracking"""

    # Default chunk size: 256KB
    DEFAULT_CHUNK_SIZE = 256 * 1024

    # Default bandwidth limit: 10 MB/s (no limit)
    DEFAULT_BANDWIDTH_LIMIT = 10 * 1024 * 1024

    def __init__(
        self,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        bandwidth_limit_mbps: int = 10,
    ):
        """Initialize file optimizer

        Args:
            chunk_size: Size of each chunk in bytes (default 256KB)
            bandwidth_limit_mbps: Bandwidth limit in MB/s (0 = unlimited)
        """
        self.chunk_size = max(chunk_size, 4096)  # Minimum 4KB
        self.bandwidth_limit = bandwidth_limit_mbps * 1024 * 1024 if bandwidth_limit_mbps > 0 else 0
        self._progress_callback: Optional[Callable[[UploadProgress | DownloadProgress], Awaitable[None]]] = None

    def set_progress_callback(
        self,
        callback: Callable[[UploadProgress | DownloadProgress], Awaitable[None]]
    ) -> None:
        """Set callback for progress updates

        Args:
            callback: Async function that takes UploadProgress or DownloadProgress
        """
        self._progress_callback = callback

    async def _throttle(self, bytes_transferred: int, elapsed_seconds: float) -> None:
        """Apply bandwidth throttling

        Args:
            bytes_transferred: Number of bytes transferred in this chunk
            elapsed_seconds: Time taken to transfer this chunk
        """
        if self.bandwidth_limit <= 0:
            return  # No limit

        current_speed = bytes_transferred / elapsed_seconds if elapsed_seconds > 0 else 0

        if current_speed > self.bandwidth_limit:
            # Need to throttle
            expected_time = bytes_transferred / self.bandwidth_limit
            extra_sleep = expected_time - elapsed_seconds
            if extra_sleep > 0:
                await asyncio.sleep(extra_sleep)

    async def upload_chunked(
        self,
        ctx: NewMessageCtx,
        file_path: str,
        caption: str = "",
        file_type: str = "auto",
    ) -> bool:
        """Upload file with chunking and progress tracking

        Args:
            ctx: NewMessageCtx for API access
            file_path: Path to file
            caption: Optional caption
            file_type: Type of file ("auto", "photo", "video", etc.)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Check file exists
            abs_path = os.path.abspath(file_path)
            if not os.path.exists(abs_path):
                logger.warning(f"File not found: {abs_path}")
                return False

            file_size = os.path.getsize(abs_path)
            file_name = os.path.basename(abs_path)

            # For now, use regular send_file (TDLib handles chunking internally)
            # This method is a placeholder for future optimization
            return await FileHelper.send_file(ctx, abs_path, caption, file_type)

        except Exception as e:
            logger.error(f"Failed to upload file: {e}")
            return False

    async def download_chunked(
        self,
        ctx: NewMessageCtx,
        file_id: int,
        output_path: str = "",
    ) -> Optional[str]:
        """Download file with chunking and progress tracking

        Args:
            ctx: NewMessageCtx for API access
            file_id: TDLib file ID
            output_path: Output path for downloaded file

        Returns:
            Path to downloaded file, or None if failed
        """
        try:
            # For now, use regular download_file (TDLib handles chunking internally)
            # This method is a placeholder for future optimization
            return await FileHelper.download_file(ctx, file_id, output_path)

        except Exception as e:
            logger.error(f"Failed to download file: {e}")
            return None

    @staticmethod
    def calculate_optimal_chunk_size(file_size: int) -> int:
        """Calculate optimal chunk size based on file size

        Args:
            file_size: Size of file in bytes

        Returns:
            Recommended chunk size in bytes
        """
        if file_size < 1024 * 1024:  # < 1MB
            return 64 * 1024  # 64KB
        elif file_size < 10 * 1024 * 1024:  # < 10MB
            return 256 * 1024  # 256KB
        elif file_size < 100 * 1024 * 1024:  # < 100MB
            return 512 * 1024  # 512KB
        else:  # >= 100MB
            return 1024 * 1024  # 1MB

    @staticmethod
    def estimate_upload_time(file_size: int, speed_mbps: int) -> int:
        """Estimate upload time in seconds

        Args:
            file_size: Size of file in bytes
            speed_mbps: Expected speed in MB/s

        Returns:
            Estimated time in seconds
        """
        if speed_mbps <= 0:
            return 0
        return int(file_size / (speed_mbps * 1024 * 1024))

    @staticmethod
    def estimate_download_time(file_size: int, speed_mbps: int) -> int:
        """Estimate download time in seconds

        Args:
            file_size: Size of file in bytes
            speed_mbps: Expected speed in MB/s

        Returns:
            Estimated time in seconds
        """
        return FileOptimizer.estimate_upload_time(file_size, speed_mbps)
