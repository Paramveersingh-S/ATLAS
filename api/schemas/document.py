from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class DocumentBase(BaseModel):
    title: str
    file_type: str

class DocumentCreate(DocumentBase):
    user_id: str

class DocumentResponse(DocumentBase):
    id: str
    page_count: Optional[int]
    chunk_count: int
    status: str
    metadata_json: Dict[str, Any]

class ChunkResponse(BaseModel):
    id: str
    text: str
    token_count: int
    page_number: Optional[int]
