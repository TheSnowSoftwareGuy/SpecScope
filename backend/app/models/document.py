from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

class DocumentIn(BaseModel):
    filename: str
    metadata: Optional[Dict[str, Any]] = None

class Document(BaseModel):
    id: str
    filename: str
    pages_count: int
    uploaded_at: datetime

class Page(BaseModel):
    document_id: str
    page_number: int
    text: str
    blocks: Optional[list] = None
    dimensions: Optional[dict] = None

class Chunk(BaseModel):
    id: str
    document_id: str
    page_number: int
    section: Optional[str]
    text: str
    char_start: int
    char_end: int
    bbox: Optional[dict] = None
    hash: str
