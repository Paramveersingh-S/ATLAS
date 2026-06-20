import torch
import numpy as np
from dataclasses import dataclass
from .precompute import TurboQuantPrecomputed
from .polar_quant import polarquant_compress, polarquant_decompress
from .qjl import qjl_compress_residual, qjl_estimate_inner_product
from .bit_packing import pack_indices, unpack_indices

@dataclass
class TurboQuantVector:
    norm: float
    r_final: float
    angle_indices: np.ndarray  # packed bytes
    qjl_sketch: np.ndarray     # packed int8
    d: int
    bits: int
    
    def memory_bytes(self) -> int:
        """Compute actual memory usage."""
        polar_bits = self.bits - 1
        angle_bytes = int(np.ceil((self.d - 1) * polar_bits / 8))
        sketch_bytes = len(self.qjl_sketch)
        overhead_bytes = 4
        return angle_bytes + sketch_bytes + overhead_bytes

class TurboQuantCompressor:
    def __init__(self, d: int, bits: int = 3, cache_dir: str = "./data/cache/"):
        self.precomputed = TurboQuantPrecomputed(d, bits, cache_dir)
        self.d = d
        self.bits = bits
        
    def compress(self, x: torch.Tensor, use_qjl: bool = True) -> TurboQuantVector:
        """Compress a single vector x to TurboQuantVector."""
        pq = polarquant_compress(x, self.precomputed, self.bits)
        packed_angles = pack_indices(pq['angle_indices'], self.bits - 1)
        
        qjl_sketch = np.zeros(0, dtype=np.int8)
        if use_qjl:
            x_recon_norm = polarquant_decompress(pq, self.precomputed, return_normalized=True)
            x_orig_norm = x / (pq['norm'] + 1e-8)
            sketch = qjl_compress_residual(x_orig_norm, x_recon_norm, self.precomputed.S)
            qjl_sketch = sketch.numpy()
            
        return TurboQuantVector(
            norm=pq['norm'],
            r_final=pq['r_final'],
            angle_indices=packed_angles,
            qjl_sketch=qjl_sketch,
            d=self.d,
            bits=self.bits
        )
        
    def decompress(self, tqv: TurboQuantVector) -> torch.Tensor:
        """Reconstruct approximate x from TurboQuantVector."""
        unpacked_angles = unpack_indices(tqv.angle_indices, self.d - 1, self.bits - 1)
        pq = {
            'norm': tqv.norm,
            'angle_indices': unpacked_angles,
            'r_final': tqv.r_final,
            'd': tqv.d,
            'bits': tqv.bits
        }
        return polarquant_decompress(pq, self.precomputed, return_normalized=False)
        
    def estimate_inner_product(self, query: torch.Tensor, tqv: TurboQuantVector) -> float:
        """Estimate dot(query, x) without full decompression."""
        unpacked_angles = unpack_indices(tqv.angle_indices, self.d - 1, self.bits - 1)
        pq = {
            'norm': tqv.norm,
            'angle_indices': unpacked_angles,
            'r_final': tqv.r_final,
            'd': tqv.d,
            'bits': tqv.bits
        }
        polar_recon_norm = polarquant_decompress(pq, self.precomputed, return_normalized=True)
        
        if len(tqv.qjl_sketch) > 0:
            sketch = torch.from_numpy(tqv.qjl_sketch)
            return qjl_estimate_inner_product(query, polar_recon_norm, sketch, self.precomputed.S, tqv.norm)
        else:
            return torch.dot(query, polar_recon_norm).item() * tqv.norm
        
    def compress_batch(self, X: torch.Tensor, use_qjl: bool = True) -> list[TurboQuantVector]:
        """Compress a batch of vectors efficiently."""
        # A basic implementation for batch compression
        # For true efficiency, polarquant_compress should be vectorized
        return [self.compress(X[i], use_qjl=use_qjl) for i in range(X.shape[0])]
