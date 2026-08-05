"""PicoDB-based JobTransfer implementation for persistent job storage."""

from typing import List, Optional, Any, TYPE_CHECKING
from datetime import datetime
from dataclasses import dataclass, asdict

from .job_transfer import JobTransfer
from .job_data import JobData, JobStatus

if TYPE_CHECKING:
    from picodb import AsyncPicodb


@dataclass
class JobRecord:
    """
    PicoDB dataclass for persistent job storage.

    This is what gets stored in the database.
    Mirrors JobData but optimized for PicoDB serialization.
    """
    job_id: str
    name: str
    trigger: str
    trigger_args: dict  # JSON-serializable dict
    status: str
    created_at: str  # ISO format
    last_run: Optional[str] = None  # ISO format
    next_run: Optional[str] = None  # ISO format
    error_count: int = 0
    last_error: Optional[str] = None


class PicoDBJobTransfer(JobTransfer):
    """
    PicoDB-based job storage with persistent database backend.

    Jobs are automatically saved to database and survive bot restarts.
    Uses AsyncPicodb for async database access.

    Setup:
        from picodb import AsyncPicodb
        from grathon.high_level.scheduler import BotScheduler
        from grathon.high_level.scheduler.picodb_transfer import PicoDBJobTransfer

        # Create PicoDB instance
        db = AsyncPicodb(
            schema_cls=JobRecord,
            path="sqlite+aiosqlite:///bot_jobs.db",
            indexes=[
                {'fields': ['job_id'], 'unique': True},
                {'fields': ['status']},
            ]
        )
        await db.init_db()

        # Create scheduler with PicoDB backend
        scheduler = BotScheduler(bot, transfer=PicoDBJobTransfer(db))

        # Jobs now persist across restarts!
    """

    def __init__(self, db: "AsyncPicodb"):
        """
        Initialize PicoDB transfer.

        Args:
            db: AsyncPicodb instance with JobRecord schema
        """
        self.db = db

    # ─── Helper Methods ────────────────────────────────────────

    @staticmethod
    def _job_data_to_record(job: JobData) -> JobRecord:
        """Convert JobData to JobRecord for storage."""
        return JobRecord(
            job_id=job.job_id,
            name=job.name,
            trigger=job.trigger,
            trigger_args=job.trigger_args,
            status=job.status,
            created_at=job.created_at.isoformat(),
            last_run=job.last_run.isoformat() if job.last_run else None,
            next_run=job.next_run.isoformat() if job.next_run else None,
            error_count=job.error_count,
            last_error=job.last_error,
        )

    @staticmethod
    def _record_to_job_data(record: JobRecord) -> JobData:
        """Convert JobRecord to JobData for use."""
        return JobData(
            job_id=record.job_id,
            name=record.name,
            trigger=record.trigger,
            trigger_args=record.trigger_args,
            status=record.status,
            created_at=datetime.fromisoformat(record.created_at),
            last_run=datetime.fromisoformat(record.last_run) if record.last_run else None,
            next_run=datetime.fromisoformat(record.next_run) if record.next_run else None,
            error_count=record.error_count,
            last_error=record.last_error,
        )

    # ─── CRUD Operations ───────────────────────────────────────

    async def save(self, job: JobData) -> str:
        """
        Save a job to database.

        Args:
            job: JobData to save

        Returns:
            job_id (str)
        """
        record = self._job_data_to_record(job)

        # Check if exists
        existing = await self.db.query().eq("job_id", job.job_id).search()

        if existing:
            # Update
            await self.db.update(existing[0].record_id, record)
        else:
            # Insert
            await self.db.insert(record)

        return job.job_id

    async def get(self, job_id: str) -> Optional[JobData]:
        """
        Get a job from database.

        Args:
            job_id: Job identifier

        Returns:
            JobData if found, None otherwise
        """
        results = await self.db.query().eq("job_id", job_id).search()

        if results:
            return self._record_to_job_data(results[0])

        return None

    async def delete(self, job_id: str) -> bool:
        """
        Delete a job from database.

        Args:
            job_id: Job identifier

        Returns:
            True if deleted, False if not found
        """
        # Find and delete
        count = 0
        results = await self.db.query().eq("job_id", job_id).search()

        if results:
            # PicoDB doesn't have record_id, need to delete by query
            await self.db.query().eq("job_id", job_id).delete()
            return True

        return False

    async def list_all(self) -> List[JobData]:
        """
        Get all jobs from database.

        Returns:
            List of all JobData objects
        """
        records = await self.db.query().search()
        return [self._record_to_job_data(r) for r in records]

    async def update(self, job_id: str, **fields) -> bool:
        """
        Update specific fields of a job.

        Args:
            job_id: Job identifier
            **fields: Fields to update

        Returns:
            True if updated, False if not found
        """
        # Get existing job
        existing = await self.get(job_id)
        if not existing:
            return False

        # Update fields
        for key, value in fields.items():
            if hasattr(existing, key):
                setattr(existing, key, value)

        # Save updated job
        await self.save(existing)
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

    async def mark_failed(
        self, job_id: str, error: str, increment_count: bool = True
    ) -> bool:
        """Mark job as failed and record error."""
        job = await self.get(job_id)
        if not job:
            return False

        job.status = JobStatus.FAILED.value
        job.last_error = error

        if increment_count:
            job.error_count += 1

        await self.save(job)
        return True

    # ─── Queries ───────────────────────────────────────────────

    async def get_active(self) -> List[JobData]:
        """Get all active jobs."""
        records = await self.db.query().eq("status", JobStatus.ACTIVE.value).search()
        return [self._record_to_job_data(r) for r in records]

    async def get_failed(self) -> List[JobData]:
        """Get all failed jobs."""
        records = await self.db.query().eq("status", JobStatus.FAILED.value).search()
        return [self._record_to_job_data(r) for r in records]

    async def exists(self, job_id: str) -> bool:
        """Check if job exists."""
        results = await self.db.query().eq("job_id", job_id).search()
        return len(results) > 0

    # ─── Utility ────────────────────────────────────────────────

    async def clear_all(self) -> int:
        """
        Clear all jobs (useful for testing).

        Returns:
            Number of deleted jobs
        """
        jobs = await self.list_all()
        for job in jobs:
            await self.delete(job.job_id)
        return len(jobs)

    async def get_stats(self) -> dict:
        """
        Get job statistics.

        Returns:
            Dict with counts: total, active, failed, paused
        """
        total = await self.count_jobs()
        active = await self.count_active()
        failed = await self.count_failed()

        records = await self.db.query().eq("status", JobStatus.PAUSED.value).search()
        paused = len(records)

        return {
            "total": total,
            "active": active,
            "failed": failed,
            "paused": paused,
        }

    async def recovery_restore(self) -> List[JobData]:
        """
        Get jobs that need recovery (active or failed).

        Used during bot startup to restore previously scheduled jobs.

        Returns:
            List of active and failed jobs
        """
        active = await self.get_active()
        failed = await self.get_failed()
        return active + failed
