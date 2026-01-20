import os
from contextlib import contextmanager
from pathlib import Path

from dotenv import load_dotenv
import psycopg

_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=_ENV_PATH)


def _get_db_url() -> str:
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    name = os.getenv("POSTGRES_DB", "task_risk")
    user = os.getenv("POSTGRES_USER", "task_risk")
    password = os.getenv("POSTGRES_PASSWORD", "task_risk")
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


@contextmanager
def get_conn():
    conn = psycopg.connect(_get_db_url())
    try:
        yield conn
    finally:
        conn.close()
