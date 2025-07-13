from __future__ import annotations

import abc
import json
import os
import sqlite3
from pathlib import Path
from typing import Dict, Tuple

from .schemas import Schema


class SchemaStore(abc.ABC):
    """Abstract persistence layer for schemas."""

    def __init__(self, path: str):
        self.path = path

    # ------------------------------------------------------------------
    @abc.abstractmethod
    def load(self) -> Dict[Tuple[str, str], Schema]:
        """Load schemas from storage."""

    @abc.abstractmethod
    def save(self, mapping: Dict[Tuple[str, str], Schema]) -> None:
        """Persist *mapping* to storage."""


# ----------------------------------------------------------------------
# JSON backend
# ----------------------------------------------------------------------

class JsonSchemaStore(SchemaStore):
    """Stores schemas as a simple JSON list."""

    def load(self) -> Dict[Tuple[str, str], Schema]:
        if not os.path.exists(self.path):
            return {}
        try:
            with open(self.path, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            return {tuple(item["symbols"]): Schema.from_dict(item) for item in data}
        except Exception as e:
            print(f"[JsonSchemaStore] Warning: failed to load {self.path}: {e}")
            return {}

    def save(self, mapping: Dict[Tuple[str, str], Schema]) -> None:
        try:
            with open(self.path, "w", encoding="utf-8") as fp:
                json.dump([s.to_dict() for s in mapping.values()], fp, indent=2)
        except Exception as e:
            print(f"[JsonSchemaStore] Warning: failed to save {self.path}: {e}")


# ----------------------------------------------------------------------
# SQLite backend
# ----------------------------------------------------------------------

class SQLiteSchemaStore(SchemaStore):
    TABLE_NAME = "schemas"

    def _init_db(self, conn: sqlite3.Connection):
        conn.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                symbol_a TEXT NOT NULL,
                symbol_b TEXT NOT NULL,
                count INTEGER NOT NULL,
                cumulative_strength REAL NOT NULL,
                last_seen REAL NOT NULL,
                PRIMARY KEY(symbol_a, symbol_b)
            );"""
        )
        conn.commit()

    def load(self) -> Dict[Tuple[str, str], Schema]:
        path_obj = Path(self.path)
        conn = sqlite3.connect(path_obj)
        self._init_db(conn)
        cur = conn.cursor()
        cur.execute(f"SELECT symbol_a, symbol_b, count, cumulative_strength, last_seen FROM {self.TABLE_NAME}")
        rows = cur.fetchall()
        conn.close()
        mapping: Dict[Tuple[str, str], Schema] = {}
        for a, b, count, cum_strength, last_seen in rows:
            mapping[(a, b)] = Schema(symbols=(a, b), count=count, cumulative_strength=cum_strength, last_seen=last_seen)
        return mapping

    def save(self, mapping: Dict[Tuple[str, str], Schema]) -> None:
        path_obj = Path(self.path)
        conn = sqlite3.connect(path_obj)
        self._init_db(conn)
        cur = conn.cursor()
        cur.execute("BEGIN TRANSACTION;")
        cur.execute(f"DELETE FROM {self.TABLE_NAME};")
        cur.executemany(
            f"INSERT INTO {self.TABLE_NAME} (symbol_a, symbol_b, count, cumulative_strength, last_seen) VALUES (?,?,?,?,?);",
            [(
                s.symbols[0],
                s.symbols[1],
                s.count,
                s.cumulative_strength,
                s.last_seen,
            ) for s in mapping.values()]
        )
        conn.commit()
        conn.close() 