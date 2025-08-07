import os
from typing import List, Optional
from pydantic import BaseSettings, AnyUrl, validator
import logging
import json
import sys
import sqlite3
from pathlib import Path

class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENV: Optional[str] = None
    PINECONE_INDEX: str = "specscope-mvp"
    PINECONE_NAMESPACE: str = "default"
    BACKEND_PORT: int = 8000
    ALLOWED_ORIGINS: str = "http://localhost:5173"
    MAX_WORKERS: int = 4
    EMBEDDING_MODEL: str = "text-embedding-3-large"
    GPT_MODEL: str = "gpt-4o-mini"
    SQLITE_PATH: str = "./data/specscope.db"
    STORAGE_PATH: str = "./data/storage"
    LOG_LEVEL: str = "INFO"
    RATE_LIMIT_RPM: int = 300
    LANGCHAIN_TRACING_V2: bool = False
    MAX_PAGES_PER_UPLOAD: int = 3000

    @validator("ALLOWED_ORIGINS")
    def parse_origins(cls, v: str) -> str:
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

# Ensure storage and data dirs
Path(settings.STORAGE_PATH).mkdir(parents=True, exist_ok=True)
Path(os.path.dirname(settings.SQLITE_PATH)).mkdir(parents=True, exist_ok=True)

def get_sqlite_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.SQLITE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Enable FTS5, foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_sqlite_schema(conn: sqlite3.Connection) -> None:
    # documents, pages, chunks, FTS5 on chunks
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            file_hash TEXT NOT NULL UNIQUE,
            pages_count INTEGER NOT NULL,
            uploaded_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS pages (
            document_id TEXT NOT NULL,
            page_number INTEGER NOT NULL,
            text TEXT NOT NULL,
            width REAL,
            height REAL,
            PRIMARY KEY (document_id, page_number),
            FOREIGN KEY(document_id) REFERENCES documents(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS chunks (
            id TEXT PRIMARY KEY,
            document_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            page_number INTEGER NOT NULL,
            section TEXT,
            text TEXT NOT NULL,
            char_start INTEGER NOT NULL,
            char_end INTEGER NOT NULL,
            hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(document_id) REFERENCES documents(id) ON DELETE CASCADE
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
            text,
            content='chunks',
            content_rowid='rowid',
            tokenize = 'porter'
        );
        CREATE TABLE IF NOT EXISTS chunk_vectors (
            chunk_id TEXT PRIMARY KEY,
            dim INTEGER NOT NULL,
            vector BLOB NOT NULL,
            FOREIGN KEY(chunk_id) REFERENCES chunks(id) ON DELETE CASCADE
        );
        """
    )
    conn.commit()

# JSON logging setup
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log = {
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
        }
        if record.exc_info:
            log["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log)

def configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = []
    root.addHandler(handler)
    root.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

configure_logging()
sqlite_conn = get_sqlite_conn()
init_sqlite_schema(sqlite_conn)

