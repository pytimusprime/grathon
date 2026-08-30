"""
Data formatting utilities for PicoDB.

Converts Python values to storage-friendly formats for consistent database storage.
"""

import datetime
from typing import Any

import orjson


def data_formatter(value: Any) -> Any:
	"""Convert Python values to database-storable format."""
	if value is None:
		return None
	if isinstance(value, bool):
		return value
	if isinstance(value, (datetime.date, datetime.datetime)):
		return value.isoformat()
	if isinstance(value, (list, dict, tuple)):
		return orjson.dumps(value, option=orjson.OPT_SERIALIZE_NUMPY).decode()
	if isinstance(value, (int, float)):
		return value
	return str(value)
