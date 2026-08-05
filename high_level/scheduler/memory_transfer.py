"""In-memory JobTransfer implementation (default backend)."""

from typing import List, Optional, Dict
from datetime import datetime
from .job_transfer import JobTransfer
from .job_data import JobData, JobStatus


class InMemoryJobTransfer(JobTransfer):
    """
    In-memory job storage (no persistence).

    Default backend used when BotScheduler is created without a transfer parameter.
    Jobs are lost when bot restarts.

    Usage:
        scheduler = BotScheduler(bot)  # Uses InMemoryJobTransfer by default
    """

    def __init__(self):
        """Initialize empty job storage."""
        self._jobs: Dict[str, JobData] = {}

    # ─── CRUD Operations ───────────────────────────────────────

    async def save(self, job: JobData) -> str:
        """Save a job to memory."""
        self._jobs[job.job_id] = job
        return job.job_id

    async def get(self, job_id: str) -> Optional[JobData]:
        """Get a job from memory."""
        return self._jobs.get(job_id)

    async def delete(self, job_id: str) -> bool:
        """Delete a job from memory."""
        if job_id in self._jobs:
            del self._jobs[job_id]
            return True
        return False

    async def list_all(self) -> List[JobData]:
        """Get all jobs from memory."""
        return list(self._jobs.values())

    async def update(self, job_id: str, **fields) -> bool:
        """Update specific fields of a job."""
        if job_id not in self._jobs:
            return False

        job = self._jobs[job_id]
        for key, value in fields.items():
            if hasattr(job, key):
                setattr(job, key, value)

        return True

    # ─── Status & Tracking ─────────────────────────────────────

    async def set_status(self, job_id: str, status: str) -> bool:
        """Set job status."""
        return await self.update(job_id, status=status)

    async def update_last_run(self, job_id: str, ran_at: datetime) -> bool:
        """Update when job last ran."""
        return await self.update(job_id, last_run=ran_at)

    async def update_next_run(self, job_id: str, next_run: datetime) -> bool:
        """Update next scheduled run time."""
        return await self.update(job_id, next_run=next_run)

    async def mark_failed(self, job_id: str, error: str, increment_count: bool = True) -> bool:
        """Mark job as failed and record error."""
        if job_id not in self._jobs:
            return False

        job = self._jobs[job_id]
        job.status = JobStatus.FAILED.value
        job.last_error = error

        if increment_count:
            job.error_count += 1

        return True

    # ─── Queries ───────────────────────────────────────────────

    async def get_active(self) -> List[JobData]:
        """Get all active jobs."""
        return [j for j in self._jobs.values() if j.status == JobStatus.ACTIVE.value]

    async def get_failed(self) -> List[JobData]:
        """Get all failed jobs."""
        return [j for j in self._jobs.values() if j.status == JobStatus.FAILED.value]

    async def exists(self, job_id: str) -> bool:
        """Check if job exists."""
        return job_id in self._jobs

    # ─── Utility ────────────────────────────────────────────────

    async def clear(self) -> None:
        """Clear all jobs (useful for testing)."""
        self._jobs.clear()

    async def debug_dump(self) -> Dict[str, JobData]:
        """Return raw jobs dict (for debugging)."""
        return self._jobs.copy()
