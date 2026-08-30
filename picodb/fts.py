"""
Full-Text Search (FTS) support for PicoDB.

Provides FTS5 indexing and searching capabilities for efficient text search.
"""

from typing import List, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class FtsMixin:
	"""Mixin providing FTS5 full-text search functionality."""

	async def _insert_into_fts(self, session: AsyncSession, record_id: str, data_dict: dict):
		"""Insert record into FTS index."""
		if not self._fts_enabled or not self._fts_fields or not self._fts_populate:
			return
		fts_name = f"{self._table_name}_fts"
		cols = ["record_id"] + self._fts_fields
		values = [record_id] + [data_dict.get(f, "") for f in self._fts_fields]
		placeholders = ", ".join(f":v{i}" for i in range(len(values)))
		params = {f"v{i}": v for i, v in enumerate(values)}
		await session.execute(
			text(f"INSERT INTO {fts_name} ({', '.join(cols)}) VALUES ({placeholders});"),
			params
		)

	async def _delete_from_fts(self, session: AsyncSession, record_id: str):
		"""Delete record from FTS index."""
		if not self._fts_enabled or not self._fts_fields:
			return
		fts_name = f"{self._table_name}_fts"
		await session.execute(
			text(f"DELETE FROM {fts_name} WHERE record_id = :rid;"),
			{"rid": record_id}
		)

	def enable_fts_populate(self, flag: bool):
		"""Enable or disable FTS population on inserts."""
		self._fts_populate = bool(flag)

	async def rebuild_fts(self, batch_size: int = 20000):
		"""Rebuild FTS index from all records."""
		if not self._fts_enabled or not self._fts_fields:
			return
		fts_name = f"{self._table_name}_fts"
		async with self._write_lock:
			async with self.engine.begin() as conn:
				await conn.execute(text(f"DROP TABLE IF EXISTS {fts_name};"))
				await conn.execute(text(
					f"CREATE VIRTUAL TABLE {fts_name} USING fts5({', '.join(['record_id'] + self._fts_fields)}, tokenize='unicode61');"
				))
		offset = 0
		async with self.session_factory() as session:
			while True:
				stmt = self._model.__class__.select(self._model).limit(batch_size).offset(offset)
				from sqlalchemy import select
				stmt = select(self._model).limit(batch_size).offset(offset)
				res = await session.execute(stmt)
				rows = res.scalars().all()
				if not rows:
					break
				for r in rows:
					data = {k: v for k, v in r.__dict__.items() if not k.startswith("_")}
					await self._insert_into_fts(session, data["record_id"], data)
				await session.commit()
				offset += len(rows)

	async def search_fts(self, query: str, limit: int = 100, offset: int = 0) -> List[str]:
		"""Search using FTS with limit and offset."""
		if not self._fts_enabled:
			return []

		fts_name = f"{self._table_name}_fts"
		async with self.session_factory() as session:
			sql_query = text(
				f"SELECT record_id FROM {fts_name} "
				f"WHERE {fts_name} MATCH :q "
				f"LIMIT :lim OFFSET :off;"
			)
			res = await session.execute(
				sql_query,
				{"q": query, "lim": limit, "off": offset}
			)
			return [r[0] for r in res.fetchall()]

	async def load_imdb_dataset(self, items: list, chunk_size: int = 5000):
		"""Bulk load items with optimized FTS population."""
		old = self._fts_populate
		self.enable_fts_populate(False)
		try:
			await self.insert_many(items, chunk_size)
			await self.rebuild_fts()
		finally:
			self.enable_fts_populate(old)
