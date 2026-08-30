# PicoDB Architecture

## Overview

PicoDB is a layered async ORM that wraps SQLAlchemy's async engine with a dataclass-first API. The design follows a **composition over inheritance** pattern: core CRUD functionality lives in `AsyncPicodb`, optional features are mixed in via `FtsMixin`, `SearchIndexMixin`, and `PicodoCache`.

```
┌─────────────────────────────────────────────────────────┐
│                    User Code                             │
│  db.insert(obj)  ·  db.query().eq().search()           │
│  db.search(use_fts=True, fts_query="...")              │
│  cache.set(key, value, ttl=3600)                       │
│  search_engine.search_index("query")                   │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│               AsyncPicodb / AsyncPicodoPG                │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  SQLAlchemy Async Engine + Session Factory         │ │
│  │  (sqlite+aiosqlite or postgresql+asyncpg)         │ │
│  └─────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Dataclass → SQLAlchemy Model Mapping              │ │
│  │  (field type → column type auto-resolution)       │ │
│  └─────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Write Lock (asyncio.Lock)                         │ │
│  │  Ensures atomic writes across all operations      │ │
│  └─────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  FTS Mixin (FtsMixin / FtsMixinPG)                │ │
│  │  SQLite: FTS5 virtual table                        │ │
│  │  PostgreSQL: tsvector column + GIN index + trigger│ │
│  └─────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Record ID Generation (MD5 hash)                   │ │
│  │  Deterministic ID from serialized data            │ │
│  └─────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  PRAGMA Configuration (SQLite only)               │ │
│  │  WAL, NORMAL sync, MEMORY temp, 256MB mmap,      │ │
│  │  128MB cache, read_uncommitted                    │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              PicodoCache (Optional)                      │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  _kv_store table (key, value, expires_at)         │ │
│  │  _set_store table (key, member)                    │ │
│  │  TTL-based expiry with lazy cleanup                │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              PicodoSearch (Optional)                     │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  _search_index table (term, record_id, field,     │ │
│  │                     frequency)                      │ │
│  │  _search_stats table (term, doc_count)             │ │
│  │  BM25 ranking with field boosts                    │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Layer 1: Data Model

### Dataclass Schema

The user defines a Python dataclass. PicoDB inspects its fields and maps them to SQLAlchemy column types automatically:

| Python Type | SQLAlchemy Column |
|---|---|
| `str` | `String` |
| `int` | `Integer` (or `BigInteger` for `user_id` in PostgreSQL) |
| `float` | `Float` |
| `bool` | `Boolean` |
| `list` / `dict` / dataclass | `JSONB` (SQLite: `JSONB` via SQLAlchemy) |
| `Optional[T]` | Unwrapped to `T`, column is nullable |

The `record_id` field is always a `String` primary key, auto-generated as an MD5 hash of the serialized record data.

### Type Resolution

```python
def _resolve_type(t: Any) -> tuple:
    """Unwrap Optional/Union types. Returns (base_type, is_optional)."""
    origin = get_origin(t)
    if origin is Union:
        args = [a for a in get_args(t) if a is not type(None)]
        return (args[0] if args else str), True
    return t, False
```

## Layer 2: Engine & Session

### SQLite Engine

```python
create_async_engine(
    "sqlite+aiosqlite:///path.db",
    echo=False,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)
```

- `check_same_thread=False` — Required for aiosqlite (SQLite allows multi-thread access)
- `AUTOCOMMIT` — Each statement is its own transaction unless explicitly wrapped
- `pool_pre_ping=True` — Validates connections before use

### PostgreSQL Engine

```python
create_async_engine(
    "postgresql+asyncpg://user:pass@host/db",
    echo=False,
    pool_size=20,
    max_overflow=20,
    pool_pre_ping=True,
    connect_args={"timeout": 10},
)
```

- Connection pooling with configurable `pool_size` and `max_overflow`
- Uses `asyncpg` driver for high performance

## Layer 3: Write Lock

All write operations (`insert`, `update`, `delete`, `delete_many`) acquire an `asyncio.Lock` to ensure atomicity. Read operations (`get`, `search`, `stream_all`) do not acquire the lock, allowing concurrent reads during writes.

## Layer 4: Record ID Generation

```python
def _compute_record_id(self, data_dict: Dict[str, Any]) -> str:
    safe_dict = {k: data_formatter(v) for k, v in data_dict.items()}
    return hashlib.md5(
        orjson.dumps(safe_dict, option=orjson.OPT_SORT_KEYS)
    ).hexdigest()
```

- Deterministic: same data always produces the same `record_id`
- Collision handling: on `IntegrityError`, appends a UUID fragment and retries (up to 3 times)

## Layer 5: Full-Text Search

### SQLite (FTS5)

- Virtual table: `CREATE VIRTUAL TABLE {table}_fts USING fts5(record_id, field1, field2, ...)`
- Tokenizer: `unicode61` (supports Unicode text)
- Auto-population: on every `insert`/`update`, the FTS table is updated in the same transaction
- Rebuild: `rebuild_fts()` drops and recreates the FTS table, then re-indexes all records

### PostgreSQL (tsvector)

- Column: `fts_vector TSVECTOR` with a GIN index
- Trigger: `BEFORE INSERT OR UPDATE` trigger auto-populates `fts_vector` using `to_tsvector('simple', ...)`
- Extension: `pg_trgm` is attempted (for trigram similarity, optional)
- Search: `fts_vector @@ plainto_tsquery('simple', :q)` with optional `ts_rank` for relevance

## Layer 6: Query Builder (`Q`)

The `Q` class provides a chainable API for building SQLAlchemy `select` statements:

```
Q(model, db)
  .eq("field", value)        → WHERE field = value
  .gte("field", 5)           → WHERE field >= 5
  .like("field", "%term%")   → WHERE field LIKE '%term%'
  .order_by("-field")        → ORDER BY field DESC
  .limit(10)                 → LIMIT 10
  .offset(20)                → OFFSET 20
  .search()                  → execute and return list
  .stream()                  → execute and async iterate
  .count()                   → execute COUNT query
  .delete()                  → execute DELETE
  .update(**values)          → execute UPDATE
```

Conditions are accumulated and combined with `AND`. The `or_()` method adds `OR` conditions.

## Layer 7: Cache (`PicodoCache`)

Sidecar tables `_kv_store` and `_set_store` provide Redis-like semantics:

- **KV Store**: key-value with optional TTL (Unix timestamp). Expired keys are detected lazily on `get`/`keys`/`exists_key`.
- **Set Store**: key-member pairs with unique constraint. Supports `sadd`, `srem`, `smembers`, `sismember`, `scard`.
- All operations share the parent's `_write_lock` for consistency.

## Layer 8: Search Engine (`PicodoSearch`)

Inverted index with BM25 ranking:

- **Index tables**: `_search_index` (term, record_id, field_name, frequency) and `_search_stats` (term, doc_count)
- **Tokenization**: lowercase, split on word boundaries, remove stopwords and short tokens (< 2 chars), count frequency
- **Indexing**: on insert, tokens are written to `_search_index` and stats updated in `_search_stats`
- **Deindexing**: on delete, entries are removed from `_search_index` and stats decremented
- **BM25 scoring**: uses standard parameters (k1=1.5, b=0.75) with configurable field boosts
- **Non-atomic** (PostgreSQL): index updates happen in a separate transaction, acceptable for search indices

## Data Flow Diagrams

### Insert Flow (SQLite)

```
User calls db.insert(obj)
  │
  ├── asdict(obj) → raw dict
  ├── data_formatter() → serialized dict
  ├── _compute_record_id() → MD5 hash
  ├── acquire _write_lock
  │
  ├── session.add(Model(**data_dict))
  │
  ├── if FTS enabled:
  │     └── _insert_into_fts(session, record_id, data_dict)
  │         └── INSERT INTO {table}_fts VALUES (...)
  │
  ├── session.commit()
  ├── release _write_lock
  └── return record_id
```

### Search Flow (SQLite FTS)

```
User calls db.search(use_fts=True, fts_query="Sci-Fi")
  │
  ├── _stream_search()
  │
  ├── if use_fts and fts_query:
  │     └── SELECT record_id FROM {table}_fts WHERE {table}_fts MATCH 'Sci-Fi'
  │     └── Get candidate record_ids
  │
  ├── Paginate through main table using record_id IN (...)
  │
  ├── Apply predicate (if provided)
  │
  ├── Convert rows to dataclass objects via _batch_converter()
  │
  └── Yield results
```

### BM25 Search Flow (PicodoSearch)

```
User calls search_engine.search_index("query", limit=10)
  │
  ├── Tokenize query → [term1, term2, ...]
  │
  ├── SELECT DISTINCT record_id FROM _search_index WHERE term IN (term1, term2, ...)
  │   → candidate_ids
  │
  ├── Get term stats from _search_stats (doc_count per term)
  │
  ├── Get total_docs and avg_doc_len
  │
  ├── For each candidate record_id:
  │     ├── Get term frequencies for this record
  │     ├── Get document length (total terms)
  │     ├── For each matching term:
  │     │     └── BM25 score = IDF * TF_norm * field_boost
  │     └── Sum scores → total relevance score
  │
  ├── Sort by score descending
  │
  ├── Apply offset/limit
  │
  ├── Fetch full records via super().get(record_id)
  │
  └── Return List[Tuple[record, score]]
```

## Key Design Decisions

1. **MD5-based record_id** — Deterministic IDs allow idempotent inserts and easy deduplication. Hash collisions are handled with UUID suffixes.

2. **Composition over inheritance for search/cache** — `PicodoSearch` and `PicodoCache` extend `AsyncPicodb` but add sidecar tables. This keeps the base class clean while allowing optional features.

3. **FTS auto-population via triggers (PG) and inline inserts (SQLite)** — Both backends keep the FTS index in sync with the main data without user intervention.

4. **Lazy TTL expiry** — Cache keys are checked for expiry on read operations, avoiding background cleanup tasks.

5. **Batch streaming with internal buffering** — `stream_all_batches` uses an internal batch size of 5000 for efficient DB round-trips, then yields user-sized batches.

6. **orjson for serialization** — Used throughout for fast JSON encoding/decoding of complex types (lists, dicts, dataclasses).