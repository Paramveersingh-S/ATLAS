from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import asyncio
import json
from api.schemas.chat import ChatRequest, ChatSessionCreate

router = APIRouter()

@router.post("/sessions")
async def create_session(session: ChatSessionCreate):
    return {"session_id": "session_123"}

@router.post("/sessions/{id}/stream")
async def chat_stream(id: str, chat_req: ChatRequest):
    async def generate():
        yield f"data: {json.dumps({'event': 'retrieval_start'})}\n\n"
        await asyncio.sleep(0.5)
        
        chunks = [{"chunk_id": "c1", "doc_title": "Example", "text_preview": "...", "score": 0.95}]
        yield f"data: {json.dumps({'event': 'retrieved_chunks', 'data': {'chunks': chunks}})}\n\n"
        
        response = "This is a streaming response from ATLAS using TurboQuant."
        for word in response.split():
            yield f"data: {json.dumps({'event': 'llm_token', 'data': {'token': word + ' '}})}\n\n"
            await asyncio.sleep(0.1)
            
        yield f"data: {json.dumps({'event': 'done', 'data': {'tokens_used': 100, 'kv_compression_ratio': 5.8}})}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
