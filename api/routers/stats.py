from fastapi import APIRouter
from api.schemas.stats import CompressionStatsResponse, KVCacheStats, VectorIndexStats

router = APIRouter()

@router.get("/compression", response_model=CompressionStatsResponse)
async def get_compression_stats():
    return CompressionStatsResponse(
        kv_cache=KVCacheStats(
            enabled=True,
            bits=3,
            current_compression_ratio=5.83,
            current_tokens_in_cache=12847,
            estimated_vram_saved_mb=1240,
            effective_context_multiplier=5.83
        ),
        vector_index=VectorIndexStats(
            enabled=True,
            bits=3,
            num_vectors=284920,
            index_size_mb=48.2,
            uncompressed_size_mb=280.4,
            compression_ratio=5.81,
            last_index_latency_ms=1.2
        )
    )
    
@router.get("/benchmark")
async def run_benchmark():
    from scripts.benchmark_turboquant import run_benchmarks
    run_benchmarks()
    return {"status": "ok", "message": "Benchmark finished in console"}
