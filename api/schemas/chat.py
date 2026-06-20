from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str
    id: Optional[str] = None

class ChatSessionCreate(BaseModel):
    user_id: str

class ChatSessionResponse(BaseModel):
    id: str
    title: Optional[str]
    message_count: int

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
