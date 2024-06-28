import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import numpy as np
from typing import Any, Dict, List, Optional, Self
from pathlib import Path
import os

__all__ = ["GenomeInfo"]


class GenomeInfo:
    _instance = None
    _db_path = Path(__file__).parent / "data" / "db.parquet"

    def __new__(cls, *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super(GenomeInfo, cls).__new__(cls)
            cls._instance._load_db()
        return cls._instance

    def _load_db(self) -> None:
        """Private method to connect to the database."""
        self._data = pq.read_table(self._db_path).to_pandas()

    @classmethod
    def connect(cls) -> Self:
        """Returns the singleton instance of GenomeInfo."""
        return cls()
