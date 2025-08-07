from typing import List, Dict, Any, Tuple
from hashlib import sha256
from dataclasses import dataclass

@dataclass
class ChunkSpec:
    start: int
    end: int

def approx_token_count(s: str) -> int:
    # Rough approximation: ~4 chars per token
    return max(1, len(s) // 4)

def deterministic_chunks(text: str, target_tokens: int = 300, overlap_tokens: int = 50) -> List[ChunkSpec]:
    if not text:
        return []
    target_chars = target_tokens * 4
    overlap_chars = overlap_tokens * 4
    chunks: List[ChunkSpec] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(n, start + target_chars)
        # Try to end at nearest newline before end, but not before start
        newline_pos = text.rfind("\n", start, end)
        if newline_pos > start + 50:
            end = newline_pos
        chunks.append(ChunkSpec(start=start, end=end))
        if end >= n:
            break
        start = max(end - overlap_chars, start + 1)
    return chunks

def chunk_page(document_id: str, filename: str, page_number: int, section: str, text: str) -> List[Dict[str, Any]]:
    specs = deterministic_chunks(text)
    result = []
    for spec in specs:
        span = text[spec.start:spec.end]
        h = sha256(f"{document_id}:{page_number}:{spec.start}:{spec.end}:{sha256(span.encode()).hexdigest()}".encode()).hexdigest()
        result.append({
            "id": h,
            "document_id": document_id,
            "filename": filename,
            "page_number": page_number,
            "section": section or None,
            "text": span,
            "char_start": spec.start,
            "char_end": spec.end,
            "hash": h
        })
    return result