from typing import List, Dict, Any
import sqlite3
from ..config import sqlite_conn
from ..models.query import Citation

def validate_citations(citations: List[Citation]) -> bool:
    """
    Ensure each quote is an exact substring of its chunk and char ranges align.
    """
    for c in citations:
        row = sqlite_conn.execute("SELECT text, char_start, char_end FROM chunks WHERE id = ?", (c.chunk_id,)).fetchone()
        if not row:
            return False
        full_text = row["text"]
        quote = c.quote
        if quote not in full_text:
            return False
        # If provided char positions, ensure they point at the quoted text
        start = full_text.find(quote)
        end = start + len(quote)
        if c.char_start != 0 and (c.char_start != start or c.char_end != end):
            return False
    return True