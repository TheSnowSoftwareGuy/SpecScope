from typing import List, Dict, Any, Optional
import logging
from ..core.search_engine import hybrid_search

logger = logging.getLogger(__name__)

async def search(query: str, top_k: int = 10, alpha: float = 0.5, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    return await hybrid_search(query, top_k, alpha, filters)

def build_highlights(text: str, terms: List[str]) -> List[str]:
    t = text.lower()
    hits = []
    for term in terms:
        if term.lower() in t:
            hits.append(term)
    return hits