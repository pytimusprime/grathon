---
name: PicoDB v4.1 - Complete Reference
description: Complete PicoDB async SQLite/PostgreSQL API with all methods, features, patterns, and examples
type: reference
originSessionId: ae842a23-1135-445b-8164-2bc42a82bd24
---
# PicoDB v4.1 - Complete Reference

## 📋 Overview

**PicoDB** = Async SQLite/PostgreSQL wrapper with:
- Dataclass-based schemas (auto table generation)
- Full-Text Search (FTS5 for SQLite, native for PostgreSQL)
- Chainable Query Builder (`.query().eq().search()`)
- Redis-like Cache Layer (key-value + sets)
- Inverted Index Search with BM25 ranking
- Bulk operations (insert_many, delete_many)
- Auto record ID generation (MD5 hash)

---

## 1. Architecture

```
PicoDB
├── AsyncPicodb[SchemaT]        # Main SQLite class
│   ├── FtsMixin                # Full-Text Search
│   ├── insert() / get()        # CRUD
│   └── query()                 # Query builder
│
├── AsyncPicodoPG[SchemaT]      # PostgreSQL variant
│   ├── FtsMixinPG              # Native PostgreSQL FTS
│   ├── Connection pooling      # Configurable pool
│   └── Same API as AsyncPicodb
│
├── Q[SchemaT]                  # Query Builder
│   ├── .eq() / .noeq()         # Comparison
│   ├── .gt() / .lt() / .gte() / .lte()
│   ├── .like() / .ilike()
│   ├── .in_() / .not_in()
│   ├── .between()
│   ├── .order_by()
│   ├── .limit() / .offset()
│   └── .search() / .stream() / .count() / .update() / .delete()
│
├── PicodoCache[SchemaT]        # Redis-like cache
│   ├── .set() / .get()         # Key-value
│   ├── .sadd() / .smembers()   # Sets
│   └── .cleanup_expired()      # TTL management
│
└── PicodoSearch[SchemaT]       # BM25 search engine
    ├── .search()               # Search with ranking
    └── .rebuild_index()        # Rebuild inverted index
```

---

## 2. AsyncPicodb - SQLite Core

### Constructor

```python
AsyncPicodb(
    schema_cls: Type[SchemaT],
    path: str = "sqlite+aiosqlite:///db.db",
    *,
    indexes: Optional[List[Dict]] = None,
    enable_fts: bool = True,
    fts_fields: Optional[List[str]] = None,
    fts_populate: bool = True,
    page_size: int = 1000,
    pragma_options: Optional[Dict] = None,
)
```

### PRAGMA Settings (Default)

```python
{
    "journal_mode": "WAL",              # Write-Ahead Logging
    "synchronous": "NORMAL",            # Balance safety/speed
    "temp_store": "MEMORY",             # Temp data in RAM
    "mmap_size": 268435456,             # 256MB memory-mapped I/O
    "cache_size": -131072,              # 128MB page cache
    "read_uncommitted": True,           # Concurrent reads
}
```

### Indexes

```python
# Simple index
indexes=[
    {'fields': ['email'], 'unique': True},
    {'fields': ['status', 'created_at']},
]

# Complex index with WHERE clause
indexes=[
    {'fields': ['status'], 'where': "status = 'active'"},
    {'expr': 'LOWER(email)', 'name': 'idx_email_lower'},
]
```

---

## 3. AsyncPicodb - Complete Methods

### Lifecycle

```python
await db.init_db()              # Create tables, indexes, FTS
await db.close()                # Close connections
await db.clear_db()             # Drop and recreate tables
```

### Insert Operations

```python
# Single insert → returns record_id (str)
record_id = await db.insert(user_obj)

# Bulk insert
ids = await db.insert_many(
    [user1, user2, user3, ...],
    chunk_size=5000,            # Records per batch
    atomic=False,               # False: commit per chunk, True: one commit
) → List[str]

# Record ID = MD5 hash of data (deterministic)
# Collision handling: auto-retry with UUID suffix
```

### Read Operations

```python
# Get by ID
user = await db.get(record_id) → Optional[SchemaT]

# Count records
total = await db.count_records() → int

# Check if exists
exists = await db.exists(predicate=lambda u: u.age > 30) → bool

# Check many exist
results = await db.exists_many(
    ['user1@test.com', 'user2@test.com'],
    field='email',
    return_existing=True,       # Return only existing
) → List[str]
```

### Stream Operations

```python
# Stream all records
async for user in db.stream_all(
    limit=None,
    order_by='created_at',      # Field name
    desc=False,                 # Descending?
):
    await process(user)

# Stream in batches (memory efficient)
async for batch in db.stream_all_batches(
    batch_size=100,
    limit=None,
    order_by=None,
    desc=False,
):
    # batch = List of records
    await process_batch(batch)
```

### Query Operations

```python
# Query builder
results = await db.query()\
    .eq('status', 'active')\
    .gt('age', 30)\
    .order_by('-created_at')\
    .limit(100)\
    .search() → List[SchemaT]

# Stream search results
async for user in db.stream_search(
    use_fts=True,
    fts_query="python developer",
    limit=100,
):
    await process(user)

# Search with predicate
results = await db.search(
    predicate=lambda u: u.age > 25,
    limit=50,
) → List[SchemaT]
```

### Update & Delete

```python
# Update single record
updated = User(..., record_id="abc123")
await db.update(record_id, updated)

# Bulk delete
deleted_count = await db.delete_many(
    [id1, id2, id3, ...],
    batch_size=1000,
) → int

# Delete via query
await db.query().eq('status', 'deleted').delete()
```

### Analysis Operations

```python
# Get unique values
categories = await db.distinct_values(
    'category',
    pre_filter=db.query().eq('active', True),  # Optional filter
    order_by='-name',                          # Optional ordering
) → List[Any]

# Count occurrences
status_counts = await db.value_counts(
    'status',
    order_by_count=True,        # Sort by count?
    limit=10,                   # Top 10
) → Dict[str, int]
# Returns: {'active': 1000, 'inactive': 500, ...}
```

### Internal Methods

```python
record_id = db._compute_record_id(data_dict)  # MD5 hash
model = db._create_model()                     # Generate SQLAlchemy model
converter = db._batch_converter()              # Get converter function
```

---

## 4. Query Builder (Q) - Complete

### Creation & Execution

```python
# Create builder (not executed)
q = db.query()

# Execute to list
results = await q.eq('status', 'active').search() → List[SchemaT]

# Stream results
async for item in await q.eq('active', True).stream():
    ...

# Count matches
count = await q.eq('status', 'active').count() → int

# Update matching
await q.eq('category', 1).update(price=9999) → None

# Delete matching
await q.eq('status', 'deleted').delete() → None
```

### Filter Methods

```python
.eq(field, value)                # =
.noeq(field, value)              # !=
.gt(field, value)                # >
.lt(field, value)                # <
.gte(field, value)               # >=
.lte(field, value)               # <=
.like(field, pattern, case_sensitive=True)   # LIKE
.ilike(field, pattern)           # Case-insensitive LIKE
.in_(field, [values])            # IN
.not_in(field, [values])         # NOT IN
.between(field, start, end)      # BETWEEN
.where(*conditions)              # Raw SQLAlchemy conditions
.or_(*conditions)                # OR
.and_(*conditions)               # AND (explicit)
```

### Ordering & Pagination

```python
.order_by('field', '-field2', cast_int=False)  # '-' = desc
.order_by_raw(*expressions, direction='desc')  # Raw SQLAlchemy
.limit(n)                        # Limit result count
.offset(n)                       # Skip N results
```

### Examples

```python
# All active users over 25
results = await db.query()\
    .eq('status', 'active')\
    .gt('age', 25)\
    .order_by('-created_at')\
    .limit(100)\
    .search()

# Case-insensitive email search
results = await db.query()\
    .ilike('email', '%gmail%')\
    .search()

# Between range
products = await db.query()\
    .between('price', 100, 5000)\
    .eq('in_stock', True)\
    .order_by('-rating')\
    .search()

# Multiple values (IN)
results = await db.query()\
    .in_('status', ['active', 'pending'])\
    .search()

# Count without fetching
count = await db.query()\
    .eq('category', 5)\
    .count()

# Delete all inactive
await db.query()\
    .eq('status', 'inactive')\
    .delete()
```

---

## 5. Full-Text Search (FTS)

### SQLite FTS5

```python
db = AsyncPicodb(
    Product,
    fts_fields=['title', 'description'],  # Indexed fields
    enable_fts=True,
    fts_populate=True,                    # Auto-populate on insert
)

# Search (returns record IDs)
matching_ids = await db.search_fts(
    'query text',
    limit=100,
    offset=0,
) → List[str]

# Rebuild after bulk updates
await db.rebuild_fts(batch_size=20000)

# Toggle auto-population
db.enable_fts_populate(False)  # Disable for bulk load
await db.insert_many(...)      # Bulk insert (faster)
db.enable_fts_populate(True)   # Re-enable
await db.rebuild_fts()         # Index all at once

# Tokenization rules:
# - Lowercase + split on word boundaries
# - Remove stopwords ("the", "and", "is", etc.)
# - Min token length: 2 chars
# - Rank by term frequency
```

### PostgreSQL FTS (Native)

```python
db = AsyncPicodoPG(
    Product,
    fts_fields=['title', 'body'],
    enable_fts=True,
)

# Uses PostgreSQL native tsvector (faster than SQLite)
# Same API as SQLite
matching_ids = await db.search_fts('query', limit=100)
```

---

## 6. Cache Layer (PicodoCache)

Extends AsyncPicodb with Redis-like operations.

```python
from picodb import PicodoCache

cache = PicodoCache(
    User,
    path="sqlite+aiosqlite:///cache.db"
)
await cache.init_db()

# Key-Value (with TTL)
await cache.set('user:123', {'name': 'Alice'}, ttl=3600)  # 1 hour
value = await cache.get('user:123') → Optional[dict]
await cache.delete_key('user:123')

# Sets (multiple values under one key)
await cache.sadd('tags:python', 'async')
await cache.sadd('tags:python', 'web')
members = await cache.smembers('tags:python') → Set[str]
# Returns: {'async', 'web'}

await cache.srem('tags:python', 'async')  # Remove from set
await cache.delete_key('tags:python')     # Delete entire set

# Expiry management
expired = await cache.get_expired_keys() → List[str]
await cache.cleanup_expired()  # Delete expired entries
```

**Storage:**
- `_kv_store` table: (key, value, expires_at)
- `_set_store` table: (key, member) with TTL

---

## 7. Search Engine (PicodoSearch)

Inverted index + BM25 ranking (alternative to FTS).

```python
from picodb import PicodoSearch

search = PicodoSearch(Article, db)

# Index single record
await search.index_record(record_id, {'title': 'Python Async', 'body': '...'})

# Rebuild entire index
await search.rebuild_index()

# Search with BM25 scoring
results = await search.search('python async', limit=100)
# Returns: [(record_id, score), ...]

# Set field importance
search.set_field_boost({'title': 2.0, 'body': 1.0})

# BM25 parameters (k1=1.5, b=0.75, k3=1.0)
# Supports phrase queries: "quoted string"
```

---

## 8. PostgreSQL Variant (AsyncPicodoPG)

Drop-in replacement using PostgreSQL.

```python
from picodb import AsyncPicodoPG

db = AsyncPicodoPG(
    User,
    path="postgresql+asyncpg://user:pass@localhost/dbname",
    enable_fts=True,
    fts_fields=['username', 'email'],
    pool_size=20,
    max_overflow=10,
)
await db.init_db()

# API identical to AsyncPicodb
results = await db.query().eq('status', 'active').search()
await db.insert(user)
```

**Differences:**
- Native `tsvector` FTS (faster than SQLite)
- Connection pooling (configurable)
- Better for concurrent writes
- No PRAGMA settings (PostgreSQL config instead)

---

## 9. Data Formatting

```python
from picodb.formatter import data_formatter

# Auto-converts Python types to storage format:
# datetime/date → ISO string
# list/dict/tuple → JSON (orjson)
# bool/int/float → stored as-is
# None → None
# Everything else → str()

# Used automatically in insert/update
```

---

## 10. Record ID System

```python
# Record ID = MD5 hash (deterministic)
# Same data = same ID (idempotent)

# MD5 hash computed from:
# 1. Normalized values (dates→ISO, dicts→JSON)
# 2. Sorted dict keys
# 3. JSON encoding
# 4. MD5 hash

# Collision handling:
# If hash collision detected:
# 1. First retry: try again (rare)
# 2. Second retry: append UUID suffix
# 3. After 3 retries: raise exception

# Manual override:
user = User(name="Alice", record_id="my_custom_id")
await db.insert(user)
```

---

## 11. Real-World Patterns

### User Management

```python
@dataclass
class User:
    username: str
    email: str
    age: int
    status: str  # 'active', 'suspended'
    tags: List[str] = None
    record_id: str = ""

db = AsyncPicodb(
    User,
    indexes=[
        {'fields': ['email'], 'unique': True},
        {'fields': ['status', 'created_at']},
    ],
    fts_fields=['username', 'email'],
)

# Create
user = User(username="alice", email="alice@test.com", age=30, status='active')
record_id = await db.insert(user)

# Find active users
active = await db.query().eq('status', 'active').order_by('-created_at').search()

# Search by text
results = await db.search_fts('alice', limit=50)

# Update status
suspended = await db.get(record_id)
suspended.status = 'suspended'
await db.update(record_id, suspended)

# Ban multiple
await db.query().in_('username', ['spammer1', 'spammer2']).update(status='banned')

# Get stats
total = await db.count_records()
active_count = await db.query().eq('status', 'active').count()

# Get unique statuses
statuses = await db.distinct_values('status')

# Count by status
counts = await db.value_counts('status')
# Returns: {'active': 1000, 'suspended': 50, ...}
```

### E-Commerce Products

```python
@dataclass
class Product:
    name: str
    description: str
    price: float
    category: str
    stock: int
    rating: float
    record_id: str = ""

db = AsyncPicodb(
    Product,
    indexes=[
        {'fields': ['category']},
        {'fields': ['price']},
        {'fields': ['stock'], 'where': "stock > 0"},  # Partial index
    ],
    fts_fields=['name', 'description'],
)

# Find in stock, price range
results = await db.query()\
    .between('price', 100, 5000)\
    .gt('stock', 0)\
    .order_by('-rating')\
    .limit(50)\
    .search()

# Search products
ids = await db.search_fts('laptop computer', limit=100)

# Get categories
categories = await db.distinct_values('category')

# Top rated in category
top_rated = await db.query()\
    .eq('category', 'electronics')\
    .order_by('-rating')\
    .limit(10)\
    .search()

# Update stock
await db.query().eq('category', 'sale').update(price=0.5 * price)  # 50% off

# Bulk delete out-of-stock
await db.query().lte('stock', 0).delete()
```

### Caching Pattern

```python
cache = PicodoCache(User)
db = AsyncPicodb(User)

# Cache-aside pattern
async def get_user(user_id: str):
    # Try cache first
    cached = await cache.get(f'user:{user_id}')
    if cached:
        return cached
    
    # Fetch from DB
    user = await db.get(user_id)
    if user:
        # Store in cache (1 hour TTL)
        await cache.set(f'user:{user_id}', {'name': user.name, 'email': user.email}, ttl=3600)
    
    return user

# Invalidate on update
async def update_user(user_id: str, updated: User):
    await db.update(user_id, updated)
    await cache.delete_key(f'user:{user_id}')  # Clear cache
```

### Bulk Import

```python
# Disable FTS for faster import
db.enable_fts_populate(False)

# Insert many
users = [User(...) for _ in range(100000)]
ids = await db.insert_many(users, chunk_size=10000, atomic=False)

# Re-enable and rebuild
db.enable_fts_populate(True)
await db.rebuild_fts()
```

---

## 12. Complete CRUD Example

```python
from dataclasses import dataclass
from picodb import AsyncPicodb

@dataclass
class Article:
    title: str
    content: str
    author: str
    published: bool = False
    record_id: str = ""

db = AsyncPicodb(Article, fts_fields=['title', 'content'])
await db.init_db()

# CREATE
article = Article(title="Python Async", content="...", author="Alice")
rid = await db.insert(article)

# READ
article = await db.get(rid)

# UPDATE
article.published = True
await db.update(rid, article)

# DELETE
await db.delete(rid)

# SEARCH
results = await db.query().eq('author', 'Alice').search()

# FTS
matched = await db.search_fts('python async')

# CLOSE
await db.close()
```

---

## Summary Table

| Operation | Method | Returns | Async? |
|-----------|--------|---------|--------|
| Create | `insert(obj)` | str (record_id) | ✅ |
| Bulk create | `insert_many(objs)` | List[str] | ✅ |
| Read by ID | `get(id)` | Optional[SchemaT] | ✅ |
| Read all | `stream_all()` | AsyncIterator | ✅ |
| Query | `query().search()` | List[SchemaT] | ✅ |
| Stream query | `query().stream()` | AsyncIterator | ✅ |
| Count | `query().count()` | int | ✅ |
| Update | `update(id, obj)` | None | ✅ |
| Update many | `query().update()` | None | ✅ |
| Delete | `delete(id)` | None | ✅ |
| Delete many | `delete_many(ids)` | int | ✅ |
| Query delete | `query().delete()` | None | ✅ |
| Search FTS | `search_fts(q)` | List[str] | ✅ |
| Analyze | `distinct_values(f)` | List[Any] | ✅ |
| Analyze | `value_counts(f)` | Dict[Any, int] | ✅ |
