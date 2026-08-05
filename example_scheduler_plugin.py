"""
Example plugin demonstrating BotScheduler usage.

This plugin shows how to use the scheduled tasks system with both
cron-based and interval-based scheduling.

Usage:
    Copy to app/plugins/ and it will auto-load.

    Or run directly:
    python -m grathon.example_scheduler_plugin
"""

from grathon import GrathonBot
from grathon.high_level.scheduler import BotScheduler
from datetime import datetime
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example: Create bot with scheduler
async def main():
    # Mock bot (for standalone testing)
    class MockAPI:
        async def send_message(self, chat_id, **kwargs):
            logger.info(f"[Mock] Sending to {chat_id}: {kwargs}")

    class MockBot:
        def __init__(self):
            self.api = MockAPI()

    bot = MockBot()

    # Create scheduler
    scheduler = BotScheduler(bot)

    # ─── Cron-based jobs ───────────────────────────────────────

    @scheduler.cron("*/10 * * * *", name="Every 10 minutes")
    async def every_10_minutes():
        logger.info(f"⏰ Running: Every 10 minutes at {datetime.now()}")
        # await bot.api.send_message(chat_id=123, text="Tick!")

    @scheduler.cron("0 9 * * *", name="Daily at 9 AM")
    async def daily_reminder():
        logger.info(f"📅 Running: Daily reminder at {datetime.now()}")
        # await bot.api.send_message(chat_id=123, text="Good morning!")

    @scheduler.cron("0 12 * * 0", name="Sunday noon")
    async def weekly_check():
        logger.info(f"📊 Running: Weekly check at {datetime.now()}")

    # ─── Interval-based jobs ───────────────────────────────────

    @scheduler.interval(seconds=5, name="Every 5 seconds")
    async def every_5_seconds():
        logger.info(f"⚡ Running: Every 5 seconds at {datetime.now()}")

    @scheduler.interval(minutes=1, name="Every minute")
    async def every_minute():
        logger.info(f"🔄 Running: Every minute at {datetime.now()}")

    @scheduler.interval(hours=1, name="Every hour")
    async def every_hour():
        logger.info(f"📈 Running: Every hour at {datetime.now()}")

    # ─── Error handling ────────────────────────────────────────

    @scheduler.interval(seconds=15, name="May fail job")
    async def flaky_job():
        import random

        if random.random() < 0.3:
            raise RuntimeError("Random failure for demo")
        logger.info(f"✅ Running: Flaky job succeeded at {datetime.now()}")

    # ─── Start scheduler ───────────────────────────────────────

    await scheduler.start()

    # Give it time to run some jobs
    logger.info("Scheduler running for 30 seconds...")
    await asyncio.sleep(30)

    # List all jobs
    logger.info("\n─── All Jobs ───")
    jobs = await scheduler.list_jobs()
    for job in jobs:
        logger.info(f"  {job.name:20} | {job.job_id[:8]} | {job.status} | Next: {job.next_run}")

    # Manual trigger
    logger.info("\n─── Manual Trigger ───")
    if jobs:
        first_job = jobs[0]
        logger.info(f"Triggering '{first_job.name}' manually...")
        await scheduler.run_now(first_job.job_id)

    # Pause and resume
    logger.info("\n─── Pause/Resume ───")
    if jobs:
        second_job = jobs[1] if len(jobs) > 1 else jobs[0]
        logger.info(f"Pausing '{second_job.name}'...")
        await scheduler.pause(second_job.job_id)
        await asyncio.sleep(5)
        logger.info(f"Resuming '{second_job.name}'...")
        await scheduler.resume(second_job.job_id)

    # Stop
    logger.info("\n─── Stopping ───")
    await scheduler.stop()
    logger.info("Done!")


if __name__ == "__main__":
    asyncio.run(main())
