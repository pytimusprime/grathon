# PicoDB — Async SQLite/PostgreSQL ORM with FTS & Search

PicoDB is an async Python ORM wrapper around SQLite (via SQLAlchemy + aiosqlite) and PostgreSQL (via asyncpg), optimized for large datasets. It provides dataclass-based schemas, automatic table generation, full-text search, a chainable query builder, a Redis-like cache layer, and an inverted-index search engine with BM25 ranking.

## Why PicoDB?

- **Dataclass schemas** — Define your data model once as a Python dataclass; tables are auto-generated.
- **Dual backend** — SQLite for lightweight/embedded use, PostgreSQL for production-scale workloads.
- **Full-Text Search** — FTS5 for SQLite, native `tsvector`/`tsquery` for PostgreSQL, with relevance ranking.
- **Chainable Query Builder** — `.query().eq().gt().search()` for composable, readable queries.
- **Redis-like Cache** — Key-value store with TTL, sets, and atomic increment/decrement on top of the same database.
- **BM25 Search Engine** — Inverted index with BM25 scoring for ranked full-text search.
- **Bulk Operations** — `insert_many`, `delete_many`, `stream_all_batches` for high-throughput workloads.
- **Async-first** — Built on `asyncio` and SQLAlchemy's async API from the ground up.

## Quick Start

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

# Get by record_id
movie = await db.get(rid)

# Search with FTS
results = await db.search(use_fts=True, fts_query="Sci-Fi", limit=10)

# Query builder
movies = await db.query().gte("rating", 8.0).order_by("-rating").limit(5).search()

# Close
await db.close()
```

## Project Structure

```
libs/picodb/
├── __init__.py            # Public exports and version
├── core.py                # AsyncPicodb — main SQLite ORM class
├── postgres.py            # AsyncPicodoPG — PostgreSQL variant
├── cache.py               # PicodoCache — Redis-like cache layer
├── search.py              # PicodoSearch — BM25 inverted index search
├── query.py               # Q — Chainable query builder
├── fts.py                 # FtsMixin — SQLite FTS5 support
├── postgres_fts.py        # FtsMixinPG — PostgreSQL tsvector FTS support
├── formatter.py           # data_formatter — value serialization utility
└── .ai-context/           # AI-facing documentation (this directory)
    ├── README.md
    ├── API.md
    ├── ARCHITECTURE.md
    ├── EXAMPLES.md
    ├── FAQ.md
    └── RULES.md
```

## Key Concepts

| Concept | Description |
|---|---|
| `AsyncPicodb` | Main SQLite ORM class with CRUD, FTS, query builder, and search |
| `AsyncPicodoPG` | PostgreSQL variant with native tsvector FTS and connection pooling |
| `PicodoCache` | Redis-like cache (key-value + sets + TTL) built on AsyncPicodb |
| `PicodoSearch` | Inverted index + BM25 search engine built on AsyncPicodb |
| `Q` | Chainable query builder for filtering, ordering, pagination |
| `FtsMixin` | SQLite FTS5 mixin — auto-populates FTS index on insert/update |
| `FtsMixinPG` | PostgreSQL FTS mixin — uses triggers for auto-population |
| `record_id` | Auto-generated MD5 hash of the serialized record, used as primary key |
| `data_formatter` | Serializes Python values (dates, lists, dicts) to DB-friendly formats |

## Installation

```bash
pip install picodb
```

Or add to your project via `pyproject.toml`:

```toml
dependencies = [
    "picodb @ file:///path/to/libs/picodb",
]
```

## Version

Current version: **4.1**