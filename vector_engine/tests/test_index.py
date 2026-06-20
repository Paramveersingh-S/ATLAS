import pytest
import numpy as np
from vector_engine.index import TurboQuantVectorIndex

def test_index_add_search(tmp_path):
    index = TurboQuantVectorIndex(d=128, bits=3, index_path=str(tmp_path))
    vec = np.random.randn(128)
    index.add(vec, "chunk_1", "doc_1")
    
    results = index.search(vec, top_k=1)
    assert len(results) == 1
    assert results[0].chunk_id == "chunk_1"
