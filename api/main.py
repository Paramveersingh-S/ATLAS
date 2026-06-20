from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.precompute import TurboQuantPrecomputed
from vector_engine.index import TurboQuantVectorIndex
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting ATLAS backend...")
    
    d = int(os.getenv("EMBEDDING_DIM", 768))
    bits = int(os.getenv("TQ_BITS", 3))
    
    app.state.tq_precomputed = TurboQuantPrecomputed(d=d, bits=bits)
    app.state.vector_index = TurboQuantVectorIndex(d=d, bits=bits, index_path="./data/index/")
    
    class DummyEmbedder:
        def encode(self, text):
            import numpy as np
            return np.random.randn(d).astype(np.float32)
            
    app.state.embedder = DummyEmbedder()
    
    from ingestion.pipeline import IngestionPipeline
    app.state.pipeline = IngestionPipeline(app.state.vector_index, app.state.embedder)
    
    print("ATLAS ready.")
    yield
    print("Shutting down...")

app = FastAPI(title="ATLAS API", lifespan=lifespan)

# Import routers after app creation to avoid circular imports if routers need app
from .routers import documents
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
