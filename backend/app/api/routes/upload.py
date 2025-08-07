from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any
import tempfile
from ....utils.validators import is_allowed_pdf, safe_filename
from ....services.document_service import store_upload, process_pdf, list_documents, get_page_text

router = APIRouter(prefix="", tags=["upload"])

@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)) -> List[Dict[str, Any]]:
    results = []
    for f in files:
        data = await f.read()
        if not is_allowed_pdf(f.filename, f.content_type or "application/pdf", len(data)):
            raise HTTPException(status_code=400, detail=f"Invalid file: {f.filename}")
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        stored_path = store_upload(tmp_path, safe_filename(f.filename))
        res = await process_pdf(stored_path, safe_filename(f.filename))
        results.append(res)
    return results

@router.get("/documents")
async def documents() -> List[Dict[str, Any]]:
    return list_documents()

@router.get("/documents/{doc_id}/pages/{page_number}")
async def document_page(doc_id: str, page_number: int) -> Dict[str, Any]:
    return get_page_text(doc_id, page_number)
