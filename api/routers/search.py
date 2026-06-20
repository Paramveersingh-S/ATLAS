from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    top_k: int = 10
    filter_doc_ids: List[str] = []
    min_score: float = 0.6

@router.post("/semantic")
async def search_semantic(req: SearchRequest):
    return {"results": []}

@router.post("/hybrid")
async def search_hybrid(req: SearchRequest):
    return {"results": []}
