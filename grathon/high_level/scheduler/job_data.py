"""Job data structures for scheduled tasks."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum


class JobStatus(str, Enum):
    """Job execution status."""
    ACTIVE = "active"
    PAUSED = "paused"
    FAILED = "failed"
    COMPLETED = "completed"


class TriggerType(str, Enum):
    """Job trigger type."""
    CRON = "cron"
    INTERVAL = "interval"


@dataclass
class JobData:
    """
    Persistent job data structure.

    Attributes:
        job_id: Unique job identifier (auto-generated)
        name: Human-readable job name
        trigger: Job trigger type ("cron" or "interval")
        trigger_args: Trigger configuration
            - For cron: {"cron": "0 9 * * *"}
            - For interval: {"seconds": 3600} or {"minutes": 60, "hours": 1}
        status: Current job status (active, paused, failed, completed)
        created_at: Timestamp when job was created
        last_run: Timestamp of last execution (None if never ran)
        next_run: Calculated next run time
        error_count: Number of consecutive failures
        last_error: Last error message (if failed)
    """
    job_id: str
    name: str
    trigger: str                               # "cron" | "interval"
    trigger_args: Dict[str, Any]              # {"cron": "0 9 * * *"} | {"seconds": 3600}
    status: str                                # JobStatus enum value
    created_at: datetime
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    error_count: int = 0
    last_error: Optional[str] = None

    def __post_init__(self):
        """Validate trigger type."""
        if self.trigger not in (TriggerType.CRON.value, TriggerType.INTERVAL.value):
            raise ValueError(f"Invalid trigger type: {self.trigger}")
        if self.status not in (s.value for s in JobStatus):
            raise ValueError(f"Invalid status: {self.status}")

    def is_active(self) -> bool:
        """Check if job is active."""
        return self.status == JobStatus.ACTIVE.value

    def is_failed(self) -> bool:
        """Check if job has failed."""
        return self.status == JobStatus.FAILED.value

    def is_paused(self) -> bool:
        """Check if job is paused."""
        return self.status == JobStatus.PAUSED.value

    def should_run(self) -> bool:
        """Check if job should run now (not paused or failed, and next_run is past)."""
        if not self.is_active():
            return False
        if self.next_run is None:
            return True
        return self.next_run <= datetime.now()
