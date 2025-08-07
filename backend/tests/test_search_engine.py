import pytest
from backend.app.config import sqlite_conn
from backend.app.core.search_engine import bm25_keyword_search, hybrid_search
from backend.app.core.embeddings import upsert_embeddings

def seed_simple_corpus():
    # Create a fake document, pages, chunks
    sqlite_conn.execute(
        "INSERT INTO documents (id, filename, file_hash, pages_count, uploaded_at) VALUES (?, ?, ?, ?, ?)",
        ("doc1", "Specs.pdf", "hash1", 2, "2024-01-01T00:00:00Z")
    )
    sqlite_conn.execute(
        "INSERT INTO chunks (id, document_id, filename, page_number, section, text, char_start, char_end, hash, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("c1", "doc1", "Specs.pdf", 1, "Division 01", "Liquidated damages: $2,000 per calendar day.", 0, 44, "h1", "2024-01-01T00:00:00Z")
    )
    sqlite_conn.execute(
        "INSERT INTO chunks (id, document_id, filename, page_number, section, text, char_start, char_end, hash, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("c2", "doc1", "Specs.pdf", 2, "Addendum", "Submittals due 14 days after award.", 0, 34, "h2", "2024-01-01T00:00:00Z")
    )
    sqlite_conn.commit()

@pytest.mark.asyncio
async def test_keyword_and_hybrid_search():
    # Seed
    seed_simple_corpus()
    # Upsert vectors offline (hash-based)
    await upsert_embeddings([
        {"id": "c1", "text": "Liquidated damages: $2,000 per calendar day."},
        {"id": "c2", "text": "Submittals due 14 days after award."},
    ], model="text-embedding-3-large", api_key=None)

    kw = bm25_keyword_search("liquidated damages", top_k=5)
    assert any(r["chunk_id"] == "c1" for r in kw)

    res = await hybrid_search("What are the liquidated damages?", top_k=2, alpha=0.5, filters=None)
    assert len(res) >= 1
    # Deterministic: ensure ordering stable on multiple runs
    res2 = await hybrid_search("What are the liquidated damages?", top_k=2, alpha=0.5, filters=None)
    assert [r["chunk_id"] for r in res] == [r["chunk_id"] for r in res2]
