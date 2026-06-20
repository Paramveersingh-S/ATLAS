import time
import torch
from core.turboquant import TurboQuantCompressor

def run_benchmarks():
    print("Running TurboQuant Benchmarks...")
    d = 768
    bits = 3
    compressor = TurboQuantCompressor(d, bits)
    
    # 1. Compress time
    x = torch.randn(d)
    start = time.perf_counter()
    tqv = compressor.compress(x)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"Single vector compress (d={d}): {elapsed:.3f} ms")
    
    # 2. Decompress time
    start = time.perf_counter()
    x_recon = compressor.decompress(tqv)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"Single vector decompress (d={d}): {elapsed:.3f} ms")
    
    # 3. Inner product estimation
    query = torch.randn(d)
    start = time.perf_counter()
    est = compressor.estimate_inner_product(query, tqv)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"Inner product estimation (d={d}): {elapsed:.3f} ms")
    
    # 4. Compression ratio
    fp16_bytes = d * 2
    tq_bytes = tqv.memory_bytes()
    ratio = fp16_bytes / tq_bytes
    print(f"Compression ratio (FP16 baseline): {ratio:.2f}x")

if __name__ == "__main__":
    run_benchmarks()
