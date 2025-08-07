from __future__ import annotations
import sqlite3
from typing import List, Dict, Any, Tuple, Optional
import logging
import numpy as np
from ..config import sqlite_conn, settings
from .embeddings import embed_texts, global_vector_index
from ..utils.patterns import MODAL_VERBS_REGEX

logger = logging.getLogger(__name__)

def init_indices(conn: sqlite3.Connection) -> None:
    # Ensure triggers for FTS5 content synchronization
    conn.executescript(
        """
        CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
            INSERT INTO chunks_fts(rowid, text) VALUES (new.rowid, new.text);
        END;
        CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
            INSERT INTO chunks_fts(chunks_fts, rowid, text) VALUES('delete', old.rowid, old.text);
        END;
        CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
            INSERT INTO chunks_fts(chunks_fts, rowid, text) VALUES('delete', old.rowid, old.text);
            INSERT INTO chunks_fts(rowid, text) VALUES (new.rowid, new.text);
        END;
        """
    )
    conn.commit()

init_indices(sqlite_conn)

def bm25_keyword_search(query: str, top_k: int, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    q = query
    sql = """
    SELECT c.*, bm25(chunks_fts) as kw_score
    FROM chunks_fts
    JOIN chunks c ON c.rowid = chunks_fts.rowid
    WHERE chunks_fts MATCH ?
    """
    params = [q]
    # Filters by document_id
    if filters and filters.get("doc_ids"):
        placeholders = ",".join("?" * len(filters["doc_ids"]))
        sql += f" AND c.document_id IN ({placeholders})"
        params.extend(filters["doc_ids"])
    sql += " ORDER BY kw_score LIMIT ?"
    params.append(top_k)
    cur = sqlite_conn.execute(sql, params)
    rows = cur.fetchall()
    results = []
    for r in rows:
        results.append({
            "chunk_id": r["id"],
            "document_id": r["document_id"],
            "filename": r["filename"],
            "page_number": r["page_number"],
            "section": r["section"],
            "text": r["text"],
            "char_start": r["char_start"],
            "char_end": r["char_end"],
            "keyword_score": float(r["kw_score"]),
        })
    return results

async def vector_search(query: str, top_k: int, filters: Optional[Dict[str, Any]] = None) -> List[Tuple[str, float]]:
    vec = (await embed_texts([query], model=settings.EMBEDDING_MODEL, api_key=settings.OPENAI_API_KEY))[0]
    sims = global_vector_index.query(vec, top_k=top_k)
    # Note: filters applied later in merge (we don't store doc ids in vector index)
    return sims

def normalize_scores(values: List[float]) -> List[float]:
    if not values:
        return []
    lo, hi = min(values), max(values)
    if hi - lo < 1e-9:
        return [0.5 for _ in values]
    return [(v - lo) / (hi - lo) for v in values]

async def hybrid_search(query: str, top_k: int, alpha: float, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    vec_k = top_k * 2
    kw_k = top_k * 2
    kw_results = bm25_keyword_search(query, kw_k, filters)
    vect_sims = await vector_search(query, vec_k, filters)
    # Build map for vector sims
    vec_map = {cid: score for cid, score in vect_sims}
    # Merge by chunk id
    candidates: Dict[str, Dict[str, Any]] = {}
    # Seed with keyword
    for r in kw_results:
        candidates[r["chunk_id"]] = {
            **r,
            "vector_score": vec_map.get(r["chunk_id"], 0.0)
        }
    # Add vector-only hits
    if vec_map:
        placeholders = ",".join("?" * len(vec_map))
        cur = sqlite_conn.execute(f"SELECT * FROM chunks WHERE id IN ({placeholders})", list(vec_map.keys()))
        for row in cur.fetchall():
            cid = row["id"]
            if filters and filters.get("doc_ids") and row["document_id"] not in set(filters["doc_ids"]):
                continue
            if cid not in candidates:
                candidates[cid] = {
                    "chunk_id": row["id"],
                    "document_id": row["document_id"],
                    "filename": row["filename"],
                    "page_number": row["page_number"],
                    "section": row["section"],
                    "text": row["text"],
                    "char_start": row["char_start"],
                    "char_end": row["char_end"],
                    "keyword_score": 0.0,
                    "vector_score": vec_map.get(cid, 0.0)
                }
    # Normalize
    kw_norm = normalize_scores([c["keyword_score"] for c in candidates.values()])
    vec_norm = normalize_scores([c["vector_score"] for c in candidates.values()])
    for (c, k, v) in zip(candidates.values(), kw_norm, vec_norm):
        c["keyword_norm"] = k
        c["vector_norm"] = v
        c["hybrid"] = alpha * v + (1 - alpha) * k
    # Deterministic tie-breakers
    items = list(candidates.values())
    items.sort(key=lambda x: (x["hybrid"], x["keyword_norm"], -x["page_number"]), reverse=True)
    # Build snippets and highlights
    results = []
    for it in items[:top_k]:
        highlights = []
        # basic keyword highlights: split query words >3 chars
        for w in set([w for w in re_split_words(query) if len(w) > 3]):
            if w.lower() in it["text"].lower():
                highlights.append(w)
        # Confidence mapping
        conf = map_confidence(it["hybrid"], it["text"])
        results.append({
            "chunk_id": it["chunk_id"],
            "document_id": it["document_id"],
            "filename": it["filename"],
            "page_number": it["page_number"],
            "section": it["section"],
            "snippet": build_snippet(it["text"], highlights),
            "highlights": highlights,
            "scores": {"vector": it["vector_norm"], "keyword": it["keyword_norm"], "hybrid": it["hybrid"]},
            "confidence": conf
        })
    return results

def re_split_words(q: str) -> List[str]:
    import re
    return re.findall(r"[A-Za-z0-9_]+", q)

def build_snippet(text: str, highlights: List[str], window: int = 200) -> str:
    if not highlights:
        return text[:window].strip()
    # pick first highlight
    t_low = text.lower()
    for h in highlights:
        idx = t_low.find(h.lower())
        if idx != -1:
            start = max(0, idx - window // 2)
            end = min(len(text), idx + window // 2)
            return text[start:end].strip()
    return text[:window].strip()

def map_confidence(hybrid: float, text: str) -> float:
    base = hybrid
    if MODAL_VERBS_REGEX.search(text):
        base = min(1.0, base + 0.15)
    return max(0.0, min(1.0, base))