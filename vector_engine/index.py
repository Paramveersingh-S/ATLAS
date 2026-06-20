import numpy as np
from core.turboquant import TurboQuantCompressor
from .storage import TQVSWriter, TQVSReader
from .search import search_compressed_index, SearchResult

class TurboQuantVectorIndex:
    def __init__(self, index_dir: str, d: int = 384, bits: int = 3):
        self.index_dir = index_dir
        self.d = d
        self.bits = bits
        self.compressor = TurboQuantCompressor(d, bits=bits)
        self.writer = TQVSWriter(index_dir)
        self.reader = TQVSReader(index_dir)
        
    def add(self, vector: np.ndarray, chunk_id: str, doc_id: str):
        """Compress and append vector to memory-mapped storage"""
        tqv = self.compressor.compress(vector)
        self.writer.append(tqv, chunk_id, doc_id)
        
    def search(self, query: np.ndarray, k: int = 5) -> list[SearchResult]:
        """Perform 2-phase retrieval on compressed index"""
        # Reload reader to catch any recent appends across async boundaries
        self.reader = TQVSReader(self.index_dir)
        return search_compressed_index(self.reader, self.compressor, query, k)
