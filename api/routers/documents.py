from fastapi import APIRouter, Request, BackgroundTasks, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import json
import asyncio
import os
import uuid
import shutil
from core.db import insert_document, get_all_documents

router = APIRouter()

@router.post("/upload")
async def upload_document(background_tasks: BackgroundTasks, request: Request, file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())
    upload_dir = "data/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{doc_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    doc = {
        "id": doc_id,
        "title": file.filename,
        "file_type": file.filename.split('.')[-1].lower() if '.' in file.filename else 'unknown',
        "source_path": file_path,
        "page_count": 1,
        "status": "ingesting"
    }
    insert_document(doc)
    
    pipeline = request.app.state.pipeline
    background_tasks.add_task(pipeline.ingest_file, file_path, doc_id, "user_1")
    
    return {"doc_id": doc_id, "status": "ingesting"}

@router.get("")
async def list_documents():
    docs = get_all_documents()
    return {"documents": docs}

@router.get("/ingestion/{job_id}")
async def stream_ingestion_progress(job_id: str, request: Request):
    async def event_generator():
        pipeline = request.app.state.pipeline
        if job_id not in pipeline.job_queues:
            pipeline.job_queues[job_id] = asyncio.Queue()
            
        queue = pipeline.job_queues[job_id]
        
        while True:
            if await request.is_disconnected():
                break
            try:
                event = await asyncio.wait_for(queue.get(), timeout=30.0)
                yield f"data: {json.dumps(event)}\n\n"
                if event.get('event') in ('done', 'error'):
                    break
            except asyncio.TimeoutError:
                yield ": heartbeat\n\n"
                
    return StreamingResponse(event_generator(), media_type="text/event-stream")
