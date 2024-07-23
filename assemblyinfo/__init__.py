from __future__ import annotations

from . import core
from .interface import AssemblyInfo

for module in [core]:
    for name, func in module.__dict__.items():
        if callable(func) and not name.startswith("_"):
            setattr(AssemblyInfo, name, func)

__all__ = ["AssemblyInfo"]


_db: AssemblyInfo | None = None

def connect() -> AssemblyInfo:
    global _db
    if _db is None:
        _db = AssemblyInfo()
    return _db
