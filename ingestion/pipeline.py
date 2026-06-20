import asyncio
from typing import Dict, Any

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
            
            if file_path.endswith('.pdf'):
                from .parsers.pdf_parser import parse_pdf
                parsed = parse_pdf(file_path)
            else:
                # Placeholder for other parsers
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                parsed = {"text": text, "metadata": {"page_count": 1}}
                
            await self.emit_progress(doc_id, "parse_done", {"pages": parsed["metadata"].get("page_count", 1)})
            
            from .chunker import SemanticChunker
            chunker = SemanticChunker("all-MiniLM-L6-v2")
            chunks = chunker.chunk(parsed["text"], doc_id)
            await self.emit_progress(doc_id, "chunk_progress", {"total": len(chunks)})
            
            from .dedup import is_near_duplicate
            existing_mhs = []
            
            for i, chunk in enumerate(chunks):
                if is_near_duplicate(chunk.text, existing_mhs):
                    continue
                
                emb = self.embedder.encode(chunk.text)
                self.vector_index.add(emb, chunk.chunk_id, doc_id)
                await self.emit_progress(doc_id, "embed_progress", {"done": i+1, "total": len(chunks)})
                
            await self.emit_progress(doc_id, "done", {"chunk_count": len(chunks)})
            return IngestionResult(job_id=doc_id, status="success")
        except Exception as e:
            await self.emit_progress(doc_id, "error", {"message": str(e)})
            return IngestionResult(job_id=doc_id, status="error", error=str(e))
