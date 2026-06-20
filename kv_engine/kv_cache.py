import torch
import math
from core.turboquant import TurboQuantCompressor, TurboQuantVector

class TurboQuantKVCache:
    def __init__(self, d_head: int, num_heads: int, bits_k: int = 3, bits_v: int = 3):
        self.compressor_k = TurboQuantCompressor(d_head, bits_k)
        self.compressor_v = TurboQuantCompressor(d_head, bits_v)
        self.compressed_k: list[list[TurboQuantVector]] = [[] for _ in range(num_heads)]
        self.compressed_v: list[list[TurboQuantVector]] = [[] for _ in range(num_heads)]
        self.num_heads = num_heads
        
    def update(self, new_k: torch.Tensor, new_v: torch.Tensor, layer_idx: int):
        """
        new_k: shape (num_heads, seq_len, d_head)
        new_v: shape (num_heads, seq_len, d_head)
        """
        for head in range(self.num_heads):
            for t in range(new_k.shape[1]):
                k_vec = new_k[head, t, :]
                v_vec = new_v[head, t, :]
                self.compressed_k[head].append(self.compressor_k.compress(k_vec, use_qjl=True))
                self.compressed_v[head].append(self.compressor_v.compress(v_vec, use_qjl=False))
                
    def compute_attention(self, query: torch.Tensor, head: int) -> torch.Tensor:
        """
        Compute attention output for a single head using compressed K and V.
        query: shape (d_head,)
        """
        scores = []
        for k_compressed in self.compressed_k[head]:
            score = self.compressor_k.estimate_inner_product(query, k_compressed)
            scores.append(score)
            
        scores = torch.softmax(torch.tensor(scores) / math.sqrt(query.shape[0]), dim=0)
        
        output = torch.zeros_like(query)
        for i, v_compressed in enumerate(self.compressed_v[head]):
            v_recon = self.compressor_v.decompress(v_compressed)
            output += scores[i] * v_recon
            
        return output
        
    def memory_bytes(self) -> int:
        total = 0
        for head in range(self.num_heads):
            for tqv in self.compressed_k[head] + self.compressed_v[head]:
                total += tqv.memory_bytes()
        return total
        
    def compression_ratio(self, baseline_bits: int = 16) -> float:
        if len(self.compressed_k[0]) == 0:
            return 1.0
        uncompressed = self.num_heads * len(self.compressed_k[0]) * 2 * self.compressor_k.d * (baseline_bits / 8)
        mem = self.memory_bytes()
        if mem == 0: return 1.0
        return uncompressed / mem
