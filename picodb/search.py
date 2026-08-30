"""
PicodoSearch — Search engine with Inverted Index + BM25 ranking.

Provides full-text search on top of AsyncPicodb (SQLite) and AsyncPicodoPG (PostgreSQL).
Uses inverted index (_search_index table) for fast lookups and BM25 for relevance scoring.
"""

import asyncio
import logging
import math
import re
from dataclasses import asdict, is_dataclass
from typing import Any, Dict, List, Optional, Set, Tuple, Type, TypeVar

from sqlalchemy import and_, delete, func, insert, select, text

from .core import AsyncPicodb
from .postgres import AsyncPicodoPG

logger = logging.getLogger("picodb.search")

SchemaT = TypeVar("SchemaT")

# Common English stopwords
STOPWORDS = {
	"a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from", "has",
	"he", "in", "is", "it", "of", "on", "or", "that", "the", "to", "was", "will", "with"
}


class SearchIndexMixin:
	"""Mixin providing search indexing (Inverted Index + BM25 scoring)."""

	_search_fields: List[str]
	_field_boosts: Dict[str, float]
	_table_name: str
	session_factory: Any
	_write_lock: asyncio.Lock

	def _tokenize(self, text: str) -> List[Tuple[str, int]]:
		"""
		Tokenize text: lowercase, split, remove stopwords, count frequency.

		Returns list of (term, frequency) tuples.
		"""
		if not text:
			return []

		# Lowercase, remove punctuation, split
		text = text.lower()
		tokens = re.findall(r"\b\w+\b", text)

		# Remove stopwords and short tokens
		tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]

		# Count frequency
		freq_map: Dict[str, int] = {}
		for token in tokens:
			freq_map[token] = freq_map.get(token, 0) + 1

		return sorted(freq_map.items(), key=lambda x: -x[1])

	async def _index_record(
		self, session, record_id: str, data_dict: Dict[str, Any]
	) -> None:
		"""
		Index a record: tokenize search_fields, insert into _search_index.

		Called inside an open session (before commit) for atomicity.
		"""
		for field in self._search_fields:
			if field not in data_dict:
				continue

			value = data_dict[field]
			if value is None:
				continue

			field_text = str(value)
			tokens = self._tokenize(field_text)

			for term, frequency in tokens:
				stmt = text(
					"INSERT OR IGNORE INTO _search_index (term, record_id, field_name, frequency) "
					"VALUES (:term, :record_id, :field_name, :frequency)"
				)
				await session.execute(
					stmt,
					{
						"term": term,
						"record_id": record_id,
						"field_name": field,
						"frequency": frequency,
					},
				)

				# Update stats
				stats_stmt = text(
					"INSERT INTO _search_stats (term, doc_count) VALUES (:term, 1) "
					"ON CONFLICT(term) DO UPDATE SET doc_count = doc_count + 1"
				)
				await session.execute(stats_stmt, {"term": term})

	async def _deindex_record(self, session, record_id: str) -> None:
		"""
		Remove record from index: delete from _search_index, update _search_stats.

		Called inside an open session (before commit) for atomicity.
		"""
		# Get all terms for this record
		stmt = text("SELECT DISTINCT term FROM _search_index WHERE record_id = :record_id")
		result = await session.execute(stmt, {"record_id": record_id})
		terms = [row[0] for row in result.fetchall() if row[0] is not None]

		# Delete from index
		del_stmt = text("DELETE FROM _search_index WHERE record_id = :record_id")
		await session.execute(del_stmt, {"record_id": record_id})

		# Update stats (decrement doc_count)
		for term in terms:
			stats_stmt = text(
				"UPDATE _search_stats SET doc_count = doc_count - 1 "
				"WHERE term = :term AND doc_count > 0"
			)
			await session.execute(stats_stmt, {"term": term})

	async def _bm25_score(
		self,
		term: str,
		term_freq: int,
		field_name: str,
		doc_freq: int,
		total_docs: int,
		doc_len: int,
		avg_doc_len: float,
	) -> float:
		"""
		Calculate BM25 score for a single term in a document.

		k1=1.5 (term saturation), b=0.75 (field length normalization)
		"""
		k1, b = 1.5, 0.75
		field_boost = self._field_boosts.get(field_name, 1.0)

		# IDF: log((N - df + 0.5) / (df + 0.5))
		idf = math.log((total_docs - doc_freq + 0.5) / (doc_freq + 0.5))

		# TF normalization with field length
		tf_norm = (term_freq * (k1 + 1)) / (
			term_freq + k1 * (1 - b + b * doc_len / max(avg_doc_len, 1))
		)

		return idf * tf_norm * field_boost

	async def search_index(
		self,
		query: str,
		limit: int = 10,
		offset: int = 0,
		ranking: str = "bm25",
	) -> List[Tuple[SchemaT, float]]:
		"""
		Search using inverted index + BM25 scoring.

		Args:
			query: Search query (space-separated terms)
			limit: Max results
			offset: Pagination offset
			ranking: "bm25" (default) or "none"

		Returns:
			List of (record, relevance_score) tuples, sorted by score descending
		"""
		query_tokens = self._tokenize(query)
		if not query_tokens:
			return []

		terms = [term for term, _ in query_tokens]

		# Get all record_ids that match any term
		async with self.session_factory() as session:
			# Use SQL IN clause with parameter binding
			placeholders = ",".join([f":term{i}" for i in range(len(terms))])
			params_dict = {f"term{i}": term for i, term in enumerate(terms)}

			stmt = text(
				f"SELECT DISTINCT record_id FROM _search_index WHERE term IN ({placeholders})"
			)
			result = await session.execute(stmt, params_dict)
			candidate_ids = [row[0] for row in result.fetchall()]

			if not candidate_ids:
				return []

			# Get stats for scoring
			stats_stmt = text(
				f"SELECT term, doc_count FROM _search_stats WHERE term IN ({placeholders})"
			)
			stats_result = await session.execute(stats_stmt, params_dict)
			term_stats = {row[0]: row[1] for row in stats_result.fetchall()}

			total_docs_stmt = text(
				f"SELECT COUNT(DISTINCT record_id) FROM {self._table_name}"
			)
			total_docs = await session.execute(total_docs_stmt)
			total_docs = total_docs.scalar_one() or 1

			# Get avg document length (in terms)
			avg_len_stmt = text(
				f"""
				SELECT AVG(term_count) FROM (
					SELECT record_id, COUNT(*) as term_count FROM _search_index
					GROUP BY record_id
				)
				"""
			)
			avg_len_result = await session.execute(avg_len_stmt)
			avg_doc_len = avg_len_result.scalar_one() or 1.0

		# Score each candidate
		scores: Dict[str, float] = {}

		async with self.session_factory() as session:
			for record_id in candidate_ids:
				score = 0.0

				# Get all term occurrences for this record
				placeholders = ",".join([f":term{i}" for i in range(len(terms))])
				freq_params = {"record_id": record_id}
				freq_params.update({f"term{i}": term for i, term in enumerate(terms)})

				freq_stmt = text(
					f"SELECT term, field_name, frequency FROM _search_index "
					f"WHERE record_id = :record_id AND term IN ({placeholders})"
				)
				freq_result = await session.execute(freq_stmt, freq_params)
				freq_rows = freq_result.fetchall()

				# Get document length
				doc_len_stmt = text(
					"SELECT COUNT(*) FROM _search_index WHERE record_id = :record_id"
				)
				doc_len = await session.execute(doc_len_stmt, {"record_id": record_id})
				doc_len = doc_len.scalar_one() or 1

				# Sum BM25 scores for all matching terms
				for term, field_name, term_freq in freq_rows:
					doc_freq = term_stats.get(term, 0)
					if doc_freq > 0 and ranking == "bm25":
						bm25 = await self._bm25_score(
							term,
							term_freq,
							field_name,
							doc_freq,
							total_docs,
							doc_len,
							avg_doc_len,
						)
						score += bm25

				if score > 0:
					scores[record_id] = score

		# Sort by score
		sorted_ids = sorted(scores.items(), key=lambda x: -x[1])
		sorted_ids = sorted_ids[offset : offset + limit]

		# Fetch records
		results = []
		for record_id, score in sorted_ids:
			# Call parent's get(record_id) method, not cache's get_cache
			record = await super(SearchIndexMixin, self).get(record_id)  # type: ignore
			if record:
				results.append((record, score))

		return results

	async def rebuild_search_index(self) -> int:
		"""Rebuild entire search index from scratch."""
		async with self._write_lock:
			async with self.session_factory() as session:
				await session.execute(text("DELETE FROM _search_index"))
				await session.execute(text("DELETE FROM _search_stats"))
				await session.commit()

		count = 0
		# Call parent's stream_all() method
		async for record in super(SearchIndexMixin, self).stream_all():  # type: ignore
			if is_dataclass(record):
				data_dict = asdict(record)
				async with self._write_lock:
					async with self.session_factory() as session:
						await self._index_record(session, record.record_id, data_dict)
						await session.commit()
						count += 1

		return count

	async def search_stats(self) -> Dict[str, Any]:
		"""Get search index statistics."""
		async with self.session_factory() as session:
			indexed_stmt = text(
				"SELECT COUNT(DISTINCT record_id) FROM _search_index"
			)
			indexed = await session.execute(indexed_stmt)
			indexed_count = indexed.scalar_one() or 0

			total_stmt = text(f"SELECT COUNT(*) FROM {self._table_name}")
			total = await session.execute(total_stmt)
			total_count = total.scalar_one() or 0

			terms_stmt = text("SELECT COUNT(*) FROM _search_stats")
			terms = await session.execute(terms_stmt)
			terms_count = terms.scalar_one() or 0

			return {
				"indexed_records": indexed_count,
				"total_records": total_count,
				"total_terms": terms_count,
				"search_fields": self._search_fields,
			}


class PicodoSearch(AsyncPicodb[SchemaT], SearchIndexMixin):
	"""
	PicodoSearch — SQLite search engine with inverted index + BM25 ranking.

	Extends AsyncPicodb with full-text search capabilities.
	"""

	def __init__(
		self,
		schema_cls: Type[SchemaT],
		path: str = "sqlite+aiosqlite:///search.db",
		*,
		search_fields: List[str],
		field_boosts: Optional[Dict[str, float]] = None,
		**kwargs
	):
		if not search_fields:
			raise ValueError("search_fields must be non-empty")

		super().__init__(schema_cls, path, **kwargs)
		self._search_fields = search_fields
		self._field_boosts = field_boosts or {f: 1.0 for f in search_fields}

	async def init_db(self):
		"""Initialize database with search index tables."""
		await super().init_db()

		async with self.engine.begin() as conn:
			await conn.execute(
				text("""
				CREATE TABLE IF NOT EXISTS _search_index (
					term TEXT NOT NULL,
					record_id TEXT NOT NULL,
					field_name TEXT NOT NULL,
					frequency INTEGER DEFAULT 1,
					PRIMARY KEY (term, record_id, field_name)
				)
			""")
			)

			await conn.execute(
				text("""
				CREATE TABLE IF NOT EXISTS _search_stats (
					term TEXT PRIMARY KEY,
					doc_count INTEGER DEFAULT 0
				)
			""")
			)

			await conn.commit()

		logger.debug("Search index tables initialized")

	async def clear_db(self):
		"""Clear all data including search index."""
		await super().clear_db()
		async with self.engine.begin() as conn:
			await conn.execute(text("DELETE FROM _search_index"))
			await conn.execute(text("DELETE FROM _search_stats"))
			await conn.commit()

	async def _insert_into_fts(self, session, record_id: str, data_dict: Dict[str, Any]):
		"""Hook: index record atomically with main insert (before commit)."""
		await super()._insert_into_fts(session, record_id, data_dict)
		await self._index_record(session, record_id, data_dict)

	async def _delete_from_fts(self, session, record_id: str):
		"""Hook: deindex record atomically with main delete (before commit)."""
		await super()._delete_from_fts(session, record_id)
		await self._deindex_record(session, record_id)

	async def delete_many(self, record_ids: List[str], batch_size: int = 1000) -> int:
		"""Delete multiple records, also cleaning search index."""
		async with self._write_lock:
			async with self.session_factory() as session:
				deleted = 0
				for i in range(0, len(record_ids), batch_size):
					batch = record_ids[i : i + batch_size]

					for record_id in batch:
						await self._deindex_record(session, record_id)

					if self._model is not None:
						stmt = delete(self._model).where(
							self._model.record_id.in_(batch)
						)
						res = await session.execute(stmt)
						deleted += int(res.rowcount or 0)

				await session.commit()
				return deleted


class PicodoSearchPG(AsyncPicodoPG[SchemaT], SearchIndexMixin):
	"""
	PicodoSearchPG — PostgreSQL search engine with inverted index + BM25 ranking.

	Extends AsyncPicodoPG with full-text search capabilities.
	Non-atomic index update (acceptable for search indices).
	"""

	def __init__(
		self,
		schema_cls: Type[SchemaT],
		path: str = "postgresql+asyncpg://user:password@localhost/searchdb",
		*,
		search_fields: List[str],
		field_boosts: Optional[Dict[str, float]] = None,
		**kwargs
	):
		if not search_fields:
			raise ValueError("search_fields must be non-empty")

		super().__init__(schema_cls, path, **kwargs)
		self._search_fields = search_fields
		self._field_boosts = field_boosts or {f: 1.0 for f in search_fields}

	async def init_db(self):
		"""Initialize database with search index tables."""
		await super().init_db()

		async with self.engine.begin() as conn:
			await conn.execute(
				text("""
				CREATE TABLE IF NOT EXISTS _search_index (
					term TEXT NOT NULL,
					record_id TEXT NOT NULL,
					field_name TEXT NOT NULL,
					frequency INTEGER DEFAULT 1,
					PRIMARY KEY (term, record_id, field_name)
				)
			""")
			)

			await conn.execute(
				text("""
				CREATE TABLE IF NOT EXISTS _search_stats (
					term TEXT PRIMARY KEY,
					doc_count INTEGER DEFAULT 0
				)
			""")
			)

			await conn.commit()

		logger.debug("Search index tables initialized (PostgreSQL)")

	async def insert(self, obj: SchemaT) -> str:
		"""Insert record and index it (non-atomic)."""
		if not is_dataclass(obj):
			raise TypeError("Only dataclass instances can be inserted")

		record_id = await super().insert(obj)

		# Second transaction for index (acceptable non-atomicity)
		data_dict = asdict(obj)
		async with self._write_lock:
			async with self.session_factory() as session:
				await self._index_record(session, record_id, data_dict)
				await session.commit()

		return record_id

	async def delete(self, record_id: str):
		"""Delete record and deindex it (non-atomic)."""
		await super().delete(record_id)

		async with self._write_lock:
			async with self.session_factory() as session:
				await self._deindex_record(session, record_id)
				await session.commit()

	async def delete_many(self, record_ids: List[str], batch_size: int = 1000) -> int:
		"""Delete multiple records, also cleaning search index."""
		async with self._write_lock:
			async with self.session_factory() as session:
				deleted = 0
				for i in range(0, len(record_ids), batch_size):
					batch = record_ids[i : i + batch_size]

					for record_id in batch:
						await self._deindex_record(session, record_id)

					if self._model is not None:
						stmt = delete(self._model).where(
							self._model.record_id.in_(batch)
						)
						res = await session.execute(stmt)
						deleted += int(res.rowcount or 0)

				await session.commit()
				return deleted
