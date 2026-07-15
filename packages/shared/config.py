from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    host: str = os.getenv("APP_HOST", "127.0.0.1")
    port: int = int(os.getenv("APP_PORT", "8000"))
    database_path: str = os.getenv("DATABASE_PATH", "data/sales_intelligence.db")


settings = Settings()
