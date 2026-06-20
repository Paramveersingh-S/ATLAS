from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    ATLAS_HOST: str = "0.0.0.0"
    ATLAS_PORT: int = 8000
    SECRET_KEY: str = "supersecret"
    DEBUG: bool = False
    
    DATABASE_PATH: str = "./data/atlas.db"
    INDEX_PATH: str = "./data/index/"
    DOCUMENT_STORE_PATH: str = "./data/documents/"
    CACHE_PATH: str = "./data/cache/"
    
    LLM_MODEL_PATH: str = "./models/Llama-3.2-3B-Instruct.Q8_0.gguf"
    EMBEDDING_MODEL_PATH: str = "./models/nomic-embed-text-v1.5"
    EMBEDDING_DIM: int = 768
    RERANKER_MODEL_PATH: str = "./models/cross-encoder-ms-marco-MiniLM-L-6-v2"
    
    VLLM_PORT: int = 8001
    VLLM_GPU_MEMORY_UTIL: float = 0.85
    USE_VLLM: bool = True
    
    TQ_BITS: int = 3
    TQ_BITS_K: int = 3
    TQ_BITS_V: int = 3
    ENABLE_TQ_KV_CACHE: bool = True
    ENABLE_TQ_VECTOR_SEARCH: bool = True
    TQ_PRECOMPUTE_SEED: int = 42
    
    CHUNK_MIN_TOKENS: int = 200
    CHUNK_MAX_TOKENS: int = 800
    CHUNK_OVERLAP_TOKENS: int = 50
    
    RETRIEVAL_TOP_K: int = 20
    RETRIEVAL_CANDIDATES: int = 200
    RETRIEVAL_MIN_SCORE: float = 0.5
    HYBRID_BM25_WEIGHT: float = 0.3
    ENABLE_RERANKER: bool = True
    
    ENCRYPT_DOCUMENT_STORE: bool = False
    DOCUMENT_STORE_KEY: Optional[str] = None
    JWT_EXPIRE_HOURS: int = 168

    class Config:
        env_file = ".env"

settings = Settings()
