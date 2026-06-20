import asyncio
from typing import Dict, Any
import PyPDF2
from core.db import insert_chunks, update_document_status

class IngestionResult:
    def __init__(self, job_id, status, error=None):
        self.job_id = job_id
        self.status = status
        self.error = error

class IngestionPipeline:
    def __init__(self, vector_index, embedder):
        self.vector_index = vector_index
        self.embedder = embedder
        self.job_queues = {}
        
    async def emit_progress(self, job_id: str, event: str, data: Dict[str, Any]):
        if job_id in self.job_queues:
            await self.job_queues[job_id].put({"event": event, "data": data})
            
    async def ingest_file(self, file_path: str, doc_id: str, user_id: str) -> IngestionResult:
        if doc_id not in self.job_queues:
            self.job_queues[doc_id] = asyncio.Queue()
            
        try:
            await self.emit_progress(doc_id, "parse_start", {"filename": file_path})
            
            text = ""
            pages = 1
            if file_path.lower().endswith('.pdf'):
                with open(file_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    pages = len(reader.pages)
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
            else:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                    
            if not text.strip():
                text = "Empty document."
                
            await self.emit_progress(doc_id, "parse_done", {"pages": pages})
            
            from .chunker import SemanticChunker
            chunker = SemanticChunker("all-MiniLM-L6-v2")
            chunks = chunker.chunk(text, doc_id)
            await self.emit_progress(doc_id, "chunk_progress", {"total": len(chunks)})
            
            db_chunks = []
            for i, chunk in enumerate(chunks):
                db_chunks.append({
                    "chunk_id": chunk.chunk_id,
                    "doc_id": doc_id,
                    "text_content": chunk.text,
                    "chunk_index": i
                })
                
                emb = self.embedder.encode(chunk.text)
                self.vector_index.add(emb, chunk.chunk_id, doc_id)
                await self.emit_progress(doc_id, "embed_progress", {"done": i+1, "total": len(chunks)})
                
            insert_chunks(db_chunks)
            update_document_status(doc_id, "Indexed", chunk_count=len(chunks))
            
            await self.emit_progress(doc_id, "done", {"chunk_count": len(chunks)})
            return IngestionResult(job_id=doc_id, status="success")
        except Exception as e:
            update_document_status(doc_id, "Error", chunk_count=0)
            await self.emit_progress(doc_id, "error", {"message": str(e)})
            return IngestionResult(job_id=doc_id, status="error", error=str(e))
