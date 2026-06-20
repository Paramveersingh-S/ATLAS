from pydantic import BaseModel

class KVCacheStats(BaseModel):
    enabled: bool
    bits: int
    current_compression_ratio: float
    current_tokens_in_cache: int
    estimated_vram_saved_mb: float
    effective_context_multiplier: float

class VectorIndexStats(BaseModel):
    enabled: bool
    bits: int
    num_vectors: int
    index_size_mb: float
    uncompressed_size_mb: float
    compression_ratio: float
    last_index_latency_ms: float

class CompressionStatsResponse(BaseModel):
    kv_cache: KVCacheStats
    vector_index: VectorIndexStats
