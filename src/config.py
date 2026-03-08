from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / '.env')


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    llm_model: str
    database_url: str
    top_k_rows: int
    query_timeout_seconds: int


def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv('OPENAI_API_KEY', ''),
        llm_model=os.getenv('LLM_MODEL', 'gpt-4.1-mini'),
        database_url=os.getenv(
            'DATABASE_URL',
            'mysql+pymysql://analytics_user:analytics_password@localhost:3306/analytics_poc',
        ),
        top_k_rows=int(os.getenv('TOP_K_ROWS', '200')),
        query_timeout_seconds=int(os.getenv('QUERY_TIMEOUT_SECONDS', '20')),
    )
