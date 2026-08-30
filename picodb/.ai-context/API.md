# PicoDB API Reference

## `AsyncPicodb[SchemaT]`

Main SQLite ORM class. Generic over a dataclass schema type.

### Constructor

```python
AsyncPicodb(
    schema_cls: Type[SchemaT],
    path: str = "sqlite+aiosqlite:///imdb.db",
    *,
    indexes: Optional[List[Dict[str, Any]]] = None,
    enable_fts: bool = True,
    fts_fields: Optional[List[str]] = None,
    fts_populate: bool = True,
    page_size: int = 1000,
    pragma_options: Optional[Dict[str, Any]] = None,
)
```

### Methods

| Method | Signature | Description |
|---|---|---|
| `init_db` | `init_db() -> Awaitable[None]` | Create tables, indexes, FTS virtual tables, and apply PRAGMAs |
| `clear_db` | `clear_db() -> Awaitable[None]` | Drop all tables and recreate (destructive) |
| `insert` | `insert(obj: SchemaT) -> Awaitable[str]` | Insert a single record; returns `record_id` |
| `insert_many` | `insert_many(objects, chunk_size=10000, atomic=False) -> Awaitable[List[str]]` | Bulk insert records in chunks |
| `get` | `get(record_id: str) -> Awaitable[Optional[SchemaT]]` | Get a record by its `record_id` |
| `update` | `update(record_id: str, new_obj: SchemaT) -> Awaitable[None]` | Update a record by `record_id` |
| `delete` | `delete(record_id: str) -> Awaitable[None]` | Delete a record by `record_id` |
| `delete_many` | `delete_many(record_ids, batch_size=1000) -> Awaitable[int]` | Bulk delete records |
| `stream_all` | `stream_all(limit=None, order_by=None, desc=False) -> AsyncIterator[SchemaT]` | Stream all records with optional ordering |
| `stream_all_batches` | `stream_all_batches(batch_size=100, limit=None, ...) -> AsyncIterator[List[SchemaT]]` | Stream records in batches |
| `count_records` | `count_records() -> Awaitable[int]` | Count total records |
| `search` | `search(predicate=None, pre_filter=None, use_fts=False, fts_query=None, limit=None, offset=0) -> Awaitable[List[SchemaT]]` | Search with optional FTS and predicate |
| `stream_search` | `stream_search(...) -> AsyncIterator[SchemaT]` | Async iterator version of `search` |
| `exists` | `exists(predicate=None, pre_filter=None) -> Awaitable[bool]` | Check if any record matches |
| `exists_many` | `exists_many(values, field, ...) -> Awaitable[Dict]` | Check existence of multiple values in a field |
| `distinct_values` | `distinct_values(field, pre_filter=None, order_by=None) -> Awaitable[List]` | Get distinct values for a field |
| `value_counts` | `value_counts(field, pre_filter=None, order_by_count=True, limit=None) -> Awaitable[Dict]` | Count occurrences per unique value |
| `query` | `query() -> Q` | Get a chainable query builder |
| `close` | `close() -> Awaitable[None]` | Dispose the engine |

### Properties

| Property | Type | Description |
|---|---|---|
| `schema_cls` | `Type[SchemaT]` | The dataclass schema |
| `db_path` | `str` | Database connection path |
| `engine` | `AsyncEngine` | SQLAlchemy async engine |
| `session_factory` | `async_sessionmaker` | Session factory |
| `_model` | `Type[DeclarativeBase]` | Generated SQLAlchemy model |
| `_table_name` | `str` | Table name (lowercase schema class name) |
| `_fts_enabled` | `bool` | Whether FTS is enabled |
| `_fts_fields` | `List[str]` | FTS indexed fields |
| `_page_size` | `int` | Default page size for streaming |

---

## `AsyncPicodoPG[SchemaT]`

PostgreSQL variant of `AsyncPicodb`. Same API with these differences:

- Uses `asyncpg` + PostgreSQL-specific types (`TSVECTOR`, `JSONB`, `BigInteger`)
- `user_id` fields auto-map to `BigInteger` instead of `Integer`
- FTS uses `tsvector`/`tsquery` with GIN index and trigger-based auto-population
- Connection pooling configurable via `pool_size` and `max_overflow`

### Constructor

```python
AsyncPicodoPG(
    schema_cls: Type[SchemaT],
    path: str = "postgresql+asyncpg://user:password@localhost/dbname",
    *,
    indexes: Optional[List[Dict[str, Any]]] = None,
    enable_fts: bool = True,
    fts_fields: Optional[List[str]] = None,
    fts_populate: bool = True,
    page_size: int = 1000,
    pool_size: int = 20,
    max_overflow: int = 20,
)
```

### Additional Methods (over AsyncPicodb)

| Method | Signature | Description |
|---|---|---|
| `search_fts` | `search_fts(query, limit=100, offset=0, ranking=True) -> Awaitable[List[str]]` | PostgreSQL FTS search with optional ranking |
| `search_fts_advanced` | `search_fts_advanced(query, limit=100, offset=0) -> Awaitable[List[str]]` | Advanced FTS with boolean operators (`& \| ! <->`) |
| `rebuild_fts` | `rebuild_fts(batch_size=20000) -> Awaitable[None]` | Rebuild FTS vector column for all records |
| `fts_stats` | `fts_stats() -> Awaitable[dict]` | Get FTS index statistics |

---

## `PicodoCache[SchemaT]`

Redis-like cache layer extending `AsyncPicodb`. Adds key-value store, set operations, and TTL support via sidecar tables (`_kv_store`, `_set_store`).

### Constructor

```python
PicodoCache(
    schema_cls: Type[SchemaT],
    path: str = "sqlite+aiosqlite:///cache.db",
    **kwargs
)
```

### Key-Value Methods

| Method | Signature | Description |
|---|---|---|
| `set` | `set(key, value, ttl=None) -> Awaitable[None]` | Store a value with optional TTL (seconds) |
| `get_cache` | `get_cache(key, default=None) -> Awaitable[Any]` | Retrieve a value (returns `default` if missing/expired) |
| `get` | `get(key, default=None) -> Awaitable[Any]` | Alias for `get_cache` (Redis-like API) |
| `delete_key` | `delete_key(key) -> Awaitable[bool]` | Delete a cache key |
| `exists_key` | `exists_key(key) -> Awaitable[bool]` | Check if key exists and is not expired |
| `keys` | `keys(pattern=None) -> Awaitable[List[str]]` | List keys, optionally filtered by GLOB pattern |
| `mset` | `mset(mapping) -> Awaitable[None]` | Set multiple key-value pairs at once |
| `mget` | `mget(keys) -> Awaitable[Dict[str, Any]]` | Get multiple keys at once |
| `incr` | `incr(key, amount=1) -> Awaitable[int]` | Increment numeric value (creates if missing) |
| `decr` | `decr(key, amount=1) -> Awaitable[int]` | Decrement numeric value |
| `expire` | `expire(key, ttl) -> Awaitable[bool]` | Set TTL on an existing key |
| `ttl` | `ttl(key) -> Awaitable[int]` | Get remaining TTL in seconds (-1=no expiry, -2=missing/expired) |
| `evict_expired` | `evict_expired() -> Awaitable[int]` | Delete all expired keys |

### Set Methods

| Method | Signature | Description |
|---|---|---|
| `sadd` | `sadd(key, *members) -> Awaitable[int]` | Add members to a set |
| `srem` | `srem(key, *members) -> Awaitable[int]` | Remove members from a set |
| `smembers` | `smembers(key) -> Awaitable[Set[str]]` | Get all members of a set |
| `sismember` | `sismember(key, member) -> Awaitable[bool]` | Check if member is in set |
| `scard` | `scard(key) -> Awaitable[int]` | Get cardinality of a set |

---

## `PicodoSearch[SchemaT]`

Inverted index + BM25 search engine extending `AsyncPicodb` (SQLite) or `AsyncPicodoPG` (PostgreSQL).

### Constructor

```python
PicodoSearch(
    schema_cls: Type[SchemaT],
    path: str = "sqlite+aiosqlite:///search.db",
    *,
    search_fields: List[str],
    field_boosts: Optional[Dict[str, float]] = None,
    **kwargs
)
```

### Methods

| Method | Signature | Description |
|---|---|---|
| `search_index` | `search_index(query, limit=10, offset=0, ranking="bm25") -> Awaitable[List[Tuple[SchemaT, float]]]` | Search with BM25 ranking; returns (record, score) pairs |
| `rebuild_search_index` | `rebuild_search_index() -> Awaitable[int]` | Rebuild entire search index from scratch |
| `search_stats` | `search_stats() -> Awaitable[Dict[str, Any]]` | Get index statistics |

---

## `Q` — Query Builder

Chainable query builder for composable database operations.

### Constructor

```python
Q(model, db)
```

### Filter Methods

| Method | Signature | Description |
|---|---|---|
| `eq` | `eq(field, value)` | Equality (`=`) |
| `noeq` | `noeq(field, value)` | Not equal (`!=`) |
| `gt` | `gt(field, value)` | Greater than (`>`) |
| `lt` | `lt(field, value)` | Less than (`<`) |
| `gte` | `gte(field, value)` | Greater than or equal (`>=`) |
| `lte` | `lte(field, value)` | Less than or equal (`<=`) |
| `like` | `like(field, pattern, *, case_sensitive=True)` | LIKE pattern matching |
| `ilike` | `ilike(field, pattern)` | Case-insensitive LIKE |
| `in_` | `in_(field, values)` | IN operator |
| `not_in` | `not_in(field, values)` | NOT IN operator |
| `between` | `between(field, start, end)` | BETWEEN operator |
| `where` | `where(*conditions)` | Add raw SQLAlchemy conditions |
| `or_` | `or_(*conditions)` | OR condition |
| `and_` | `and_(*conditions)` | AND condition |

### Ordering Methods

| Method | Signature | Description |
|---|---|---|
| `order_by` | `order_by(*fields, cast_int=False)` | Order by field names; prefix with `-` for descending |
| `order_by_raw` | `order_by_raw(*expressions, direction=None)` | Order by raw SQLAlchemy expressions |

### Pagination

| Method | Signature | Description |
|---|---|---|
| `limit` | `limit(n)` | Limit result count |
| `offset` | `offset(n)` | Offset result start |

### Execution Methods

| Method | Signature | Description |
|---|---|---|
| `build` | `build() -> Select` | Build SQLAlchemy statement |
| `search` | `search() -> Awaitable[List[SchemaT]]` | Execute and return list |
| `stream` | `stream() -> AsyncIterator[SchemaT]` | Execute and stream results |
| `count` | `count() -> Awaitable[int]` | Count matching records |
| `delete` | `delete() -> Awaitable[None]` | Delete matching records |
| `update` | `update(**values) -> Awaitable[None]` | Update matching records |

---

## `FtsMixin` (SQLite FTS5)

Mixin providing FTS5 full-text search for `AsyncPicodb`.

| Method | Signature | Description |
|---|---|---|
| `_insert_into_fts` | `_insert_into_fts(session, record_id, data_dict)` | Insert record into FTS index (internal) |
| `_delete_from_fts` | `_delete_from_fts(session, record_id)` | Delete record from FTS index (internal) |
| `enable_fts_populate` | `enable_fts_populate(flag)` | Enable/disable FTS population on inserts |
| `rebuild_fts` | `rebuild_fts(batch_size=20000)` | Rebuild FTS index from all records |
| `search_fts` | `search_fts(query, limit=100, offset=0) -> Awaitable[List[str]]` | Search FTS index; returns record_ids |
| `load_imdb_dataset` | `load_imdb_dataset(items, chunk_size=5000)` | Bulk load with optimized FTS population |

---

## `FtsMixinPG` (PostgreSQL FTS)

Mixin providing PostgreSQL `tsvector`/`tsquery` FTS for `AsyncPicodoPG`.

| Method | Signature | Description |
|---|---|---|
| `search_fts` | `search_fts(query, limit=100, offset=0, ranking=True) -> Awaitable[List[str]]` | FTS search with optional `ts_rank` relevance ranking |
| `search_fts_advanced` | `search_fts_advanced(query, limit=100, offset=0) -> Awaitable[List[str]]` | Advanced FTS with boolean operators (`& \| ! <->`) |
| `rebuild_fts` | `rebuild_fts(batch_size=20000)` | Re-populate `fts_vector` for all records |
| `enable_fts_populate` | `enable_fts_populate(flag)` | API compatibility (PostgreSQL uses triggers) |
| `fts_stats` | `fts_stats() -> Awaitable[dict]` | Get FTS index statistics |

---

## `data_formatter`

```python
def data_formatter(value: Any) -> Any
```

Converts Python values to database-storable format:
- `None` → `None`
- `bool` → `bool` (unchanged)
- `datetime.date` / `datetime.datetime` → ISO format string
- `list` / `dict` / `tuple` → JSON string (via `orjson`)
- `int` / `float` → unchanged
- Other → `str(value)`