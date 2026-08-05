"""BotScheduler - background job scheduling for Grathon bots."""

import asyncio
import logging
import uuid
from datetime import datetime, timedelta
from typing import Callable, Optional, List, Any, TYPE_CHECKING

from .job_transfer import JobTransfer
from .memory_transfer import InMemoryJobTransfer
from .job_data import JobData, JobStatus, TriggerType

if TYPE_CHECKING:
    from grathon.grathon_bot import GrathonBot

try:
    from croniter import croniter
except ImportError:
    raise ImportError(
        "BotScheduler requires 'croniter' for cron support.\n"
        "Install it with: pip install croniter"
    )

logger = logging.getLogger(__name__)


class BotScheduler:
    """
    Background job scheduler for Grathon bots.

    Features:
    - Cron-based scheduling (0 9 * * *)
    - Interval-based scheduling (every hour, every 5 minutes, etc)
    - Pluggable storage backend (in-memory, PicoDB, etc)
    - Pause/resume/manual trigger jobs
    - Error tracking and retry logic

    Usage:
        scheduler = BotScheduler(bot)
        # or with PicoDB:
        # scheduler = BotScheduler(bot, transfer=PicoDBJobTransfer(db))

        @scheduler.cron("0 9 * * *")  # Daily at 9 AM
        async def daily_reminder():
            await bot.api.send_message(...)

        @scheduler.interval(hours=1)  # Every hour
        async def cleanup_task():
            await do_cleanup()

        # Start background processing
        await scheduler.start()
        # ... bot runs ...
        await scheduler.stop()
    """

    def __init__(
        self,
        bot: "GrathonBot",
        transfer: Optional[JobTransfer] = None,
        tick_interval: float = 10.0,
    ):
        """
        Initialize scheduler.

        Args:
            bot: GrathonBot instance
            transfer: JobTransfer backend (default: InMemoryJobTransfer)
            tick_interval: How often to check for jobs (seconds)
        """
        self.bot = bot
        self.transfer = transfer or InMemoryJobTransfer()
        self.tick_interval = max(1.0, float(tick_interval))

        self._running = False
        self._tasks: List[asyncio.Task[Any]] = []
        self._registered_jobs: dict[str, Callable] = {}  # job_id -> async function

    # ─── Decorators ────────────────────────────────────────────

    def cron(self, expr: str, *, name: Optional[str] = None, tz: str = "UTC"):
        """
        Schedule a job using cron expression.

        Args:
            expr: Cron expression (e.g., "0 9 * * *" for 9 AM daily)
            name: Optional human-readable job name
            tz: Timezone (default: UTC)

        Usage:
            @scheduler.cron("0 9 * * *")
            async def daily_task():
                print("Running at 9 AM")

        Cron format: minute hour day-of-month month day-of-week
            Examples:
            - "0 9 * * *" → 9:00 AM every day
            - "*/5 * * * *" → Every 5 minutes
            - "0 0 * * 0" → Midnight every Sunday
        """

        def decorator(func: Callable) -> Callable:
            # Validate cron expression
            try:
                croniter(expr)
            except Exception as e:
                raise ValueError(f"Invalid cron expression '{expr}': {e}")

            job_id = str(uuid.uuid4())
            job_name = name or f"{func.__name__}_{job_id[:8]}"

            async def wrapper():
                try:
                    # Calculate next run
                    now = datetime.now()
                    cron = croniter(expr, now)
                    next_run = datetime.fromtimestamp(cron.get_next(float))

                    # Create job data
                    job = JobData(
                        job_id=job_id,
                        name=job_name,
                        trigger=TriggerType.CRON.value,
                        trigger_args={"cron": expr, "tz": tz},
                        status=JobStatus.ACTIVE.value,
                        created_at=now,
                        next_run=next_run,
                    )

                    # Save to storage
                    await self.transfer.save(job)

                    # Register function
                    self._registered_jobs[job_id] = func

                    logger.info(
                        f"✅ Scheduled cron job '{job_name}' (ID: {job_id[:8]}): {expr}"
                    )

                except Exception as e:
                    logger.error(f"Error registering cron job '{job_name}': {e}")
                    raise

            # Run wrapper immediately to register
            asyncio.create_task(wrapper())

            return func

        return decorator

    def interval(
        self,
        *,
        seconds: Optional[int] = None,
        minutes: Optional[int] = None,
        hours: Optional[int] = None,
        days: Optional[int] = None,
        name: Optional[str] = None,
    ):
        """
        Schedule a job at regular intervals.

        Args:
            seconds: Interval in seconds
            minutes: Interval in minutes
            hours: Interval in hours
            days: Interval in days
            name: Optional human-readable job name

        Usage:
            @scheduler.interval(hours=1)
            async def every_hour():
                print("Running every hour")

            @scheduler.interval(minutes=5)
            async def every_five_minutes():
                print("Running every 5 minutes")
        """

        def decorator(func: Callable) -> Callable:
            # Calculate total seconds
            total_seconds = 0
            if seconds:
                total_seconds += seconds
            if minutes:
                total_seconds += minutes * 60
            if hours:
                total_seconds += hours * 3600
            if days:
                total_seconds += days * 86400

            if total_seconds <= 0:
                raise ValueError("Interval must be > 0")

            job_id = str(uuid.uuid4())
            job_name = name or f"{func.__name__}_{job_id[:8]}"

            async def wrapper():
                try:
                    now = datetime.now()
                    next_run = now + timedelta(seconds=total_seconds)

                    # Create job data
                    job = JobData(
                        job_id=job_id,
                        name=job_name,
                        trigger=TriggerType.INTERVAL.value,
                        trigger_args={
                            "seconds": seconds,
                            "minutes": minutes,
                            "hours": hours,
                            "days": days,
                        },
                        status=JobStatus.ACTIVE.value,
                        created_at=now,
                        next_run=next_run,
                    )

                    # Save to storage
                    await self.transfer.save(job)

                    # Register function
                    self._registered_jobs[job_id] = func

                    interval_str = (
                        f"{seconds}s"
                        if seconds
                        else f"{minutes}m"
                        if minutes
                        else f"{hours}h"
                        if hours
                        else f"{days}d"
                    )
                    logger.info(
                        f"✅ Scheduled interval job '{job_name}' (ID: {job_id[:8]}): every {interval_str}"
                    )

                except Exception as e:
                    logger.error(f"Error registering interval job '{job_name}': {e}")
                    raise

            # Run wrapper immediately to register
            asyncio.create_task(wrapper())

            return func

        return decorator

    # ─── Lifecycle ─────────────────────────────────────────────

    async def start(self) -> None:
        """
        Start the scheduler background loop.

        This spawns a background task that checks for jobs to run.
        Must be awaited:
            await scheduler.start()

        The scheduler runs until stop() is called.
        """
        if self._running:
            logger.warning("Scheduler already running")
            return

        self._running = True
        logger.info("🚀 Scheduler started")

        # Create background task
        task = asyncio.create_task(self._run_loop())
        self._tasks.append(task)

    async def stop(self) -> None:
        """
        Stop the scheduler gracefully.

        Cancels all background tasks and awaits cleanup.
        """
        if not self._running:
            logger.warning("Scheduler not running")
            return

        self._running = False
        logger.info("🛑 Scheduler stopping...")

        # Cancel all tasks
        for task in self._tasks:
            if not task.done():
                task.cancel()

        # Wait for cancellation
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)

        self._tasks.clear()
        logger.info("✅ Scheduler stopped")

    # ─── Management ────────────────────────────────────────────

    async def pause(self, job_id: str) -> bool:
        """
        Pause a job (won't run until resumed).

        Args:
            job_id: Job identifier

        Returns:
            True if paused, False if not found
        """
        if await self.transfer.set_status(job_id, JobStatus.PAUSED.value):
            logger.info(f"⏸️ Job {job_id[:8]} paused")
            return True
        return False

    async def resume(self, job_id: str) -> bool:
        """
        Resume a paused job.

        Args:
            job_id: Job identifier

        Returns:
            True if resumed, False if not found
        """
        if await self.transfer.set_status(job_id, JobStatus.ACTIVE.value):
            logger.info(f"▶️ Job {job_id[:8]} resumed")
            return True
        return False

    async def run_now(self, job_id: str) -> bool:
        """
        Manually trigger a job immediately.

        Args:
            job_id: Job identifier

        Returns:
            True if triggered, False if not found or no function registered
        """
        job = await self.transfer.get(job_id)
        if not job:
            logger.warning(f"Job {job_id[:8]} not found")
            return False

        if job_id not in self._registered_jobs:
            logger.warning(f"Job {job_id[:8]} has no registered function")
            return False

        logger.info(f"⚡ Running job {job_id[:8]} manually")

        # Run immediately
        try:
            func = self._registered_jobs[job_id]
            await func()
            await self.transfer.update_last_run(job_id, datetime.now())
            logger.info(f"✅ Job {job_id[:8]} completed successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Job {job_id[:8]} failed: {e}")
            await self.transfer.mark_failed(job_id, str(e))
            return False

    async def list_jobs(self) -> List[JobData]:
        """
        Get all scheduled jobs.

        Returns:
            List of JobData objects
        """
        return await self.transfer.list_all()

    async def get_job(self, job_id: str) -> Optional[JobData]:
        """
        Get a specific job.

        Args:
            job_id: Job identifier

        Returns:
            JobData if found, None otherwise
        """
        return await self.transfer.get(job_id)

    async def delete_job(self, job_id: str) -> bool:
        """
        Delete a job.

        Args:
            job_id: Job identifier

        Returns:
            True if deleted, False if not found
        """
        if await self.transfer.delete(job_id):
            if job_id in self._registered_jobs:
                del self._registered_jobs[job_id]
            logger.info(f"🗑️ Job {job_id[:8]} deleted")
            return True
        return False

    # ─── Internal ──────────────────────────────────────────────

    async def _run_loop(self) -> None:
        """Main background loop that runs jobs."""
        while self._running:
            try:
                # Get all jobs
                jobs = await self.transfer.get_active()

                now = datetime.now()

                # Check each job
                for job in jobs:
                    # Skip if no next_run calculated
                    if job.next_run is None:
                        continue

                    # Skip if not time yet
                    if now < job.next_run:
                        continue

                    # Skip if no registered function
                    if job.job_id not in self._registered_jobs:
                        logger.warning(f"Job {job.job_id[:8]} has no function registered")
                        continue

                    # Run the job
                    await self._execute_job(job)

                # Sleep before next tick
                await asyncio.sleep(self.tick_interval)

            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(self.tick_interval)

    async def _execute_job(self, job: JobData) -> None:
        """Execute a single job."""
        logger.info(f"▶️ Executing job '{job.name}' ({job.job_id[:8]})")

        try:
            # Get registered function
            func = self._registered_jobs[job.job_id]

            # Run it
            await func()

            # Update tracking
            await self.transfer.update_last_run(job.job_id, datetime.now())

            # Calculate next run
            next_run = self._calculate_next_run(job)
            await self.transfer.update_next_run(job.job_id, next_run)

            # Reset error count on success
            await self.transfer.update(job.job_id, error_count=0, last_error=None)

            logger.info(f"✅ Job '{job.name}' completed successfully")

        except Exception as e:
            logger.error(f"❌ Job '{job.name}' failed: {e}")
            await self.transfer.mark_failed(job.job_id, str(e), increment_count=True)

    def _calculate_next_run(self, job: JobData) -> datetime:
        """Calculate next run time for a job."""
        now = datetime.now()

        if job.trigger == TriggerType.CRON.value:
            cron_expr = job.trigger_args.get("cron")
            if cron_expr:
                cron = croniter(cron_expr, now)
                return datetime.fromtimestamp(cron.get_next(float))
            return now + timedelta(hours=1)  # fallback

        elif job.trigger == TriggerType.INTERVAL.value:
            seconds = (
                (job.trigger_args.get("days") or 0) * 86400
                + (job.trigger_args.get("hours") or 0) * 3600
                + (job.trigger_args.get("minutes") or 0) * 60
                + (job.trigger_args.get("seconds") or 0)
            )
            if seconds > 0:
                return now + timedelta(seconds=seconds)
            return now + timedelta(hours=1)  # fallback

        return now + timedelta(hours=1)  # default fallback
