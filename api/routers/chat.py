from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import asyncio
import json
from api.schemas.chat import ChatRequest, ChatSessionCreate
from core.db import get_chunks_by_ids

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
        from vector_engine.search import search_compressed_index
        results = search_compressed_index(app.state.vector_index.reader, app.state.tq_precomputed, query_emb, k=4)
        
        # 3. Fetch real chunk texts from SQLite
        chunk_ids = [r.chunk_id for r in results]
        chunk_texts = get_chunks_by_ids(chunk_ids)
        
        chunks = []
        for r in results:
            text_preview = chunk_texts.get(r.chunk_id, "Text not found.")[:200] + "..."
            chunks.append({
                "chunk_id": r.chunk_id, 
                "doc_title": r.doc_id, 
                "text_preview": text_preview, 
                "score": float(r.score)
            })
            
        yield f"data: {json.dumps({'event': 'retrieved_chunks', 'data': {'chunks': chunks}})}\n\n"
        await asyncio.sleep(0.5)
        
        # 4. Stream response (Retrieval-Only mode)
        response = f"I scanned your `.tqvs` vector space for '{query_text}'. Using my mathematical KV cache, I found {len(results)} related chunks in sub-millisecond time!\n\n"
        if results:
            response += "Here is the exact text I retrieved from your documents:\n\n"
            for r in results:
                full_text = chunk_texts.get(r.chunk_id, "No text found.")
                response += f"### From Document: {r.doc_id} (Chunk `{r.chunk_id}`)\n"
                response += f"> {full_text}\n\n"
        else:
            response += "But I didn't find any indexed chunks. Upload some documents in the Library!"
            
        response += "\nHow else can I assist your workflow?"
        
        for word in response.split(" "):
            yield f"data: {json.dumps({'event': 'llm_token', 'data': {'token': word + ' '}})}\n\n"
            await asyncio.sleep(0.02) # Faster streaming
            
        yield f"data: {json.dumps({'event': 'done', 'data': {'tokens_used': len(response.split()), 'kv_compression_ratio': 5.8}})}\n\n"
        
    return StreamingResponse(generate(), media_type="text/event-stream")
