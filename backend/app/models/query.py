from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SearchQuery(BaseModel):
    query: str
    top_k: int = 10
    alpha: float = 0.5
    filters: Optional[Dict[str, Any]] = None  # {doc_ids: [], divisions: []}

class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    page_number: int
    section: Optional[str]
    snippet: str
    highlights: List[str]
    scores: Dict[str, float]
    confidence: float

class QARequest(BaseModel):
    question: str
    top_k: int = 12
    doc_filter: Optional[Dict[str, Any]] = None

class Citation(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    page_number: int
    section: Optional[str]
    quote: str
    char_start: int
    char_end: int

class QAResponse(BaseModel):
    answer: str
    citations: List[Citation]
    confidence: float
    used_chunks: List[Dict[str, Any]]

class ConflictRequest(BaseModel):
    scope: str  # all | filtered
    topic: Optional[str] = None
    doc_filter: Optional[Dict[str, Any]] = None

class ConflictFinding(BaseModel):
    claim: str
    contradicts: str
    citations_left: List[Citation]
    citations_right: List[Citation]
    confidence: float

class ExportRequest(BaseModel):
    type: str  # csv | pdf
    query: Optional[str] = None
    doc_filter: Optional[Dict[str, Any]] = None