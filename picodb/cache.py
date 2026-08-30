"""
PicodoCache — SQLite + Redis-like cache operations.

Provides key-value store, set operations, and TTL support on top of AsyncPicodb.
"""

import asyncio
import logging
import time
from dataclasses import is_dataclass
from typing import Any, Dict, Generic, List, Optional, Set, Type, TypeVar

import orjson
from sqlalchemy import delete, insert, select, text

from .core import AsyncPicodb

logger = logging.getLogger("picodb.cache")

SchemaT = TypeVar("SchemaT")


class PicodoCache(AsyncPicodb[SchemaT]):
	"""
	AsyncPicodb subclass with Redis-like cache operations.

	Adds key-value store, set operations, and TTL support via sidecar tables.
	All operations are async-safe and use the same write_lock as parent.
	"""

	def __init__(
		self,
		schema_cls: Type[SchemaT],
		path: str = "sqlite+aiosqlite:///cache.db",
		**kwargs
	):
		if not is_dataclass(schema_cls):
			raise TypeError("schema_cls must be a dataclass type")
		super().__init__(schema_cls, path, **kwargs)

	async def init_db(self):
		"""Initialize database with cache sidecar tables."""
		await super().init_db()

		async with self.engine.begin() as conn:
			await conn.execute(text("""
				CREATE TABLE IF NOT EXISTS _kv_store (
					key TEXT PRIMARY KEY,
					value TEXT NOT NULL,
					expires_at REAL
				);
			"""))

			await conn.execute(text("""
				CREATE TABLE IF NOT EXISTS _set_store (
					key TEXT NOT NULL,
					member TEXT NOT NULL,
					PRIMARY KEY (key, member)
				);
			"""))
			await conn.commit()

		logger.debug("Cache tables initialized")

	async def clear_db(self):
		"""Clear all data including cache tables."""
		await super().clear_db()
		async with self._write_lock:
			async with self.engine.begin() as conn:
				await conn.execute(text("DELETE FROM _kv_store;"))
				await conn.execute(text("DELETE FROM _set_store;"))
				await conn.commit()

	# ========== KEY-VALUE OPERATIONS ==========

	async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
		"""
		Store a value in cache with optional TTL.

		Args:
			key: Cache key
			value: Any JSON-serializable value
			ttl: Time-to-live in seconds. None = no expiry.
		"""
		if not isinstance(key, str):
			raise TypeError("key must be a string")

		serialized = orjson.dumps(value).decode("utf-8")
		expires_at = None if ttl is None else time.time() + ttl

		async with self._write_lock:
			async with self.session_factory() as session:
				stmt = text("""
					INSERT INTO _kv_store (key, value, expires_at)
					VALUES (:key, :value, :expires_at)
					ON CONFLICT(key) DO UPDATE SET
						value = :value,
						expires_at = :expires_at
				""")
				await session.execute(stmt, {"key": key, "value": serialized, "expires_at": expires_at})
				await session.commit()

	async def get_cache(self, key: str, default: Any = None) -> Any:
		"""
		Retrieve a value from cache.

		Returns `default` if key missing or expired.
		"""
		if not isinstance(key, str):
			raise TypeError("key must be a string")

		async with self.session_factory() as session:
			stmt = text("SELECT value, expires_at FROM _kv_store WHERE key = :key")
			result = await session.execute(stmt, {"key": key})
			row = result.one_or_none()

			if not row:
				return default

			value_str, expires_at = row
			if expires_at is not None and time.time() > expires_at:
				# Key expired; delete it
				await self._delete_key_internal(session, key)
				return default

			try:
				return orjson.loads(value_str)
			except orjson.JSONDecodeError:
				logger.warning(f"Failed to decode cache value for key '{key}'")
				return default

	# Alias for Redis-like API
	async def get(self, key: str, default: Any = None) -> Any:  # type: ignore
		"""Alias for get_cache for Redis-like interface."""
		return await self.get_cache(key, default)

	async def _delete_key_internal(self, session, key: str) -> None:
		"""Internal helper to delete a key within an existing session."""
		await session.execute(text("DELETE FROM _kv_store WHERE key = :key"), {"key": key})

	async def delete_key(self, key: str) -> bool:
		"""
		Delete a cache key.

		Returns True if key existed, False otherwise.
		"""
		if not isinstance(key, str):
			raise TypeError("key must be a string")

		async with self._write_lock:
			async with self.session_factory() as session:
				result = await session.execute(
					text("DELETE FROM _kv_store WHERE key = :key"),
					{"key": key}
				)
				await session.commit()
				return bool(result.rowcount and result.rowcount > 0)  # type: ignore

	async def exists_key(self, key: str) -> bool:
		"""Check if a key exists and is not expired."""
		if not isinstance(key, str):
			raise TypeError("key must be a string")

		async with self.session_factory() as session:
			stmt = text("SELECT expires_at FROM _kv_store WHERE key = :key")
			result = await session.execute(stmt, {"key": key})
			row = result.one_or_none()

			if not row:
				return False

			expires_at = row[0]
			if expires_at is not None and time.time() > expires_at:
				return False

			return True

	async def keys(self, pattern: Optional[str] = None) -> List[str]:
		"""
		List all cache keys, optionally filtered by GLOB pattern.

		Pattern uses SQL GLOB syntax (e.g., "user:*", "session:*:data")
		"""
		async with self.session_factory() as session:
			if pattern:
				stmt = text("SELECT key FROM _kv_store WHERE key GLOB :pattern")
				result = await session.execute(stmt, {"pattern": pattern})
			else:
				stmt = text("SELECT key FROM _kv_store")
				result = await session.execute(stmt)

			rows = result.fetchall()
			keys = [row[0] for row in rows if row[0] is not None]

			# Filter expired
			now = time.time()
			valid_keys = []
			for key in keys:
				stmt2 = text("SELECT expires_at FROM _kv_store WHERE key = :key")
				res2 = await session.execute(stmt2, {"key": key})
				row2 = res2.one_or_none()
				if row2:
					expires_at = row2[0]
					if expires_at is None or time.time() <= expires_at:
						valid_keys.append(key)

			return valid_keys

	async def mset(self, mapping: Dict[str, Any]) -> None:
		"""Set multiple key-value pairs at once."""
		if not isinstance(mapping, dict):
			raise TypeError("mapping must be a dict")

		async with self._write_lock:
			async with self.session_factory() as session:
				for key, value in mapping.items():
					if not isinstance(key, str):
						raise TypeError("All keys must be strings")

					serialized = orjson.dumps(value).decode("utf-8")
					stmt = text("""
						INSERT INTO _kv_store (key, value, expires_at)
						VALUES (:key, :value, NULL)
						ON CONFLICT(key) DO UPDATE SET value = :value
					""")
					await session.execute(stmt, {"key": key, "value": serialized})

				await session.commit()

	async def mget(self, keys: List[str]) -> Dict[str, Any]:
		"""Get multiple keys at once. Returns dict with existing keys only."""
		if not isinstance(keys, list):
			raise TypeError("keys must be a list")

		result = {}
		async with self.session_factory() as session:
			for key in keys:
				if not isinstance(key, str):
					raise TypeError("All keys must be strings")

				stmt = text("SELECT value, expires_at FROM _kv_store WHERE key = :key")
				row = await session.execute(stmt, {"key": key})
				row_data = row.one_or_none()

				if row_data:
					value_str, expires_at = row_data
					if expires_at is None or time.time() <= expires_at:
						try:
							result[key] = orjson.loads(value_str)
						except orjson.JSONDecodeError:
							pass

		return result

	async def incr(self, key: str, amount: int = 1) -> int:
		"""
		Increment numeric value. Creates key if not exists.

		Returns the new value.
		"""
		if not isinstance(key, str):
			raise TypeError("key must be a string")
		if not isinstance(amount, int):
			raise TypeError("amount must be an int")

		async with self._write_lock:
			async with self.session_factory() as session:
				stmt = text("SELECT value FROM _kv_store WHERE key = :key")
				result = await session.execute(stmt, {"key": key})
				row = result.one_or_none()

				current = 0
				if row:
					try:
						current = int(orjson.loads(row[0]))
					except (orjson.JSONDecodeError, ValueError):
						current = 0

				new_value = current + amount
				serialized = orjson.dumps(new_value).decode("utf-8")

				stmt_upsert = text("""
					INSERT INTO _kv_store (key, value, expires_at)
					VALUES (:key, :value, NULL)
					ON CONFLICT(key) DO UPDATE SET value = :value
				""")
				await session.execute(stmt_upsert, {"key": key, "value": serialized})
				await session.commit()

				return new_value

	async def decr(self, key: str, amount: int = 1) -> int:
		"""Decrement numeric value. Creates key if not exists."""
		return await self.incr(key, -amount)

	async def expire(self, key: str, ttl: int) -> bool:
		"""
		Set TTL on an existing key.

		Returns True if key existed, False otherwise.
		"""
		if not isinstance(key, str):
			raise TypeError("key must be a string")
		if not isinstance(ttl, int):
			raise TypeError("ttl must be an int")

		expires_at = time.time() + ttl

		async with self._write_lock:
			async with self.session_factory() as session:
				result = await session.execute(
					text("UPDATE _kv_store SET expires_at = :expires_at WHERE key = :key"),
					{"key": key, "expires_at": expires_at}
				)
				await session.commit()
				return bool(result.rowcount and result.rowcount > 0)  # type: ignore

	async def ttl(self, key: str) -> int:
		"""
		Get remaining TTL in seconds.

		Returns:
			-1 if key exists but has no expiry
			-2 if key missing or expired
		"""
		if not isinstance(key, str):
			raise TypeError("key must be a string")

		async with self.session_factory() as session:
			stmt = text("SELECT expires_at FROM _kv_store WHERE key = :key")
			result = await session.execute(stmt, {"key": key})
			row = result.one_or_none()

			if not row:
				return -2

			expires_at = row[0]
			if expires_at is None:
				return -1

			remaining = expires_at - time.time()
			if remaining <= 0:
				return -2

			return int(remaining)

	async def evict_expired(self) -> int:
		"""Delete all expired keys from both cache tables. Returns count deleted."""
		async with self._write_lock:
			async with self.session_factory() as session:
				now = time.time()

				# Delete expired KV pairs
				stmt_kv = text("DELETE FROM _kv_store WHERE expires_at IS NOT NULL AND expires_at < :now")
				result_kv = await session.execute(stmt_kv, {"now": now})
				count = int(result_kv.rowcount or 0)  # type: ignore

				await session.commit()
				return count

	# ========== SET OPERATIONS ==========

	async def sadd(self, key: str, *members: Any) -> int:
		"""
		Add members to a set.

		Args:
			key: Set key
			*members: Members to add (can be strings, ints, record_ids, etc.)

		Returns: Number of members added (not counting duplicates)
		"""
		if not isinstance(key, str):
			raise TypeError("key must be a string")

		async with self._write_lock:
			async with self.session_factory() as session:
				added = 0
				for member in members:
					member_str = str(member)  # Convert to string for storage

					try:
						stmt = text("""
							INSERT INTO _set_store (key, member)
							VALUES (:key, :member)
						""")
						await session.execute(stmt, {"key": key, "member": member_str})
						added += 1
					except Exception:
						# Duplicate, skip
						pass

				await session.commit()
				return added

	async def srem(self, key: str, *members: Any) -> int:
		"""
		Remove members from a set.

		Returns: Number of members removed
		"""
		if not isinstance(key, str):
			raise TypeError("key must be a string")

		async with self._write_lock:
			async with self.session_factory() as session:
				removed = 0
				for member in members:
					member_str = str(member)

					result = await session.execute(
						text("DELETE FROM _set_store WHERE key = :key AND member = :member"),
						{"key": key, "member": member_str}
					)
					removed += int(result.rowcount or 0)  # type: ignore

				await session.commit()
				return removed

	async def smembers(self, key: str) -> Set[str]:
		"""Get all members of a set."""
		if not isinstance(key, str):
			raise TypeError("key must be a string")

		async with self.session_factory() as session:
			stmt = text("SELECT member FROM _set_store WHERE key = :key")
			result = await session.execute(stmt, {"key": key})
			rows = result.fetchall()
			return {row[0] for row in rows if row[0] is not None}

	async def sismember(self, key: str, member: Any) -> bool:
		"""Check if member is in set."""
		if not isinstance(key, str):
			raise TypeError("key must be a string")

		member_str = str(member)

		async with self.session_factory() as session:
			stmt = text("SELECT 1 FROM _set_store WHERE key = :key AND member = :member LIMIT 1")
			result = await session.execute(stmt, {"key": key, "member": member_str})
			return result.one_or_none() is not None

	async def scard(self, key: str) -> int:
		"""Get cardinality (number of members) of a set."""
		if not isinstance(key, str):
			raise TypeError("key must be a string")

		async with self.session_factory() as session:
			stmt = text("SELECT COUNT(*) FROM _set_store WHERE key = :key")
			result = await session.execute(stmt, {"key": key})
			count = result.scalar_one() or 0
			return count
