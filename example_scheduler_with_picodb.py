"""
Example: BotScheduler with PicoDB persistence.

This demonstrates how to use scheduled tasks with persistent storage.
Jobs survive bot restarts!

Setup:
    1. Install: pip install croniter
    2. Run: python3 example_scheduler_with_picodb.py
"""

import asyncio
import logging
from datetime import datetime
from dataclasses import dataclass

# Note: In a real Grathon bot, these imports would be:
# from grathon import GrathonBot
# from grathon.high_level.scheduler import BotScheduler
# from grathon.high_level.scheduler.picodb_transfer import PicoDBJobTransfer
# from picodb import AsyncPicodb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class JobRecord:
    """PicoDB dataclass for jobs."""
    job_id: str
    name: str
    trigger: str
    trigger_args: dict
    status: str
    created_at: str
    last_run: str | None = None
    next_run: str | None = None
    error_count: int = 0
    last_error: str | None = None


async def main():
    """Demo: Persistent scheduled tasks with PicoDB."""

    logger.info("\n" + "="*60)
    logger.info("Grathon Scheduled Tasks + PicoDB Demo")
    logger.info("="*60 + "\n")

    # ─── Setup PicoDB ───────────────────────────────────────

    # In real code:
    # from picodb import AsyncPicodb
    # db = AsyncPicodb(
    #     schema_cls=JobRecord,
    #     path="sqlite+aiosqlite:///bot_jobs.db",
    #     indexes=[
    #         {'fields': ['job_id'], 'unique': True},
    #         {'fields': ['status']},
    #     ]
    # )
    # await db.init_db()

    logger.info("✅ PicoDB initialized")

    # ─── Setup Scheduler ────────────────────────────────────

    # In real code:
    # from grathon import GrathonBot
    # from grathon.high_level.scheduler import BotScheduler
    # from grathon.high_level.scheduler.picodb_transfer import PicoDBJobTransfer
    #
    # bot = GrathonBot(api_id=..., api_hash=..., bot_token=...)
    # scheduler = BotScheduler(bot, transfer=PicoDBJobTransfer(db))

    logger.info("✅ BotScheduler initialized with PicoDB backend\n")

    # ─── Example Usage ──────────────────────────────────────

    logger.info("Example Scheduler Setup:")
    logger.info("-" * 60)

    setup_code = '''
@scheduler.cron("0 9 * * *", name="Daily Reminder")
async def daily_reminder():
    """Runs at 9 AM every day - persists across restarts!"""
    await bot.api.send_message(chat_id=123, text="Good morning!")

@scheduler.cron("0 12 * * 0", name="Weekly Check")
async def weekly_check():
    """Runs at noon every Sunday"""
    await run_weekly_health_check()

@scheduler.interval(hours=1, name="Hourly Cleanup")
async def cleanup_old_data():
    """Runs every hour"""
    await db.delete_expired()
    await db.cleanup()

@scheduler.interval(minutes=5, name="Status Check")
async def status_check():
    """Runs every 5 minutes"""
    await monitor_active_users()

# Startup:
await scheduler.start()

# Management:
jobs = await scheduler.list_jobs()                    # Get all jobs
await scheduler.pause(job_id)                         # Pause job
await scheduler.resume(job_id)                        # Resume job
await scheduler.run_now(job_id)                       # Manual trigger
stats = await scheduler.transfer.get_stats()          # Get stats

# Recovery on restart:
# PicoDB automatically loads all previously saved jobs!
    '''

    logger.info(setup_code)

    # ─── Key Features ───────────────────────────────────────

    logger.info("\n" + "="*60)
    logger.info("Key Features")
    logger.info("="*60)

    features = [
        ("✅ Persistence", "Jobs saved to database"),
        ("✅ Restart Recovery", "Jobs resume after bot restart"),
        ("✅ Cron Support", "0 9 * * * (9 AM daily)"),
        ("✅ Intervals", "Every N seconds/minutes/hours/days"),
        ("✅ Management", "Pause, resume, manual trigger, delete"),
        ("✅ Error Tracking", "Auto-recorded failures + error count"),
        ("✅ Extensible", "Easy to add custom JobTransfer backends"),
        ("✅ Decoupled", "Scheduler ≠ Database"),
    ]

    for feature, desc in features:
        logger.info(f"  {feature:25} {desc}")

    # ─── PicoDB Benefits ────────────────────────────────────

    logger.info("\n" + "="*60)
    logger.info("Why PicoDB for Job Storage?")
    logger.info("="*60)

    benefits = [
        ("Async-first", "All operations are async/await"),
        ("SQLite native", "No extra server, just a file"),
        ("FTS support", "Full-text search on job names/errors"),
        ("Query builder", "Chainable .eq().gt().between() etc"),
        ("Lightweight", "~2800 lines, minimal dependencies"),
        ("Dataclass-based", "Type-safe schemas"),
    ]

    for benefit, detail in benefits:
        logger.info(f"  • {benefit:20} → {detail}")

    # ─── Implementation Notes ───────────────────────────────

    logger.info("\n" + "="*60)
    logger.info("Implementation Notes")
    logger.info("="*60)

    notes = [
        "PicoDBJobTransfer converts between JobData ↔ JobRecord",
        "Datetime fields stored as ISO format strings in DB",
        "Job IDs are UUIDs (unique across restarts)",
        "next_run calculated automatically after each run",
        "error_count incremented on failure, reset on success",
        "Status can be: active, paused, failed, completed",
    ]

    for note in notes:
        logger.info(f"  • {note}")

    # ─── Comparison ─────────────────────────────────────────

    logger.info("\n" + "="*60)
    logger.info("Storage Backend Comparison")
    logger.info("="*60)

    comparison = """
┌─────────────────┬──────────────┬─────────────────┐
│ Feature         │ InMemory     │ PicoDB          │
├─────────────────┼──────────────┼─────────────────┤
│ Persistence     │ ❌ No        │ ✅ Yes          │
│ Restart recovery│ ❌ No        │ ✅ Yes          │
│ Dependencies    │ ✅ None      │ ⚠️ PicoDB       │
│ Database file   │ N/A          │ ✅ SQLite       │
│ Performance     │ ✅ Instant   │ ✅ Very fast    │
│ Suitable for    │ Dev/testing  │ Production      │
└─────────────────┴──────────────┴─────────────────┘
    """

    logger.info(comparison)

    # ─── Next Steps ─────────────────────────────────────────

    logger.info("="*60)
    logger.info("Next Steps")
    logger.info("="*60)

    steps = [
        "1. In your bot, import: from grathon.high_level.scheduler import ...",
        "2. Create scheduler: scheduler = BotScheduler(bot, transfer=PicoDBJobTransfer(db))",
        "3. Define jobs with @scheduler.cron() or @scheduler.interval()",
        "4. Start: await scheduler.start()",
        "5. Jobs will now persist and survive restarts! 🚀",
    ]

    for step in steps:
        logger.info(f"  {step}")

    logger.info("\n" + "="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
