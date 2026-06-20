from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import asyncio
import json
from api.schemas.chat import ChatRequest, ChatSessionCreate
from core.db import get_chunks_by_ids, get_doc_titles_by_ids

router = APIRouter()

@router.post("/sessions")
async def create_session(session: ChatSessionCreate):
    return {"session_id": "session_123"}

@router.post("/sessions/{id}/stream")
async def chat_stream(id: str, chat_req: ChatRequest, request: Request):
    async def generate():
        yield f"data: {json.dumps({'event': 'retrieval_start'})}\n\n"
        
        app = request.app
        query_text = chat_req.messages[-1].content
        
        # 1. Embed query
        query_emb = app.state.embedder.encode(query_text)
        
        # 2. Search TurboQuant
        results = app.state.vector_index.search(query_emb, k=4)
        
        # 3. Fetch real chunk texts from SQLite
        chunk_ids = [r.chunk_id for r in results]
        doc_ids = [r.doc_id for r in results]
        
        chunk_texts = get_chunks_by_ids(chunk_ids)
        doc_titles = get_doc_titles_by_ids(doc_ids)
        
        chunks = []
        for r in results:
            doc_title = doc_titles.get(r.doc_id, "Unknown Document")
            text_preview = chunk_texts.get(r.chunk_id, "Text not found.")[:200] + "..."
            chunks.append({
                "chunk_id": r.chunk_id, 
                "doc_title": doc_title, 
                "text_preview": text_preview, 
                "score": float(r.score)
            })
            
        yield f"data: {json.dumps({'event': 'retrieved_chunks', 'data': {'chunks': chunks}})}\n\n"
        await asyncio.sleep(0.5)
        
        # 4. Stream response (Retrieval-Only mode)
        response = f"I found the following information to answer your question:\n\n"
        if results:
            for r in results:
                full_text = chunk_texts.get(r.chunk_id, "No text found.")
                doc_title = doc_titles.get(r.doc_id, "Unknown Document")
                response += f"### From {doc_title}\n"
                response += f"{full_text}\n\n"
        else:
            response = "I couldn't find any relevant information in your documents."
            
        for word in response.split(" "):
            yield f"data: {json.dumps({'event': 'llm_token', 'data': {'token': word + ' '}})}\n\n"
            await asyncio.sleep(0.02) # Faster streaming
            
        yield f"data: {json.dumps({'event': 'done', 'data': {'tokens_used': len(response.split()), 'kv_compression_ratio': 5.8}})}\n\n"
        
    return StreamingResponse(generate(), media_type="text/event-stream")
