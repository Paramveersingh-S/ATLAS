from fastapi import APIRouter

router = APIRouter()

@router.post("/reindex")
async def reindex_all():
    return {"status": "started"}
