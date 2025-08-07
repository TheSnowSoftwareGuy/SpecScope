from fastapi import APIRouter, HTTPException
from typing import List
from ....models.query import SearchQuery, SearchResult, QARequest, QAResponse
from ....services.search_service import search as search_service
from ....services.ai_service import answer_question

router = APIRouter(prefix="", tags=["search"])

@router.post("/search", response_model=List[SearchResult])
async def search(q: SearchQuery):
    results = await search_service(q.query, q.top_k, q.alpha, q.filters)
    return results

@router.post("/qa", response_model=QAResponse)
async def qa(req: QARequest):
    resp = await answer_question(req)
    return resp
