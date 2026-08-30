# PicoDB Examples

## 1. Basic CRUD with SQLite

```python
from dataclasses import dataclass
from picodb import AsyncPicodb

@dataclass
class Movie:
    title: str
    year: int
    genre: str
    rating: float

db = AsyncPicodb(Movie, path="sqlite+aiosqlite:///movies.db", fts_fields=["title", "genre"])
await db.init_db()

# Insert
rid = await db.insert(Movie(title="Inception", year=2010, genre="Sci-Fi", rating=8.8))

# Get
movie = await db.get(rid)
print(movie.title)  # "Inception"

# Update
movie.rating = 9.0
await db.update(rid, movie)

# Delete
await db.delete(rid)

await db.close()
```

## 2. Bulk Insert

```python
from dataclasses import dataclass
from picodb import AsyncPicodb

@dataclass
class Movie:
    title: str
    year: int
    genre: str
    rating: float

db = AsyncPicodb(Movie, path="sqlite+aiosqlite:///movies.db")
await db.init_db()

movies = [
    Movie(title="Inception", year=2010, genre="Sci-Fi", rating=8.8),
    Movie(title="Interstellar", year=2014, genre="Sci-Fi", rating=8.7),
    Movie(title="The Dark Knight", year=2008, genre="Action", rating=9.0),
]

rids = await db.insert_many(movies, chunk_size=1000)
print(f"Inserted {len(rids)} movies")

await db.close()
```

## 3. Query Builder

```python
from dataclasses import dataclass
from picodb import AsyncPicodb

@dataclass
class Movie:
    title: str
    year: int
    genre: str
    rating: float

db = AsyncPicodb(Movie, path="sqlite+aiosqlite:///movies.db")
await db.init_db()

# Filter by genre and rating, ordered by rating descending
results = await db.query() \
    .eq("genre", "Sci-Fi") \
    .gte("rating", 8.0) \
    .order_by("-rating") \
    .limit(10) \
    .search()

for movie in results:
    print(f"{movie.title} ({movie.year}) — {movie.rating}")

# LIKE search
results = await db.query() \
    .like("title", "%Dark%", case_sensitive=False) \
    .search()

# IN operator
results = await db.query() \
    .in_("genre", ["Sci-Fi", "Action"]) \
    .order_by("-rating") \
    .search()

# BETWEEN
results = await db.query() \
    .between("year", 2000, 2015) \
    .search()

# OR condition
results = await db.query() \
    .or_(
        db.query().model.title == "Inception",
        db.query().model.genre == "Action",
    ) \
    .search()

await db.close()
```

## 4. Full-Text Search (SQLite FTS5)

```python
from dataclasses import dataclass
from picodb import AsyncPicodb

@dataclass
class Movie:
    title: str
    year: int
    genre: str
    rating: float

db = AsyncPicodb(Movie, path="sqlite+aiosqlite:///movies.db", fts_fields=["title", "genre"])
await db.init_db()

# Insert some movies
await db.insert(Movie(title="Inception", year=2010, genre="Sci-Fi", rating=8.8))
await db.insert(Movie(title="Interstellar", year=2014, genre="Sci-Fi", rating=8.7))
await db.insert(Movie(title="The Dark Knight", year=2008, genre="Action", rating=9.0))

# FTS search
results = await db.search(use_fts=True, fts_query="Sci-Fi", limit=10)
for movie in results:
    print(movie.title)

# FTS search with streaming
async for movie in db.stream_search(use_fts=True, fts_query="Dark", limit=5):
    print(movie.title)

# Rebuild FTS index (after bulk operations)
await db.rebuild_fts()

await db.close()
```

## 5. PostgreSQL with Native FTS

```python
from dataclasses import dataclass
from picodb import AsyncPicodoPG

@dataclass
class Movie:
    title: str
    year: int
    genre: str
    rating: float

db = AsyncPicodoPG(
    Movie,
    path="postgresql+asyncpg://user:password@localhost/movies",
    fts_fields=["title", "genre"],
    pool_size=10,
)
await db.init_db()

# Insert
rid = await db.insert(Movie(title="Inception", year=2010, genre="Sci-Fi", rating=8.8))

# PostgreSQL FTS search with ranking
results = await db.search_fts("Sci-Fi", ranking=True)
# Returns record_ids sorted by ts_rank relevance

# Advanced FTS with boolean operators
results = await db.search_fts_advanced("Sci-Fi & Inception")
# Finds records containing both "Sci-Fi" and "Inception"

# FTS statistics
stats = await db.fts_stats()
print(stats)  # {"indexed_records": 3, "total_records": 3, "fts_enabled": True, ...}

await db.close()
```

## 6. Redis-like Cache

```python
from dataclasses import dataclass
from picodb import PicodoCache

@dataclass
class Session:
    user_id: int
    data: dict

cache = PicodoCache(Session, path="sqlite+aiosqlite:///cache.db")
await cache.init_db()

# Set with TTL (expires in 1 hour)
await cache.set("session:user_123", {"cart": ["item1", "item2"]}, ttl=3600)

# Get
data = await cache.get("session:user_123")
print(data)  # {"cart": ["item1", "item2"]}

# Check expiry
remaining = await cache.ttl("session:user_123")
print(f"TTL remaining: {remaining} seconds")

# Set operations
await cache.sadd("online_users", "user_1", "user_2", "user_3")
members = await cache.smembers("online_users")
print(members)  # {"user_1", "user_2", "user_3"}

is_online = await cache.sismember("online_users", "user_1")
print(is_online)  # True

# Increment counter
count = await cache.incr("page_views:home")
print(count)  # 1
count = await cache.incr("page_views:home")
print(count)  # 2

# List all keys matching a pattern
keys = await cache.keys("session:*")
print(keys)

# Delete expired keys
evicted = await cache.evict_expired()
print(f"Evicted {evicted} expired keys")

await cache.close()
```

## 7. BM25 Search Engine

```python
from dataclasses import dataclass
from picodb import PicodoSearch

@dataclass
class Article:
    title: str
    content: str
    author: str

search_db = PicodoSearch(
    Article,
    path="sqlite+aiosqlite:///search.db",
    search_fields=["title", "content", "author"],
    field_boosts={"title": 2.0, "content": 1.0, "author": 1.5},
)
await search_db.init_db()

# Insert articles (automatically indexed)
await search_db.insert(Article(
    title="Introduction to Databases",
    content="Databases are organized collections of data...",
    author="Jane Smith",
))

await search_db.insert(Article(
    title="Advanced SQL Techniques",
    content="Learn advanced SQL queries and optimization...",
    author="John Doe",
))

# Search with BM25 ranking
results = await search_db.search_index("database SQL", limit=5)
for article, score in results:
    print(f"[{score:.4f}] {article.title} by {article.author}")

# Rebuild index (after bulk operations)
count = await search_db.rebuild_search_index()
print(f"Indexed {count} articles")

# Get index statistics
stats = await search_db.search_stats()
print(stats)

await search_db.close()
```

## 8. Existence Checks

```python
from dataclasses import dataclass
from picodb import AsyncPicodb

@dataclass
class User:
    username: str
    email: str

db = AsyncPicodb(User, path="sqlite+aiosqlite:///users.db")
await db.init_db()

# Check if any user matches a condition
exists = await db.exists(pre_filter=db.query().eq("username", "admin"))
print(f"Admin exists: {exists}")

# Check multiple values at once
results = await db.exists_many(
    values=["alice@example.com", "bob@example.com"],
    field="email",
    return_existing=True,
    return_missing=True,
)
existing, missing = results
print(f"Existing: {existing}")
print(f"Missing: {missing}")

await db.close()
```

## 9. Distinct Values and Aggregations

```python
from dataclasses import dataclass
from picodb import AsyncPicodb

@dataclass
class Movie:
    title: str
    year: int
    genre: str
    rating: float

db = AsyncPicodb(Movie, path="sqlite+aiosqlite:///movies.db")
await db.init_db()

# Get all distinct genres
genres = await db.distinct_values("genre")
print(genres)  # ["Sci-Fi", "Action", "Drama", ...]

# Count movies per genre
counts = await db.value_counts("genre", order_by_count=True)
print(counts)  # {"Sci-Fi": 15, "Action": 10, "Drama": 8, ...}

# Count with a filter
counts = await db.value_counts(
    "genre",
    pre_filter=db.query().gte("year", 2010),
    order_by_count=True,
    limit=5,
)
print(counts)  # Top 5 genres from 2010+

await db.close()
```

## 10. Streaming Large Datasets

```python
from dataclasses import dataclass
from picodb import AsyncPicodb

@dataclass
class LogEntry:
    timestamp: str
    level: str
    message: str

db = AsyncPicodb(LogEntry, path="sqlite+aiosqlite:///logs.db")
await db.init_db()

# Stream all entries in batches (memory-efficient)
async for batch in db.stream_all_batches(batch_size=100, order_by="timestamp"):
    for entry in batch:
        process(entry)

# Stream with a filter
async for entry in db.stream_all(
    order_by="timestamp",
    desc=True,
):
    print(f"{entry.timestamp} [{entry.level}] {entry.message}")

await db.close()
```

## 11. Custom Indexes

```python
from dataclasses import dataclass
from picodb import AsyncPicodb

@dataclass
class User:
    username: str
    email: str
    status: str

db = AsyncPicodb(
    User,
    path="sqlite+aiosqlite:///users.db",
    indexes=[
        {"fields": ["email"], "unique": True},
        {"fields": ["status", "created_at"]},
        {"fields": ["status"], "where": "status = 'active'"},
    ],
)
await db.init_db()

await db.close()
```

## 12. Custom PRAGMAs

```python
from picodb import AsyncPicodb

db = AsyncPicodb(
    Movie,
    path="sqlite+aiosqlite:///movies.db",
    pragma_options={
        "journal_mode": "WAL",
        "synchronous": "OFF",       # Faster but less safe
        "cache_size": -262144,      # 256MB cache
    },
)
await db.init_db()

await db.close()
```