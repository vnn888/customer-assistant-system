"""
PostgreSQL connection helper. Reads DATABASE_URL from environment (.env),
e.g.: postgresql://user:password@host:5432/dbname
"""
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL not set. Copy .env.example to .env and fill it in."
        )
    return psycopg2.connect(url)
