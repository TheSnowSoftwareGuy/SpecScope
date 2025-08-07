import asyncio
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
import fitz  # PyMuPDF
import re
from ..utils.patterns import CSI_DIVISION_REGEX, ADDENDA_REGEX

@dataclass
class ExtractedPage:
    page_number: int
    text: str
    width: float
    height: float
    blocks: List[Dict[str, Any]]

def _detect_section_header(text: str) -> str:
    # Simple heuristic: first matching division or section-like header within first 500 chars
    head = text[:500]
    m = CSI_DIVISION_REGEX.search(head)
    if m:
        return m.group(0)
    # Fallback: uppercase lines that look like headers
    lines = [ln.strip() for ln in head.splitlines() if ln.strip()]
    for ln in lines[:5]:
        if ln.isupper() and len(ln) < 120:
            return ln
    return ""

async def extract_pdf(filepath: str, max_pages: int | None = None) -> Tuple[List[ExtractedPage], List[str]]:
    """
    Extract text, dimensions, and blocks from a PDF. Returns (pages, sections_per_page)
    """
    pages: List[ExtractedPage] = []
    sections: List[str] = []

    def _extract_sync() -> Tuple[List[ExtractedPage], List[str]]:
        doc = fitz.open(filepath)
        try:
            total = len(doc)
            if max_pages:
                total = min(total, max_pages)
            for i in range(total):
                page = doc.load_page(i)
                text = page.get_text("text")
                blocks = page.get_text("blocks")
                width, height = page.rect.width, page.rect.height
                pages.append(
                    ExtractedPage(
                        page_number=i + 1,
                        text=text,
                        width=width,
                        height=height,
                        blocks=[{"bbox": b[:4], "text": b[4]} for b in blocks],
                    )
                )
                sections.append(_detect_section_header(text))
        finally:
            doc.close()
        return pages, sections

    return await asyncio.to_thread(_extract_sync)