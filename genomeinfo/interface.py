from pathlib import Path
from typing import NoReturn, Self

import pyarrow.parquet as pq

__all__ = ["GenomeInfo"]


class GenomeInfo:
    _instance = None
    _db_path = Path(__file__).parent / "data" / "db.parquet"

    def __new__(cls, *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super(GenomeInfo, cls).__new__(cls)
            cls._instance._load_db()
        return cls._instance

    def _load_db(self) -> NoReturn:
        """Private method to connect to the database."""
        self._data = pq.read_table(self._db_path).to_pandas()

    @classmethod
    def connect(cls) -> Self:
        """Returns the singleton instance of GenomeInfo."""
        return cls()
