from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import StreamingResponse
import json
import asyncio

router = APIRouter()

@router.post("/upload")
async def upload_document(background_tasks: BackgroundTasks, request: Request):
    doc_id = "test_doc_id"
    file_path = "test.pdf"
    
    pipeline = request.app.state.pipeline
    background_tasks.add_task(pipeline.ingest_file, file_path, doc_id, "user_1")
    
    return {"doc_id": doc_id, "status": "ingesting"}

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
