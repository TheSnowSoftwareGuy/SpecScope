import os
import io
import fitz
import pytest
from backend.app.core.pdf_processor import extract_pdf

def create_sample_pdf(path: str):
    doc = fitz.open()
    page = doc.new_page()
    text = "DIVISION 01 — GENERAL REQUIREMENTS\nLiquidated damages: $2,000 per calendar day.\nContractor shall submit shop drawings."
    page.insert_text((72, 72), text)
    page2 = doc.new_page()
    page2.insert_text((72, 72), "ADDENDUM 1\nSubmittals due 14 days after award.")
    doc.save(path)
    doc.close()

@pytest.mark.asyncio
async def test_extract_pdf(tmp_path):
    p = tmp_path / "sample.pdf"
    create_sample_pdf(str(p))
    pages, sections = await extract_pdf(str(p))
    assert len(pages) == 2
    assert any("DIVISION" in (s or "") for s in sections)
    assert "Liquidated damages" in pages[0].text
    assert pages[0].width > 0 and pages[0].height > 0
