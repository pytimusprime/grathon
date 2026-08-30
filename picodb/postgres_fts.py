"""
Full-Text Search (FTS) support for PostgreSQL.

Provides native PostgreSQL tsvector/tsquery FTS with ranking and advanced features.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import text, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
	from .postgres import AsyncPicodoPG


class FtsMixinPG:
	"""Mixin providing PostgreSQL full-text search functionality via tsvector."""

	async def search_fts(
			self,
			query: str,
			limit: int = 100,
			offset: int = 0,
			ranking: bool = True,
	) -> List[str]:
		"""
		Search using PostgreSQL FTS with optional ranking.

		Args:
			query: Search query (plain text, converted to tsquery)
			limit: Maximum results
			offset: Result offset
			ranking: Use ts_rank for relevance ranking

		Returns:
			List of record_ids sorted by relevance (if ranking=True)
		"""
		if not self._fts_enabled or not hasattr(self._model, "fts_vector"):
			return []

		async with self.session_factory() as session:
			tsquery = func.plainto_tsquery("simple", query)

			if ranking:
				rank_expr = func.ts_rank(self._model.fts_vector, tsquery).label("rank")
				sql_query = text(f"""
					SELECT record_id FROM {self._table_name}
					WHERE fts_vector @@ plainto_tsquery('simple', :q)
					ORDER BY ts_rank(fts_vector, plainto_tsquery('simple', :q)) DESC
					LIMIT :lim OFFSET :off;
				""")
			else:
				sql_query = text(f"""
					SELECT record_id FROM {self._table_name}
					WHERE fts_vector @@ plainto_tsquery('simple', :q)
					LIMIT :lim OFFSET :off;
				""")

			try:
				res = await session.execute(
					sql_query,
					{"q": query, "lim": limit, "off": offset}
				)
				return [r[0] for r in res.fetchall()]
			except Exception as e:
				import logging
				logger = logging.getLogger("picodb.postgres_fts")
				logger.warning(f"FTS search failed: {e}")
				return []

	async def search_fts_advanced(
			self,
			query: str,
			limit: int = 100,
			offset: int = 0,
	) -> List[str]:
		"""
		Advanced FTS search with boolean operators (& | ! <->).

		Syntax:
			- word1 & word2: both words
			- word1 | word2: either word
			- !word: exclude word
			- word1 <-> word2: adjacent words

		Args:
			query: tsquery format search (e.g., "database & search")
			limit: Maximum results
			offset: Result offset

		Returns:
			List of record_ids sorted by relevance
		"""
		if not self._fts_enabled or not hasattr(self._model, "fts_vector"):
			return []

		async with self.session_factory() as session:
			sql_query = text(f"""
				SELECT record_id FROM {self._table_name}
				WHERE fts_vector @@ to_tsquery('simple', :q)
				ORDER BY ts_rank(fts_vector, to_tsquery('simple', :q)) DESC
				LIMIT :lim OFFSET :off;
			""")

			try:
				res = await session.execute(
					sql_query,
					{"q": query, "lim": limit, "off": offset}
				)
				return [r[0] for r in res.fetchall()]
			except Exception as e:
				import logging
				logger = logging.getLogger("picodb.postgres_fts")
				logger.warning(f"Advanced FTS search failed: {e}")
				return []

	async def rebuild_fts(self, batch_size: int = 20000):
		"""
		Rebuild FTS index by re-populating fts_vector for all records.

		The trigger function will auto-populate on each update, so this is mainly
		for fixing corrupted indexes or after bulk operations.
		"""
		if not self._fts_enabled or not self._fts_fields:
			return

		async with self._write_lock:
			async with self.engine.begin() as conn:
				tsvector_cols = " || ' ' || ".join([f"COALESCE({f}, '')" for f in self._fts_fields])
				update_sql = f"""
				UPDATE {self._table_name}
				SET fts_vector = to_tsvector('simple', {tsvector_cols});
				"""
				try:
					await conn.execute(text(update_sql))
					await conn.commit()
				except Exception as e:
					import logging
					logger = logging.getLogger("picodb.postgres_fts")
					logger.warning(f"FTS rebuild failed: {e}")

	def enable_fts_populate(self, flag: bool):
		"""
		Enable or disable FTS population.

		Note: For PostgreSQL, FTS is auto-populated via trigger, so this is mainly
		for API compatibility with SQLite version.
		"""
		self._fts_populate = bool(flag)

	async def fts_stats(self) -> dict:
		"""Get FTS statistics."""
		if not self._fts_enabled or not hasattr(self._model, "fts_vector"):
			return {}

		async with self.session_factory() as session:
			try:
				# Count records with non-null fts_vector
				count_sql = text(f"SELECT COUNT(*) FROM {self._table_name} WHERE fts_vector IS NOT NULL;")
				res = await session.execute(count_sql)
				indexed_count = res.scalar_one() or 0

				# Get total records
				total_sql = text(f"SELECT COUNT(*) FROM {self._table_name};")
				res = await session.execute(total_sql)
				total_count = res.scalar_one() or 0

				return {
					"indexed_records": indexed_count,
					"total_records": total_count,
					"fts_enabled": True,
					"fts_fields": self._fts_fields,
				}
			except Exception as e:
				import logging
				logger = logging.getLogger("picodb.postgres_fts")
				logger.warning(f"FTS stats failed: {e}")
				return {"error": str(e)}
