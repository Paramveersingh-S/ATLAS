import pytest
import torch
from kv_engine.kv_cache import TurboQuantKVCache

def test_kv_cache():
    cache = TurboQuantKVCache(d_head=128, num_heads=4)
    k = torch.randn(4, 10, 128)
    v = torch.randn(4, 10, 128)
    cache.update(k, v, 0)
    
    query = torch.randn(128)
    out = cache.compute_attention(query, 0)
    assert out.shape == (128,)
    assert cache.memory_bytes() > 0
