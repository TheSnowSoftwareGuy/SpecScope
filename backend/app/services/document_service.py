import hashlib
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any, Tuple
import sqlite3
import logging
from pathlib import Path
from ..config import settings, sqlite_conn
from ..core.pdf_processor import extract_pdf
from ..core.text_chunker import chunk_page
from ..core.embeddings import upsert_embeddings

logger = logging.getLogger(__name__)

def file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

async def process_pdf(filepath: str, filename: str) -> Dict[str, Any]:
    """
    Process a PDF: dedupe, extract pages, chunk, embed, and index.
    """
    # Dedupe by file hash
    fhash = file_sha256(filepath)
    cur = sqlite_conn.execute("SELECT id, pages_count FROM documents WHERE file_hash = ?", (fhash,))
    row = cur.fetchone()
    if row:
        logger.info("Duplicate file detected, skipping processing")
        return {"id": row["id"], "filename": filename, "pages_count": row["pages_count"], "uploaded_at": datetime.utcnow().isoformat()}

    doc_id = str(uuid.uuid4())
    # Extract pages
    pages, sections = await extract_pdf(filepath, max_pages=settings.MAX_PAGES_PER_UPLOAD)
    pages_count = len(pages)
    # Insert document
    sqlite_conn.execute(
        "INSERT INTO documents (id, filename, file_hash, pages_count, uploaded_at) VALUES (?, ?, ?, ?, ?)",
        (doc_id, filename, fhash, pages_count, datetime.utcnow().isoformat()),
    )
    sqlite_conn.commit()
    # Insert pages and chunks
    all_chunks: List[Dict[str, Any]] = []
    for p, section in zip(pages, sections):
        sqlite_conn.execute(
            "INSERT INTO pages (document_id, page_number, text, width, height) VALUES (?, ?, ?, ?, ?)",
            (doc_id, p.page_number, p.text, p.width, p.height)
        )
        chs = chunk_page(doc_id, filename, p.page_number, section, p.text)
        for c in chs:
            sqlite_conn.execute(
                "INSERT INTO chunks (id, document_id, filename, page_number, section, text, char_start, char_end, hash, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (c["id"], c["document_id"], c["filename"], c["page_number"], c["section"], c["text"], c["char_start"], c["char_end"], c["hash"], datetime.utcnow().isoformat())
            )
        all_chunks.extend(chs)
    sqlite_conn.commit()
    # Embed and upsert to vector index
    await upsert_embeddings(all_chunks, model=settings.EMBEDDING_MODEL, api_key=settings.OPENAI_API_KEY)
    return {"id": doc_id, "filename": filename, "pages_count": pages_count, "uploaded_at": datetime.utcnow().isoformat()}

def store_upload(temp_path: str, original_filename: str) -> str:
    """
    Store the original file under STORAGE_PATH/{doc_id}/original.pdf
    Returns the stored path.
    """
    # For dedupe, compute hash first then set dir by UUID but also store by hash for direct mapping
    fname = original_filename
    # For now, store in a temp staging path; process_pdf will handle eventual doc id, we keep file in place
    dest_dir = Path(settings.STORAGE_PATH)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / fname
    os.replace(temp_path, dest_path)
    return str(dest_path)

def list_documents() -> List[Dict[str, Any]]:
    cur = sqlite_conn.execute("SELECT * FROM documents ORDER BY uploaded_at DESC")
    return [dict(row) for row in cur.fetchall()]

def get_page_text(document_id: str, page_number: int) -> Dict[str, Any]:
    cur = sqlite_conn.execute("SELECT * FROM pages WHERE document_id = ? AND page_number = ?", (document_id, page_number))
    row = cur.fetchone()
    if not row:
        raise FileNotFoundError("Page not found")
    return dict(row)