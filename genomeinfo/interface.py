from __future__ import annotations

from pathlib import Path

import pyarrow.parquet as pq

__all__ = ["GenomeInfo"]


class GenomeInfo:
    _instance = None
    _db_path = Path(__file__).parent / "data" / "db.parquet"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_db()
        return cls._instance

    def _load_db(self) -> None:
        """Private method to connect to the database."""
        self._data = pq.read_table(self._db_path).to_pandas()

    @classmethod
    def connect(cls):
        """Returns the singleton instance of GenomeInfo."""
        return cls()
