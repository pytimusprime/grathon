# PicoDB — Coding Rules & Conventions

## Overview

These rules define how to write code that works correctly with PicoDB. Violating these rules will cause bugs, data corruption, or unexpected behavior.

---

## 1. Schema Definition Rules

### ALWAYS use dataclasses for schemas

```python
# ✅ CORRECT
@dataclass
class Movie:
    title: str
    year: int
    rating: float

# ❌ WRONG — don't use plain classes or namedtuples
class Movie:
    def __init__(self, title, year, rating):
        self.title = title
        self.year = year
        self.rating = rating
```

### ALWAYS include `record_id` as a field if you need to set it manually

```python
# ✅ CORRECT — record_id is auto-generated if not provided
@dataclass
class Movie:
    record_id: str = ""
    title: str
    year: int

# ❌ WRONG — record_id is auto-generated, don't try to set it manually in most cases
```

### NEVER use mutable default values in dataclass fields

```python
# ✅ CORRECT
@dataclass
class Movie:
    tags: list = field(default_factory=list)

# ❌ WRONG — mutable default shared across all instances
@dataclass
class Movie:
    tags: list = []
```

---

## 2. Database Initialization Rules

### ALWAYS call `init_db()` before any operations

```python
# ✅ CORRECT
db = AsyncPicodb(Movie, path="sqlite+aiosqlite:///movies.db")
await db.init_db()
await db.insert(movie)

# ❌ WRONG — operations will fail without init_db()
db = AsyncPicodb(Movie, path="sqlite+aiosqlite:///movies.db")
await db.insert(movie)
```

### ALWAYS call `close()` when done

```python
# ✅ CORRECT
await db.insert(movie)
await db.close()

# ❌ WRONG — resource leak
await db.insert(movie)
```

---

## 3. Insert Rules

### ALWAYS use `insert()` for single records and `insert_many()` for bulk

```python
# ✅ CORRECT — single insert
rid = await db.insert(movie)

# ✅ CORRECT — bulk insert
rids = await db.insert_many(movies, chunk_size=5000, atomic=True)

# ❌ WRONG — looping insert_many for single records
for movie in movies:
    await db.insert(movie)
```

### ALWAYS handle hash collisions gracefully

PicoDB retries on `IntegrityError` (hash collision) up to 3 times. If all retries fail, it raises `RuntimeError`.

---

## 4. Query Rules

### ALWAYS use the `Q` query builder for structured queries

```python
# ✅ CORRECT
results = await db.query().gte("rating", 8.0).order_by("-rating").search()

# ❌ WRONG — don't write raw SQLAlchemy queries unless necessary
stmt = select(MovieModel).where(MovieModel.rating >= 8.0)
```

### ALWAYS use `stream_all()` or `stream_all_batches()` for large result sets

```python
# ✅ CORRECT — memory-efficient for large datasets
async for movie in db.stream_all(order_by="title"):
    process(movie)

# ❌ WRONG — loads all records into memory
all_movies = await db.search()  # No limit, could be huge
```

### ALWAYS specify `limit` on search queries

```python
# ✅ CORRECT
results = await db.search(limit=100)

# ❌ WRONG — no limit, could return millions of records
results = await db.search()
```

---

## 5. FTS Rules

### ALWAYS specify `fts_fields` at construction time

```python
# ✅ CORRECT
db = AsyncPicodb(Movie, fts_fields=["title", "genre"])

# ❌ WRONG — FTS won't work without fts_fields
db = AsyncPicodb(Movie, enable_fts=True)
```

### ALWAYS use `use_fts=True` explicitly in search calls

```python
# ✅ CORRECT
results = await db.search(use_fts=True, fts_query="Sci-Fi")

# ❌ WRONG — FTS is not enabled by default in search()
results = await db.search(fts_query="Sci-Fi")
```

### NEVER mix FTS search with Q query builder conditions

FTS and `Q` queries are separate paths. Use one or the other:

```python
# ✅ CORRECT — FTS only
results = await db.search(use_fts=True, fts_query="Sci-Fi")

# ✅ CORRECT — Q builder only
results = await db.query().eq("genre", "Sci-Fi").search()

# ❌ WRONG — mixing both
results = await db.query().eq("genre", "Sci-Fi").search(use_fts=True, fts_query="Sci-Fi")
```

---

## 6. Cache Rules

### ALWAYS check key type before cache operations

All cache keys must be strings. PicoDB enforces this but defensive coding helps:

```python
# ✅ CORRECT
key = f"session:{user_id}"
await cache.set(key, data, ttl=3600)

# ❌ WRONG — non-string key
await cache.set(user_id, data)  # user_id is an int
```

### ALWAYS handle expired keys in read logic

```python
# ✅ CORRECT
data = await cache.get("my_key", default={})
if not data:
    data = await fetch_from_source()
    await cache.set("my_key", data, ttl=3600)

# ❌ WRONG — doesn't handle expired/missing keys
data = await cache.get("my_key")
if data is None:
    # This could also mean the key was never set, not just expired
    pass
```

### NEVER use cache for critical data that must survive process restarts

Cache is best-effort. For critical data, always use the main database operations.

---

## 7. Search Engine Rules

### ALWAYS rebuild the search index after bulk operations

```python
# ✅ CORRECT
await search_db.insert_many(movies)
await search_db.rebuild_search_index()

# ❌ WRONG — index may be stale after bulk insert
await search_db.insert_many(movies)
# No rebuild — index is inconsistent
```

### ALWAYS check `search_fields` are valid before creating `PicodoSearch`

```python
# ✅ CORRECT
search_db = PicodoSearch(Movie, search_fields=["title", "content"])

# ❌ WRONG — empty search_fields raises ValueError
search_db = PicodoSearch(Movie, search_fields=[])
```

### NEVER rely on search index for critical lookups

The inverted index is a performance optimization. Always have a fallback to direct database queries.

---

## 8. PostgreSQL-Specific Rules

### ALWAYS handle `fts_vector` column in batch converter

When reading records from PostgreSQL, the `fts_vector` column is excluded from the result automatically. Don't include it in your dataclass schema.

### NEVER create `fts_vector` column manually

The `AsyncPicodoPG` class creates it automatically during `init_db()`. Manual creation may conflict with the trigger.

### ALWAYS use `BigInteger` for `user_id` in PostgreSQL

PicoDB auto-maps `user_id` fields to `BigInteger`. Don't override this unless you have a specific reason.

---

## 9. Error Handling Rules

### ALWAYS wrap database operations in try/except

```python
# ✅ CORRECT
try:
    rid = await db.insert(movie)
except IntegrityError:
    logger.warning(f"Duplicate record for movie: {movie.title}")
except Exception as e:
    logger.error(f"Insert failed: {e}")
    raise
```

### ALWAYS handle `RuntimeError` from insert retries

```python
# ✅ CORRECT
try:
    rid = await db.insert(movie)
except RuntimeError as e:
    if "Insert failed after retries" in str(e):
        logger.error(f"Hash collision for movie: {movie.title}")
    raise
```

### NEVER ignore exceptions from `stream_all_batches`

```python
# ✅ CORRECT
try:
    async for batch in db.stream_all_batches(batch_size=100):
        process(batch)
except Exception as e:
    logger.error(f"Stream failed: {e}")
    raise
```

---

## 10. Type Handling Rules

### ALWAYS be defensive with JSONB fields

Database fields of type `list` or `dict` may be stored as JSON strings or already parsed as lists/dicts:

```python
# ✅ CORRECT — handle both cases
if isinstance(movie.tags, str):
    try:
        movie.tags = orjson.loads(movie.tags)
    except Exception:
        movie.tags = []
elif not isinstance(movie.tags, list):
    movie.tags = []
```

### ALWAYS convert dates/datetimes to ISO format before storage

The `data_formatter` utility handles this automatically, but be aware when constructing dataclass instances manually.

---

## 11. Concurrency Rules

### NEVER access `_write_lock` directly from outside the class

The write lock is internal to PicoDB. All write operations acquire it automatically.

### ALWAYS use `asyncio.Lock`-safe patterns

```python
# ✅ CORRECT — PicoDB handles locking internally
await db.insert(movie)
await db.update(rid, movie)
await db.delete(rid)

# ❌ WRONG — don't add your own locking on top of PicoDB's lock
async with my_external_lock:
    await db.insert(movie)
```

---

## 12. Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Dataclass names | `PascalCase` | `Movie`, `User`, `LogEntry` |
| Field names | `snake_case` | `title`, `year`, `rating` |
| Database variable names | `snake_case` | `db`, `cache_db`, `search_db` |
| Method calls | `snake_case` | `insert()`, `get()`, `search()` |
| Constants | `UPPER_SNAKE_CASE` | `DEFAULT_PATH`, `MAX_BATCH_SIZE` |
| Type variables | `SchemaT` | `AsyncPicodb[SchemaT]` |

---

## 13. Import Rules

### ALWAYS import from `picodb` top-level package

```python
# ✅ CORRECT
from picodb import AsyncPicodb, AsyncPicodoPG, PicodoCache, PicodoSearch, Q

# ❌ WRONG — don't import internal modules directly
from picodb.core import AsyncPicodb
from picodb.query import Q
```

### ALWAYS import `dataclass` from `dataclasses`

```python
# ✅ CORRECT
from dataclasses import dataclass

# ❌ WRONG
from dataclasses import dataclass as dc
```

---

## 14. Testing Rules

### ALWAYS test with both SQLite and PostgreSQL before deploying

PicoDB's behavior differs slightly between backends (FTS mechanism, type mapping, locking). Test both.

### ALWAYS test bulk operations with realistic data sizes

`insert_many` with `chunk_size=10000` behaves differently than with 10 records. Test at scale.

### ALWAYS test FTS and search index rebuilds

```python
# Test FTS rebuild
await db.rebuild_fts()
results = await db.search(use_fts=True, fts_query="test")
assert len(results) > 0

# Test search index rebuild
count = await search_db.rebuild_search_index()
assert count > 0
```