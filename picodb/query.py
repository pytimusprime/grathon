"""
Query builder for PicoDB.

Provides chainable query API for filtering, ordering, and pagination.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from sqlalchemy import (
	Integer, asc, cast, delete, desc as sa_desc, func, and_, or_, select, update
)

if TYPE_CHECKING:
	from .core import AsyncPicodb


class Q:
	"""Query builder for composable database operations."""

	def __init__(self, model, db: Any):
		self.model = model
		self.db = db
		self._where = []
		self._order_by = []
		self._limit = None
		self._offset = None

	# ———— Simple Conditions ————
	def eq(self, field: str, value: Any):
		"""Equality (=)"""
		self._where.append(getattr(self.model, field) == value)
		return self

	def noeq(self, field: str, value: Any):
		"""Not equal (!=)"""
		self._where.append(getattr(self.model, field) != value)
		return self

	def gt(self, field: str, value: Any):
		"""Greater than (>)"""
		self._where.append(getattr(self.model, field) > value)
		return self

	def lt(self, field: str, value: Any):
		"""Less than (<)"""
		self._where.append(getattr(self.model, field) < value)
		return self

	def gte(self, field: str, value: Any):
		"""Greater than or equal (>=)"""
		self._where.append(getattr(self.model, field) >= value)
		return self

	def lte(self, field: str, value: Any):
		"""Less than or equal (<=)"""
		self._where.append(getattr(self.model, field) <= value)
		return self

	def like(self, field: str, pattern: str, *, case_sensitive: bool = True):
		"""LIKE pattern matching."""
		col = getattr(self.model, field)

		if not case_sensitive:
			clean_pattern = pattern.replace('%', '').strip()
			lower_pattern = clean_pattern.lower()

			if pattern.startswith('%') and pattern.endswith('%'):
				self._where.append(func.lower(col).like(f"%{lower_pattern}%"))
			elif pattern.endswith('%'):
				self._where.append(func.lower(col).like(f"{lower_pattern}%"))
			elif pattern.startswith('%'):
				self._where.append(func.lower(col).like(f"%{lower_pattern}"))
			else:
				self._where.append(func.lower(col) == lower_pattern)
		else:
			self._where.append(col.like(pattern))

		return self

	def ilike(self, field: str, pattern: str):
		"""Case-insensitive LIKE pattern matching."""
		self._where.append(getattr(self.model, field).ilike(pattern))
		return self

	def in_(self, field: str, values: List[Any]):
		"""IN operator"""
		self._where.append(getattr(self.model, field).in_(values))
		return self

	def not_in(self, field: str, values: List[Any]):
		"""NOT IN operator"""
		self._where.append(~getattr(self.model, field).in_(values))
		return self

	def between(self, field: str, start: Any, end: Any):
		"""BETWEEN operator"""
		self._where.append(getattr(self.model, field).between(start, end))
		return self

	# ———— Complex Conditions ————
	def where(self, *conditions):
		"""Add raw SQLAlchemy conditions."""
		self._where.extend(conditions)
		return self

	def or_(self, *conditions):
		"""OR condition"""
		if conditions:
			self._where.append(or_(*conditions))
		return self

	def and_(self, *conditions):
		"""AND condition (default)"""
		if conditions:
			self._where.append(and_(*conditions))
		return self

	# ———— Ordering ————
	def order_by(self, *fields: str, cast_int: bool = False):
		"""Order by field names. Prefix with '-' for descending."""
		for f in fields:
			if not isinstance(f, str):
				raise TypeError("order_by() only accepts string field names")

			desc_flag = f.startswith("-")
			field_name = f[1:] if desc_flag else f

			col = getattr(self.model, field_name)

			if cast_int:
				ordered_col = cast(col, Integer)
			else:
				ordered_col = col

			if desc_flag:
				self._order_by.append(sa_desc(ordered_col))
			else:
				self._order_by.append(asc(ordered_col))

		return self

	def order_by_raw(self, *expressions, direction: Optional[str] = None):
		"""Order by raw SQLAlchemy expressions."""
		direction = direction.lower() if isinstance(direction, str) else None

		for expr in expressions:
			if direction == "desc":
				if hasattr(expr, "desc"):
					self._order_by.append(expr.desc())
				else:
					self._order_by.append(expr)
			elif direction == "asc":
				if hasattr(expr, "asc"):
					self._order_by.append(expr.asc())
				else:
					self._order_by.append(expr)
			else:
				self._order_by.append(expr)

		return self

	def limit(self, n):
		"""Limit result count."""
		self._limit = n
		return self

	def offset(self, n):
		"""Offset result start."""
		self._offset = n
		return self

	# ———— Query Building ————
	def build(self):
		"""Build SQLAlchemy statement."""
		stmt = select(self.model)
		if self._where:
			stmt = stmt.where(and_(*self._where))
		if self._order_by:
			stmt = stmt.order_by(*self._order_by)
		if self._limit:
			stmt = stmt.limit(self._limit)
		if self._offset:
			stmt = stmt.offset(self._offset)
		return stmt

	# ———— Execution ————
	async def search(self):
		"""Execute query and return list."""
		stmt = self.build()
		async with self.db.session_factory() as session:
			result = await session.execute(stmt)
			rows = result.scalars().all()
			return list(self.db._batch_converter()(rows))

	async def stream(self):
		"""Execute query and stream results."""
		stmt = self.build()
		async with self.db.session_factory() as session:
			result = await session.execute(stmt)
			async for row in result.scalars():
				yield next(self.db._batch_converter()([row]))

	async def count(self):
		"""Count matching records."""
		stmt = select(func.count()).select_from(self.model)
		if self._where:
			stmt = stmt.where(and_(*self._where))
		async with self.db.session_factory() as session:
			res = await session.execute(stmt)
			return res.scalar_one()

	async def delete(self):
		"""Delete matching records."""
		stmt = delete(self.model)
		if self._where:
			stmt = stmt.where(and_(*self._where))
		async with self.db._write_lock:
			async with self.db.session_factory() as session:
				await session.execute(stmt)
				await session.commit()

	async def update(self, **values):
		"""Update matching records."""
		stmt = update(self.model).values(**values)
		if self._where:
			stmt = stmt.where(and_(*self._where))
		async with self.db._write_lock:
			async with self.db.session_factory() as session:
				await session.execute(stmt)
				await session.commit()
