from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import pandas as pd


class DatabaseClient:
    def __init__(self, database_url: str, query_timeout_seconds: int = 20):
        self.query_timeout_seconds = query_timeout_seconds
        self.engine: Engine = create_engine(
            database_url,
            future=True,
            pool_pre_ping=True,
        )

    def run_select(self, sql: str) -> pd.DataFrame:
        with self.engine.connect() as conn:
            # MySQL supports session-level MAX_EXECUTION_TIME in milliseconds.
            timeout_ms = max(1000, int(self.query_timeout_seconds * 1000))
            conn.execute(text(f'SET SESSION MAX_EXECUTION_TIME={timeout_ms}'))
            return pd.read_sql(text(sql), conn)
