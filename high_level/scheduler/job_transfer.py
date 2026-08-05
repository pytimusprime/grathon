"""Abstract JobTransfer interface for persistent job storage."""

from abc import ABC, abstractmethod
from typing import List, Optional, Any
from datetime import datetime
from .job_data import JobData, JobStatus


class JobTransfer(ABC):
    """
    Abstract storage backend for scheduled jobs.

    Implementations must provide persistence and retrieval of job data.
    This allows BotScheduler to work with any storage backend (in-memory, PicoDB, SQL, etc).

    Example custom implementation:
        class PicoDBJobTransfer(JobTransfer):
            def __init__(self, db):
                self.db = db

            async def save(self, job: JobData) -> str:
                job_id = await self.db.insert(job)
                return job_id

            async def get(self, job_id: str) -> Optional[JobData]:
                return await self.db.query().eq('job_id', job_id).search()
            # ... implement other methods
    """

    # ─── CRUD Operations ───────────────────────────────────────

    @abstractmethod
    async def save(self, job: JobData) -> str:
        """
        Save a job (insert or update).

        Args:
            job: JobData object to save

        Returns:
            job_id (str)
        """
        pass

    @abstractmethod
    async def get(self, job_id: str) -> Optional[JobData]:
        """
        Get a job by ID.

        Args:
            job_id: Job identifier

        Returns:
            JobData if found, None otherwise
        """
        pass

    @abstractmethod
    async def delete(self, job_id: str) -> bool:
        """
        Delete a job.

        Args:
            job_id: Job identifier

        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def list_all(self) -> List[JobData]:
        """
        Get all jobs.

        Returns:
            List of all JobData objects
        """
        pass

    @abstractmethod
    async def update(self, job_id: str, **fields) -> bool:
        """
        Update specific fields of a job.

        Args:
            job_id: Job identifier
            **fields: Fields to update (e.g., status="paused", error_count=2)

        Returns:
            True if updated, False if not found
        """
        pass

    # ─── Status & Tracking ─────────────────────────────────────

    @abstractmethod
    async def set_status(self, job_id: str, status: str) -> bool:
        """
        Set job status (active, paused, failed, completed).

        Args:
            job_id: Job identifier
            status: New status (JobStatus enum value)

        Returns:
            True if updated, False if not found
        """
        pass

    @abstractmethod
    async def update_last_run(self, job_id: str, ran_at: datetime) -> bool:
        """
        Update when job last ran.

        Args:
            job_id: Job identifier
            ran_at: Execution timestamp

        Returns:
            True if updated, False if not found
        """
        pass

    @abstractmethod
    async def update_next_run(self, job_id: str, next_run: datetime) -> bool:
        """
        Update next scheduled run time.

        Args:
            job_id: Job identifier
            next_run: Next run timestamp

        Returns:
            True if updated, False if not found
        """
        pass

    @abstractmethod
    async def mark_failed(self, job_id: str, error: str, increment_count: bool = True) -> bool:
        """
        Mark job as failed and record error.

        Args:
            job_id: Job identifier
            error: Error message
            increment_count: Whether to increment error_count

        Returns:
            True if updated, False if not found
        """
        pass

    # ─── Queries ───────────────────────────────────────────────

    @abstractmethod
    async def get_active(self) -> List[JobData]:
        """
        Get all active jobs.

        Returns:
            List of active JobData objects
        """
        pass

    @abstractmethod
    async def get_failed(self) -> List[JobData]:
        """
        Get all failed jobs.

        Returns:
            List of failed JobData objects
        """
        pass

    @abstractmethod
    async def exists(self, job_id: str) -> bool:
        """
        Check if job exists.

        Args:
            job_id: Job identifier

        Returns:
            True if exists, False otherwise
        """
        pass

    # ─── Utility ────────────────────────────────────────────────

    async def count_jobs(self) -> int:
        """Count total jobs."""
        jobs = await self.list_all()
        return len(jobs)

    async def count_active(self) -> int:
        """Count active jobs."""
        jobs = await self.get_active()
        return len(jobs)

    async def count_failed(self) -> int:
        """Count failed jobs."""
        jobs = await self.get_failed()
        return len(jobs)
