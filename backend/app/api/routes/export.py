from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse
from ....models.query import ExportRequest
from io import StringIO
import csv

router = APIRouter(prefix="", tags=["export"])

@router.post("/export")
async def export(req: ExportRequest):
    # MVP: return empty CSV header or error if type unsupported
    if req.type == "csv":
        stream = StringIO()
        writer = csv.writer(stream)
        writer.writerow(["query/claim", "answer/left", "right", "document", "page", "section", "confidence", "source_text"])
        stream.seek(0)
        return StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    return PlainTextResponse("PDF export not implemented in MVP step", status_code=501)
