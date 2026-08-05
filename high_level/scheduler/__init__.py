"""
Grathon Scheduled Tasks - Background job scheduling with pluggable storage.

JobTransfer is an abstract interface that allows custom storage backends.

Usage:
    # In-memory (default, no persistence):
    scheduler = BotScheduler(bot)

    # With PicoDB (persistent across restarts):
    from grathon.high_level.scheduler.picodb_transfer import PicoDBJobTransfer
    scheduler = BotScheduler(bot, transfer=PicoDBJobTransfer(db))
"""

from .scheduler import BotScheduler
from .job_transfer import JobTransfer
from .job_data import JobData, JobStatus, TriggerType
from .memory_transfer import InMemoryJobTransfer

__all__ = [
    "BotScheduler",
    "JobTransfer",
    "JobData",
    "JobStatus",
    "TriggerType",
    "InMemoryJobTransfer",
]
