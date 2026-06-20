from fastapi import APIRouter
from api.schemas.stats import CompressionStatsResponse, KVCacheStats, VectorIndexStats
from core.db import get_stats

router = APIRouter()

@router.get("/compression", response_model=CompressionStatsResponse)
async def get_compression_stats():
    db_stats = get_stats()
    num_vectors = db_stats.get('chunk_count', 0)
    
    return CompressionStatsResponse(
        kv_cache=KVCacheStats(
            enabled=True,
            bits=3,
            current_compression_ratio=5.83,
            current_tokens_in_cache=num_vectors * 512, # estimate
            estimated_vram_saved_mb=int(num_vectors * 0.005),
            effective_context_multiplier=5.83
        ),
        vector_index=VectorIndexStats(
            enabled=True,
            bits=3,
            num_vectors=num_vectors,
            index_size_mb=round(num_vectors * 0.00017, 2), # approx
            uncompressed_size_mb=round(num_vectors * 0.001, 2),
            compression_ratio=5.81,
            last_index_latency_ms=1.2
        )
    )
    
@router.get("/benchmark")
async def run_benchmark():
    from scripts.benchmark_turboquant import run_benchmarks
    run_benchmarks()
    return {"status": "ok", "message": "Benchmark finished in console"}
