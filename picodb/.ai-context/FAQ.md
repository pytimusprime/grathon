# PicoDB FAQ

## General

### What is PicoDB?
PicoDB is an async Python ORM wrapper around SQLite (via SQLAlchemy + aiosqlite) and PostgreSQL (via asyncpg). It provides dataclass-based schemas, automatic table generation, full-text search, a chainable query builder, a Redis-like cache layer, and an inverted-index search engine with BM25 ranking.

### Why PicoDB instead of SQLAlchemy directly?
PicoDB simplifies common patterns:
- **Dataclass schemas** — no need to define SQLAlchemy model classes manually
- **Auto table generation** — tables are created from dataclass field types
- **Built-in FTS** — full-text search is a first-class feature, not an afterthought
- **Redis-like cache** — key-value and set operations on the same database
- **BM25 search** — inverted index with relevance scoring out of the box
- **Record ID generation** — deterministic MD5 hashes for idempotent operations

### Which database should I use?
- **SQLite** — for development, testing, embedded use, and small-to-medium datasets
- **PostgreSQL** — for production workloads, concurrent access, and large datasets

### What Python versions are supported?
Python >= 3.13 is required.

## Installation & Setup

### How do I install PicoDB?
```bash
pip install picodb
```

Or reference it locally:
```toml
dependencies = [
    "picodb @ file:///path/to/libs/picodb",
]
```

### I get `ModuleNotFoundError: No module named 'sqlalchemy'`
PicoDB depends on SQLAlchemy. Install it:
```bash
pip install sqlalchemy aiosqlite asyncpg orjson
```

### How do I connect to PostgreSQL?
```python
db = AsyncPicodoPG(
    MySchema,
    path="postgresql+asyncpg://user:password@localhost/dbname",
)
```

Make sure `asyncpg` is installed and the PostgreSQL server is running.

## Dataclass Schemas

### What types are supported in dataclass fields?
| Python Type | SQLAlchemy Column |
|---|---|
| `str` | `String` |
| `int` | `Integer` (or `BigInteger` for `user_id` in PG) |
| `float` | `Float` |
| `bool` | `Boolean` |
| `list` / `dict` | `JSONB` |
| `Optional[T]` | Nullable `T` |

### What happens if I use a type not in the table?
Unknown types default to `String`.

### Can I use nested dataclasses?
Yes. Nested dataclasses are stored as JSONB. When reading back, they are deserialized automatically.

### How is `record_id` generated?
The `record_id` is an MD5 hash of the serialized record data (using `orjson` with sorted keys). This makes it deterministic — the same data always produces the same ID.

### What happens on hash collision?
If two different records produce the same MD5 hash (extremely rare), PicoDB appends a UUID fragment and retries up to 3 times.

## Full-Text Search

### How do I enable FTS?
Pass `fts_fields` to the constructor:
```python
db = AsyncPicodb(Movie, fts_fields=["title", "genre"])
```

### Can I disable FTS?
Yes:
```python
db = AsyncPicodb(Movie, enable_fts=False)
```

### How do I search with FTS?
```python
results = await db.search(use_fts=True, fts_query="Sci-Fi", limit=10)
```

### Can I use FTS with the query builder?
FTS and `Q` queries are separate. Use `search(use_fts=True, fts_query=...)` for FTS, or `query().eq(...).search()` for structured queries.

### How do I rebuild the FTS index?
```python
await db.rebuild_fts()
```

This is useful after bulk inserts or if the FTS index becomes corrupted.

### What is the difference between SQLite FTS and PostgreSQL FTS?
| Feature | SQLite (FTS5) | PostgreSQL (tsvector) |
|---|---|---|
| Index type | Virtual table | GIN index on tsvector column |
| Tokenizer | unicode61 | Built-in (simple, english, etc.) |
| Auto-population | Inline on insert/update | Trigger-based |
| Ranking | Built-in FTS ranking | ts_rank() |
| Boolean operators | FTS5 syntax | to_tsquery() syntax |

## Query Builder

### How do I do a case-insensitive search?
```python
results = await db.query().ilike("title", "%inception%").search()
```

### How do I use OR conditions?
```python
results = await db.query().or_(
    db.query().model.title == "Inception",
    db.query().model.genre == "Action",
).search()
```

### How do I order by multiple fields?
```python
results = await db.query().order_by("-rating", "title").search()
```

### Can I use raw SQLAlchemy conditions?
Yes:
```python
from sqlalchemy import func
results = await db.query().where(func.length(db.query().model.title) > 10).search()
```

## Cache

### How does TTL work?
When you set a key with `ttl`, the expiry time is stored as a Unix timestamp. On read operations (`get`, `keys`, `exists_key`), expired keys are detected and treated as missing. There is no background cleanup thread.

### Can I manually clean up expired keys?
Yes:
```python
evicted = await cache.evict_expired()
```

### What happens if I set a key that already exists?
It is overwritten (UPSERT behavior). The TTL is also updated.

### Are cache operations atomic?
Cache operations share the parent database's write lock, so they are consistent with the main data.

## Search Engine (BM25)

### How is BM25 different from FTS?
FTS (FTS5/tsvector) returns matching records but doesn't provide fine-grained relevance scoring. BM25 uses an inverted index with term frequency, document frequency, and field length normalization to produce a numeric relevance score for each record.

### Is the search index updated automatically?
Yes. On `insert` and `delete`, the search index is updated in the same transaction (SQLite) or a separate transaction (PostgreSQL).

### Can I use both FTS and BM25 search?
Yes. FTS is built into `AsyncPicodb`/`AsyncPicodoPG`. BM25 requires `PicodoSearch`. They serve different purposes and can be used independently.

### How do I rebuild the search index?
```python
count = await search_db.rebuild_search_index()
```

## Performance

### How do I optimize bulk inserts?
Use `insert_many` with `chunk_size` and `atomic=True`:
```python
rids = await db.insert_many(movies, chunk_size=5000, atomic=True)
```

### How do I stream large result sets without loading everything into memory?
Use `stream_all` or `stream_all_batches`:
```python
async for movie in db.stream_all(order_by="title"):
    process(movie)
```

### What PRAGMAs are set by default (SQLite)?
| PRAGMA | Value | Purpose |
|---|---|---|
| `journal_mode` | `WAL` | Write-Ahead Logging for better concurrency |
| `synchronous` | `NORMAL` | Balance between safety and speed |
| `temp_store` | `MEMORY` | Temp tables in RAM |
| `mmap_size` | 256MB | Memory-mapped I/O for faster reads |
| `cache_size` | -128MB | 128MB page cache |
| `read_uncommitted` | `True` | Allow dirty reads for better concurrency |

### How can I change the page size for streaming?
```python
db = AsyncPicodb(Movie, page_size=5000)
```

## Troubleshooting

### `IntegrityError` on insert
This usually means a unique constraint violation (e.g., duplicate email). If using `record_id`, it means two different records produced the same MD5 hash (extremely rare). PicoDB retries with a UUID suffix automatically.

### FTS search returns no results
- Check that `fts_fields` was set when creating the database
- Check that `fts_populate=True` (default)
- Try `await db.rebuild_fts()` to rebuild the index
- Verify the FTS virtual table exists: `SELECT name FROM sqlite_master WHERE type='virtual'`

### `Field 'X' not found in schema`
You referenced a field name in `distinct_values`, `value_counts`, or `exists_many` that doesn't exist in your dataclass. Double-check the field name.

### Slow queries on large tables
- Add indexes via the `indexes` parameter
- Use `stream_all_batches` instead of `search()` for large result sets
- Use `pre_filter` with `Q` objects for server-side filtering
- For PostgreSQL, ensure `work_mem` is adequately sized

### `AsyncPicodoPG` connection errors
- Verify the PostgreSQL server is running
- Check the connection string format: `postgresql+asyncpg://user:password@host:port/dbname`
- Ensure `asyncpg` is installed
- Check firewall/network access to the PostgreSQL host