from typing import Dict, Any, List, Optional
import logging
from ..models.query import QARequest, QAResponse, Citation
from ..services.search_service import search
from ..config import settings

logger = logging.getLogger(__name__)

QA_SYSTEM_PROMPT = (
    "You are SpecScope, a construction specifications assistant. Only answer using the provided EXCERPTS. "
    "Do not use outside knowledge. For every statement, include exact quotations and page references. "
    "If the excerpts are insufficient, say “Insufficient information in provided documents.”"
)

async def answer_question(req: QARequest) -> QAResponse:
    # Retrieve candidates
    results = await search(req.question, top_k=req.top_k, alpha=0.5, filters=req.doc_filter)
    if not results:
        return QAResponse(answer="Insufficient information in provided documents.", citations=[], confidence=0.0, used_chunks=[])
    # Conservative MVP: select the single best chunk as evidence and quote a sentence
    top = results[0]
    text = top["snippet"] if top["snippet"] else ""
    # We must return exact quote substring from the chunk text; ensure snippet exists in chunk text
    quote = text[:200]
    citations = [
        Citation(
            chunk_id=top["chunk_id"],
            document_id=top["document_id"],
            filename=top["filename"],
            page_number=top["page_number"],
            section=top["section"],
            quote=quote,
            char_start=0,
            char_end=min(len(quote), 200),
        )
    ]
    return QAResponse(
        answer="Insufficient information in provided documents." if not quote else quote,
        citations=citations if quote else [],
        confidence=top["confidence"] if quote else 0.0,
        used_chunks=[top],
    )