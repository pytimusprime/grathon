"""
Core PicoDB functionality.

AsyncPicodb - async SQLite wrapper with dataclass schemas and FTS support.
"""

import asyncio
import hashlib
import logging
import uuid
from dataclasses import asdict, fields, is_dataclass
from functools import lru_cache
from typing import (
	Any, AsyncIterator, Callable, Dict, Generic, List, Optional, Type, TypeVar, Union, get_args, get_origin, get_type_hints
)

import orjson
from sqlalchemy import JSON, BigInteger, String, Index, and_, func, select, text, Boolean, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("picodb")

from .formatter import data_formatter
from .query import Q
from .fts import FtsMixin

SchemaT = TypeVar("SchemaT")


class Base(DeclarativeBase):
	pass


def _resolve_type(t: Any) -> tuple:
	"""Unwrap Optional/Union types. Returns (base_type, is_optional)."""
	origin = get_origin(t)
	if origin is Union:
		args = [a for a in get_args(t) if a is not type(None)]
		return (args[0] if args else str), True
	return t, False


class AsyncPicodb(Generic[SchemaT], FtsMixin):
	"""
	AsyncPicodb v4.1 — SQLite wrapper optimized for large datasets.
	"""

	def __init__(
			self,
			schema_cls: Type[SchemaT],
			path: str = "sqlite+aiosqlite:///imdb.db",
			*,
			indexes: Optional[List[Dict[str, Any]]] = None,
			enable_fts: bool = True,
			fts_fields: Optional[List[str]] = None,
			fts_populate: bool = True,
			page_size: int = 1000,
			pragma_options: Optional[Dict[str, Any]] = None,
	):
		if not is_dataclass(schema_cls):
			raise TypeError("schema_cls must be a dataclass type")

		self.schema_cls = schema_cls
		self.db_path = path
		is_postgresql = path.startswith("postgresql") or path.startswith("postgresql+asyncpg")
		connect_args = {} if is_postgresql else {"check_same_thread": False}
		self._json_column_type = JSONB if is_postgresql else JSON
		self.engine = create_async_engine(
			path,
			echo=False,
			connect_args=connect_args,
			pool_pre_ping=True,
			execution_options={"isolation_level": "AUTOCOMMIT"},
		)
		self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)
		self._write_lock = asyncio.Lock()
		self._model = None
		self._table_name = schema_cls.__name__.lower()
		self._extra_index_sql: List[str] = []
		self._fts_enabled = bool(enable_fts)
		self._fts_fields = list(fts_fields) if fts_fields else []
		self._fts_populate = bool(fts_populate)
		self._page_size = max(100, int(page_size))
		self._type_hints = get_type_hints(schema_cls)
		self._indexes_param = indexes or []

		self._pragma_options = {
			"journal_mode": "WAL",
			"synchronous": "NORMAL",
			"temp_store": "MEMORY",
			"mmap_size": 268435456,
			"cache_size": -131072,
			"read_uncommitted": True,
		}
		if pragma_options:
			self._pragma_options.update(pragma_options)

		self._create_model()

	def _create_model(self):
		attrs = {"__tablename__": self._table_name}
		for f in fields(self.schema_cls):
			raw_t = self._type_hints.get(f.name, str)
			base_t, is_optional = _resolve_type(raw_t)

			if f.name == "record_id":
				attrs[f.name] = mapped_column(String, primary_key=True, nullable=False)
			elif base_t is bool:
				attrs[f.name] = mapped_column(Boolean, nullable=is_optional)
			elif base_t is int:
				attrs[f.name] = mapped_column(BigInteger, nullable=is_optional)
			elif base_t is float:
				attrs[f.name] = mapped_column(Float, nullable=is_optional)
			elif get_origin(base_t) in (list, dict, List, Dict) or base_t in (list, dict) or is_dataclass(base_t):
				attrs[f.name] = mapped_column(self._json_column_type, nullable=True)
			else:
				attrs[f.name] = mapped_column(String, nullable=is_optional)

		sqlalchemy_indexes = []
		for idx in self._indexes_param:
			if "fields" in idx and "expr" not in idx and "where" not in idx:
				name = idx.get("name") or f"idx_{self._table_name}_{'_'.join(idx['fields'])}"
				cols = tuple(idx["fields"])
				unique = idx.get("unique", False)
				sqlalchemy_indexes.append(Index(name, *cols, unique=unique))
			else:
				name = idx.get("name") or f"idx_{self._table_name}_{uuid.uuid4().hex[:8]}"
				if "expr" in idx:
					sql = f"CREATE INDEX IF NOT EXISTS {name} ON {self._table_name} ({idx['expr']});"
					self._extra_index_sql.append(sql)
				elif "fields" in idx and "where" in idx:
					cols = ", ".join(idx["fields"])
					sql = f"CREATE INDEX IF NOT EXISTS {name} ON {self._table_name} ({cols}) WHERE {idx['where']};"
					self._extra_index_sql.append(sql)

		if sqlalchemy_indexes:
			attrs["__table_args__"] = tuple(sqlalchemy_indexes)

		self._model = type(f"{self.schema_cls.__name__}Model", (Base,), attrs)

	async def init_db(self):
		async with self.engine.begin() as conn:
			await conn.run_sync(Base.metadata.create_all)
			for key, val in self._pragma_options.items():
				await conn.execute(text(f"PRAGMA {key}={val};"))
			for sql in self._extra_index_sql:
				await conn.execute(text(sql))

			if self._fts_enabled and self._fts_fields:
				fts_name = f"{self._table_name}_fts"
				cols_sql = ", ".join(["record_id"] + self._fts_fields)
				await conn.execute(text(
					f"CREATE VIRTUAL TABLE IF NOT EXISTS {fts_name} USING fts5({cols_sql}, tokenize='unicode61');"
				))
			await conn.commit()

	async def clear_db(self):
		async with self._write_lock:
			async with self.engine.begin() as conn:
				await conn.run_sync(Base.metadata.drop_all)
				await conn.run_sync(Base.metadata.create_all)
				if self._fts_enabled and self._fts_fields:
					fts_name = f"{self._table_name}_fts"
					await conn.execute(text(f"DROP TABLE IF EXISTS {fts_name};"))
					cols_sql = ", ".join(["record_id"] + self._fts_fields)
					await conn.execute(text(
						f"CREATE VIRTUAL TABLE IF NOT EXISTS {fts_name} USING fts5({cols_sql}, tokenize='unicode61');"
					))
				await conn.commit()

	def _compute_record_id(self, data_dict: Dict[str, Any]) -> str:
		safe_dict = {k: data_formatter(v) for k, v in data_dict.items()}
		return hashlib.md5(
			orjson.dumps(safe_dict, option=orjson.OPT_SORT_KEYS)
		).hexdigest()

	async def insert(self, obj: SchemaT) -> str:
		if not is_dataclass(obj):
			raise TypeError("Only dataclass instances can be inserted")

		data_dict = asdict(obj)
		for k, v in data_dict.items():
			if v is not None:
				data_dict[k] = data_formatter(v)

		record_id = obj.record_id if getattr(obj, "record_id", None) else self._compute_record_id(data_dict)
		data_dict["record_id"] = record_id

		async with self._write_lock:
			async with self.session_factory() as session:
				for attempt in range(3):
					try:
						session.add(self._model(**data_dict))
						if self._fts_enabled and self._fts_fields and self._fts_populate:
							await self._insert_into_fts(session, record_id, data_dict)
						await session.commit()
						if hasattr(obj, "record_id"):
							obj.record_id = record_id
						logger.debug(f"Inserted record_id={record_id}")
						return record_id
					except IntegrityError:
						await session.rollback()
						logger.warning(f"Hash collision on attempt {attempt+1}, retrying")
						record_id = f"{self._compute_record_id(data_dict)}_{uuid.uuid4().hex[:8]}"
						data_dict["record_id"] = record_id
						if hasattr(obj, "record_id"):
							obj.record_id = record_id
				logger.error("Insert failed after 3 retries")
				raise RuntimeError("Insert failed after retries")

	async def insert_many(self, objects: List[SchemaT], chunk_size: int = 10000, atomic: bool = False) -> List[str]:
		if not objects:
			return []
		if not all(is_dataclass(o) and isinstance(o, type(objects[0])) for o in objects):
			raise TypeError("All objects must be same dataclass type")

		dicts = []
		for obj in objects:
			d = asdict(obj)
			for k, v in d.items():
				if v is not None:
					d[k] = data_formatter(v)
			rid = obj.record_id if getattr(obj, "record_id", None) else self._compute_record_id(d)
			d["record_id"] = rid
			dicts.append(d)

		async with self._write_lock:
			async with self.session_factory() as session:
				try:
					chunk_count = 0
					for i in range(0, len(dicts), chunk_size):
						batch = dicts[i:i + chunk_size]
						session.add_all([self._model(**b) for b in batch])
						if self._fts_enabled and self._fts_fields and self._fts_populate:
							for b in batch:
								await self._insert_into_fts(session, b["record_id"], b)
						if not atomic:
							await session.commit()
						chunk_count += 1
					if atomic:
						await session.commit()
					logger.info(f"Inserted {len(dicts)} records in {chunk_count} chunks (atomic={atomic})")
					return [d["record_id"] for d in dicts]
				except Exception as e:
					await session.rollback()
					logger.error(f"insert_many failed after {chunk_count} chunks, rolled back {len(dicts)} records: {e}")
					raise

	async def get(self, record_id: str) -> Optional[SchemaT]:
		async with self.session_factory() as session:
			result = await session.execute(select(self._model).where(self._model.record_id == record_id))
			row = result.scalars().one_or_none()
			if not row:
				return None
			return next(self._batch_converter()([row]))

	@lru_cache(maxsize=32)
	def _batch_converter(self):
		json_fields = {
			f.name for f in fields(self.schema_cls)
			if (t := self._type_hints.get(f.name)) and (
					get_origin(t) in (list, dict, List, Dict) or t in (list, dict) or is_dataclass(t)
			)
		}

		bool_fields = {
			f.name for f in fields(self.schema_cls)
			if (base_t := _resolve_type(self._type_hints.get(f.name))[0]) is bool
		}

		def convert(rows):
			for row in rows:
				data = {}
				for k, v in row.__dict__.items():
					if k.startswith("_"):
						continue
					if k in json_fields and v is not None:
						if isinstance(v, str):
							try:
								data[k] = orjson.loads(v)
							except orjson.JSONDecodeError:
								data[k] = v
						else:
							data[k] = v
					elif k in bool_fields and v is not None:
						data[k] = bool(v)
					else:
						data[k] = v
				yield self.schema_cls(**data)

		return convert

	async def stream_all(self, limit: Optional[int] = None,
					   order_by: Optional[str] = None,
					   desc: bool = False) -> AsyncIterator[SchemaT]:
		converter = self._batch_converter()
		offset = 0
		batch_size = 5000

		stmt_base = select(self._model)
		if order_by:
			col = getattr(self._model, order_by)
			stmt_base = stmt_base.order_by(col.desc() if desc else col)

		async with self.session_factory() as session:
			while True:
				if limit and offset >= limit:
					break
				stmt = stmt_base.limit(min(batch_size, limit - offset) if limit else batch_size).offset(offset)
				result = await session.execute(stmt)
				rows = result.scalars().all()
				if not rows:
					break
				for obj in converter(rows):
					yield obj
				offset += len(rows)

	async def stream_all_batches(
			self,
			batch_size: int = 100,
			limit: Optional[int] = None,
			order_by: Optional[str] = None,
			desc: bool = False,
			order_by_exprs: Optional[list] = None,
			pre_filter: Optional[Any] = None,
	) -> AsyncIterator[List[SchemaT]]:
		if batch_size <= 0:
			raise ValueError("batch_size must be > 0")

		converter = self._batch_converter()
		offset = 0
		internal_batch_size = 5000

		if pre_filter and hasattr(pre_filter, "build"):
			stmt_base = pre_filter.build()
		else:
			stmt_base = select(self._model)
			if pre_filter:
				stmt_base = stmt_base.where(pre_filter)

		if not hasattr(pre_filter, "build") or not pre_filter._order_by:
			if order_by_exprs:
				stmt_base = stmt_base.order_by(*order_by_exprs)
			elif order_by:
				col = getattr(self._model, order_by)
				stmt_base = stmt_base.order_by(col.desc() if desc else col.asc())

		async with self.session_factory() as session:
			while True:
				if limit is not None and offset >= limit:
					break

				remaining = (limit - offset) if limit is not None else None
				current_size = min(
					internal_batch_size,
					remaining if remaining is not None else internal_batch_size
				)
				if current_size <= 0:
					break

				stmt = stmt_base.limit(current_size).offset(offset)

				result = await session.execute(stmt)
				rows = result.scalars().all()
				if not rows:
					break

				items = list(converter(rows))
				offset += len(items)

				for i in range(0, len(items), batch_size):
					batch = items[i:i + batch_size]

					if limit is not None:
						allowed = limit - (offset - len(items) + i)
						if len(batch) > allowed:
							batch = batch[:allowed]

					if batch:
						yield batch

					if limit is not None and offset - len(items) + i + len(batch) >= limit:
						return

	async def count_records(self) -> int:
		async with self.session_factory() as session:
			res = await session.execute(select(func.count()).select_from(self._model))
			return res.scalar_one()

	async def update(self, record_id: str, new_obj: SchemaT):
		if not is_dataclass(new_obj):
			raise TypeError("Only dataclass instances can be updated")

		data_dict = asdict(new_obj)
		data_dict.pop("record_id", None)

		for k, v in data_dict.items():
			if v is not None:
				data_dict[k] = data_formatter(v)

		async with self._write_lock:
			async with self.session_factory() as session:
				result = await session.execute(select(self._model).where(self._model.record_id == record_id))
				db_obj = result.scalars().one_or_none()
				if not db_obj:
					raise ValueError("Record not found")

				for k, v in data_dict.items():
					setattr(db_obj, k, v)

				if self._fts_enabled and self._fts_fields:
					await self._delete_from_fts(session, record_id)
					if self._fts_populate:
						full_data = {k: getattr(db_obj, k) for k in self._type_hints.keys()}
						full_data["record_id"] = record_id
						await self._insert_into_fts(session, record_id, full_data)

				await session.commit()

	async def delete(self, record_id: str):
		async with self._write_lock:
			async with self.session_factory() as session:
				result = await session.execute(select(self._model).where(self._model.record_id == record_id))
				db_obj = result.scalars().one_or_none()
				if db_obj:
					await session.delete(db_obj)
					if self._fts_enabled and self._fts_fields:
						await self._delete_from_fts(session, record_id)
					await session.commit()

	async def delete_many(self, record_ids: List[str], batch_size: int = 1000) -> int:
		from sqlalchemy import delete
		deleted = 0
		async with self._write_lock:
			async with self.session_factory() as session:
				for i in range(0, len(record_ids), batch_size):
					batch = record_ids[i:i + batch_size]
					stmt = delete(self._model).where(self._model.record_id.in_(batch))
					res = await session.execute(stmt)
					if self._fts_enabled and self._fts_fields:
						for rid in batch:
							await self._delete_from_fts(session, rid)
					deleted += res.rowcount or 0
					await session.commit()
				return deleted

	def query(self):
		return Q(self._model, self)

	async def search(
			self,
			predicate: Optional[Callable] = None,
			pre_filter: Optional[Any] = None,
			use_fts: bool = False,
			fts_query: Optional[str] = None,
			limit: Optional[int] = None,
			offset: Optional[int] = 0,
	) -> List[SchemaT]:
		result = []
		async for obj in self._stream_search(predicate, pre_filter, use_fts, fts_query, limit, offset):
			result.append(obj)
		return result

	async def stream_search(
			self,
			predicate: Optional[Callable] = None,
			pre_filter: Optional[Any] = None,
			use_fts: bool = False,
			fts_query: Optional[str] = None,
			limit: Optional[int] = None,
			offset: Optional[int] = 0,
	) -> AsyncIterator[SchemaT]:
		async for obj in self._stream_search(predicate, pre_filter, use_fts, fts_query, limit, offset):
			yield obj

	async def _stream_search(self, predicate, pre_filter, use_fts, fts_query, limit, offset=0):
		import asyncio
		converter = self._batch_converter()
		record_ids = None
		if use_fts and self._fts_enabled and fts_query:
			async with self.session_factory() as session:
				fts_name = f"{self._table_name}_fts"
				res = await session.execute(
					text(f"SELECT record_id FROM {fts_name} WHERE {fts_name} MATCH :q LIMIT :lim;"),
					{"q": fts_query, "lim": limit or 10000}
				)
				record_ids = [r[0] for r in res.fetchall()]
				if not record_ids:
					return

		current_offset = offset or 0
		page_size = self._page_size
		async with self.session_factory() as session:
			while True:
				if limit and (current_offset - offset) >= limit:
					break

				current_limit = min(page_size, limit - (current_offset - offset)) if limit else page_size

				if record_ids:
					slice_ids = record_ids[current_offset:current_offset + current_limit]
					if not slice_ids:
						break
					stmt = select(self._model).where(self._model.record_id.in_(slice_ids))
				else:
					if pre_filter and hasattr(pre_filter, "build"):
						built = pre_filter.build()
						stmt = built.limit(current_limit).offset(current_offset)
					elif pre_filter:
						stmt = select(self._model).where(pre_filter).limit(current_limit).offset(current_offset)
					else:
						stmt = select(self._model).limit(current_limit).offset(current_offset)

				result = await session.execute(stmt)
				rows = result.scalars().all()
				if not rows:
					break

				for obj in converter(rows):
					if predicate:
						check = await predicate(obj, {}) if asyncio.iscoroutinefunction(predicate) else predicate(obj, {})
						if not check:
							continue
					yield obj

				current_offset += len(rows)

	async def exists(self, predicate=None, pre_filter=None) -> bool:
		async for _ in self._stream_search(predicate, pre_filter, False, None, 1):
			return True
		return False

	async def exists_many(
			self,
			values: List[Any],
			field: str,
			batch_size: int = 5000,
			return_existing: bool = False,
			return_missing: bool = False,
	):
		"""Check existence of multiple values in field."""
		if not values:
			if return_existing and return_missing:
				return [], []
			if return_existing:
				return []
			if return_missing:
				return []
			return {}

		if field not in self._type_hints and field != "record_id":
			raise ValueError(f"Field '{field}' not found in schema")

		results = {v: False for v in values}
		existing_values = set()

		values_list = list(values)

		async with self.session_factory() as session:
			for i in range(0, len(values_list), batch_size):
				batch = values_list[i:i + batch_size]

				stmt = select(getattr(self._model, field)).where(
					getattr(self._model, field).in_(batch)
				)
				res = await session.execute(stmt)
				existing_values.update(row[0] for row in res.fetchall())

		for v in values:
			results[v] = v in existing_values

		if return_existing and return_missing:
			existing = [v for v in values if results[v]]
			missing = [v for v in values if not results[v]]
			return existing, missing

		if return_existing:
			return [v for v in values if results[v]]

		if return_missing:
			return [v for v in values if not results[v]]

		return results

	async def distinct_values(
			self,
			field: str,
			pre_filter: Optional[Q] = None,
			order_by: Optional[str] = None,
	) -> List[Any]:
		"""Get distinct values for a field."""
		if field not in self._type_hints and field != "record_id":
			raise ValueError(f"Field '{field}' not found in schema")

		col = getattr(self._model, field)
		stmt = select(col).distinct()

		if pre_filter:
			if pre_filter._where:
				stmt = stmt.where(and_(*pre_filter._where))
			if pre_filter._order_by:
				stmt = stmt.order_by(*pre_filter._order_by)
			if pre_filter._limit:
				stmt = stmt.limit(pre_filter._limit)

		if order_by:
			from sqlalchemy import asc, desc
			desc_flag = order_by.startswith("-")
			field_name = order_by[1:] if desc_flag else order_by
			order_col = getattr(self._model, field_name)
			stmt = stmt.order_by(desc(order_col) if desc_flag else asc(order_col))

		async with self.session_factory() as session:
			result = await session.execute(stmt)
			return [row[0] for row in result.fetchall()]

	async def value_counts(
			self,
			field: str,
			pre_filter: Optional[Q] = None,
			order_by_count: bool = True,
			limit: Optional[int] = None,
	) -> Dict[Any, int]:
		"""Count occurrences of each unique value in field."""
		if field not in self._type_hints and field != "record_id":
			raise ValueError(f"Field '{field}' not found in schema")

		col = getattr(self._model, field)

		stmt = select(col, func.count().label("cnt")).group_by(col)

		if pre_filter:
			if pre_filter._where:
				stmt = stmt.where(and_(*pre_filter._where))
			if pre_filter._order_by:
				stmt = stmt.order_by(*pre_filter._order_by)

		if order_by_count:
			from sqlalchemy import desc
			stmt = stmt.order_by(desc("cnt"))

		if limit:
			stmt = stmt.limit(limit)

		async with self.session_factory() as session:
			result = await session.execute(stmt)
			rows = result.fetchall()
			return {row[0]: row[1] for row in rows}

	async def close(self):
		await self.engine.dispose()
