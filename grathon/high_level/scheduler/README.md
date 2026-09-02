# Grathon Scheduled Tasks

Background job scheduling for Grathon bots with pluggable storage backends.

## Features

- 🎯 **Cron-based scheduling** - `0 9 * * *` format
- ⏱️ **Interval-based scheduling** - Every N seconds/minutes/hours/days
- 💾 **Pluggable storage** - In-memory (default) or PicoDB (persistent)
- 🔄 **Job management** - Pause, resume, manual trigger, delete
- 📊 **Error tracking** - Auto-recorded failures with error count
- 🚀 **Zero dependencies** (by default, `croniter` only)
- 📈 **Extensible** - Easy to implement custom storage backends

## Quick Start

### In-Memory (Default - No Persistence)

```python
from grathon import GrathonBot
from grathon.high_level.scheduler import BotScheduler

bot = GrathonBot(api_id=..., api_hash=..., bot_token=...)
scheduler = BotScheduler(bot)  # Uses InMemoryJobTransfer

@scheduler.cron("0 9 * * *", name="Daily Reminder")
async def daily_reminder():
    await bot.api.send_message(chat_id=123, text="Good morning!")

@scheduler.interval(hours=1, name="Cleanup")
async def cleanup():
    await db.delete_expired()

await scheduler.start()
# ... bot runs ...
await scheduler.stop()
```

### With PicoDB (Persistent Storage)

```python
from picodb import AsyncPicodb
from grathon import GrathonBot
from grathon.high_level.scheduler import BotScheduler
from grathon.high_level.scheduler.picodb_transfer import PicoDBJobTransfer, JobRecord

# Create PicoDB database
db = AsyncPicodb(
    schema_cls=JobRecord,
    path="sqlite+aiosqlite:///bot_jobs.db",
    indexes=[
        {'fields': ['job_id'], 'unique': True},
        {'fields': ['status']},
    ]
)
await db.init_db()

# Create bot with persistent scheduler
bot = GrathonBot(...)
scheduler = BotScheduler(bot, transfer=PicoDBJobTransfer(db))

@scheduler.cron("0 9 * * *")
async def daily_task():
    pass

await scheduler.start()
# Jobs persist across restarts! ✨
```

## API Reference

### BotScheduler

#### Constructor

```python
BotScheduler(
    bot: GrathonBot,
    transfer: JobTransfer = None,      # Default: InMemoryJobTransfer
    tick_interval: float = 10.0,       # Check for jobs every 10 seconds
)
```

#### Decorators

```python
@scheduler.cron(expr, name=None, tz="UTC")
async def my_job():
    pass

@scheduler.interval(seconds=None, minutes=None, hours=None, days=None, name=None)
async def my_job():
    pass
```

#### Lifecycle

```python
await scheduler.start()      # Start background loop
await scheduler.stop()       # Stop gracefully
```

#### Management

```python
await scheduler.pause(job_id)          # Pause a job
await scheduler.resume(job_id)         # Resume a job
await scheduler.run_now(job_id)        # Trigger immediately
await scheduler.delete_job(job_id)     # Delete a job

jobs = await scheduler.list_jobs()     # Get all jobs
job = await scheduler.get_job(job_id)  # Get specific job
```

### JobTransfer

Abstract interface for custom storage backends.

```python
class JobTransfer(ABC):
    # CRUD
    async def save(job: JobData) -> str
    async def get(job_id: str) -> Optional[JobData]
    async def delete(job_id: str) -> bool
    async def list_all() -> List[JobData]
    async def update(job_id: str, **fields) -> bool

    # Status
    async def set_status(job_id: str, status: str) -> bool
    async def update_last_run(job_id: str, ran_at: datetime) -> bool
    async def update_next_run(job_id: str, next_run: datetime) -> bool
    async def mark_failed(job_id: str, error: str, increment_count: bool = True) -> bool

    # Queries
    async def get_active() -> List[JobData]
    async def get_failed() -> List[JobData]
    async def exists(job_id: str) -> bool
```

## Cron Format

`minute hour day-of-month month day-of-week`

Examples:
- `0 9 * * *` → 9:00 AM every day
- `*/5 * * * *` → Every 5 minutes
- `0 0 * * 0` → Midnight every Sunday
- `0 12 * * 1-5` → Noon every weekday
- `30 2 * * *` → 2:30 AM every day

## Job Status

- `active` - Will run on schedule
- `paused` - Won't run until resumed
- `failed` - Had errors, still runs
- `completed` - Finished (optional final state)

## Error Handling

Jobs that raise exceptions are marked as failed:

```python
# With error tracking:
@scheduler.interval(minutes=1)
async def may_fail():
    if error_condition:
        raise ValueError("Something went wrong")
    # On failure: job.error_count += 1, job.last_error set

# Manual recovery:
failed_jobs = await scheduler.transfer.get_failed()
for job in failed_jobs:
    await scheduler.resume(job.job_id)  # Reset to active
```

## Implementing Custom Storage

```python
from grathon.high_level.scheduler import JobTransfer

class MyCustomJobTransfer(JobTransfer):
    async def save(self, job):
        # Save to your backend
        pass
    
    # ... implement all abstract methods ...

# Use it:
scheduler = BotScheduler(bot, transfer=MyCustomJobTransfer())
```

## Architecture

```
BotScheduler
    ├─ @scheduler.cron() → register job
    ├─ @scheduler.interval() → register job
    ├─ await scheduler.start() → background loop
    │   └─ Check every tick_interval seconds
    │   └─ Run due jobs
    │   └─ Calculate next_run
    │   └─ Track errors
    └─ Transfer (abstract)
        ├─ InMemoryJobTransfer (default)
        ├─ PicoDBJobTransfer (persistent)
        └─ YourCustomTransfer (your DB)
```

## Performance Notes

- **InMemoryJobTransfer**: Instant, ~O(1) operations
- **PicoDBJobTransfer**: Very fast SQLite, ~O(log n) for indexed queries
- **Tick interval**: Default 10s. Lower = more responsive, higher = less CPU
- **Job execution**: Async, non-blocking

## Testing

```python
import asyncio
from grathon.high_level.scheduler import BotScheduler, InMemoryJobTransfer

async def test():
    # Create mock bot
    class MockBot:
        class API:
            async def send_message(self, **kwargs):
                pass
        api = API()

    bot = MockBot()
    scheduler = BotScheduler(bot)

    call_count = 0

    @scheduler.interval(seconds=1)
    async def test_job():
        nonlocal call_count
        call_count += 1

    await scheduler.start()
    await asyncio.sleep(3)
    await scheduler.stop()

    assert call_count >= 2, "Job should run at least twice"

asyncio.run(test())
```

## Files

- `job_data.py` - JobData dataclass and enums
- `job_transfer.py` - Abstract JobTransfer ABC
- `memory_transfer.py` - InMemoryJobTransfer (default)
- `picodb_transfer.py` - PicoDBJobTransfer (persistent)
- `scheduler.py` - BotScheduler main class

## Examples

See:
- `example_scheduler_plugin.py` - Basic usage
- `example_scheduler_with_picodb.py` - With persistence

## Dependencies

- **Required**: Python 3.10+
- **Optional**: `croniter` (for cron parsing)
- **Optional**: `picodb` (for persistent storage)

## License

Same as Grathon framework.
