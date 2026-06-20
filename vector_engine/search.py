import numpy as np
from dataclasses import dataclass
from core.turboquant import TurboQuantCompressor

@dataclass
class SearchResult:
    chunk_id: str
    doc_id: str
    score: float

def search_compressed_index(reader, compressor: TurboQuantCompressor, query: np.ndarray, top_k: int = 5) -> list[SearchResult]:
    if reader.num_vectors == 0:
        return []
        
    scores = []
    # Two-Phase MIPS Ranking:
    # Phase 1: Fast QJL Sketch inner product estimation (skipped in MVP for exact correctness)
    # Phase 2: Exact Polar Quantization decompression for top candidates
    
    for i in range(reader.num_vectors):
        if reader.is_deleted(i):
            continue
        tqv = reader.get(i)
        # Decompress back to continuous vector
        decompressed = compressor.decompress(tqv)
        
        # Calculate dot product similarity
        score = float(np.dot(query, decompressed))
        chunk_id, doc_id = reader.get_metadata(i)
        scores.append((score, chunk_id, doc_id))
        
    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    results = []
    for score, chunk_id, doc_id in scores[:top_k]:
        results.append(SearchResult(chunk_id=chunk_id, doc_id=doc_id, score=score))
        
    return results
