import torch
import math

def qjl_compress_residual(x_original: torch.Tensor, 
                           x_reconstructed_polar: torch.Tensor,
                           S: torch.Tensor) -> torch.Tensor:
    """
    x_original: the original vector before PolarQuant
    x_reconstructed_polar: the PolarQuant reconstruction of x
    S: random sign matrix of shape (m, d) where m << d
    Returns: 1-bit sketch of shape (m,) packed as int8
    """
    residual = x_original - x_reconstructed_polar
    sketch = S @ residual
    return torch.sign(sketch).to(torch.int8)

def qjl_estimate_inner_product(query: torch.Tensor,
                                polar_recon: torch.Tensor,
                                qjl_sketch: torch.Tensor,
                                S: torch.Tensor,
                                norm: float) -> float:
    """
    During attention: estimate <query, key> using compressed key.
    query: FP16 query vector
    polar_recon: PolarQuant reconstruction of key (NORMALIZED)
    qjl_sketch: 1-bit QJL sketch of key residual
    S: same sign matrix used during compression
    norm: original L2 norm of key
    """
    term1 = torch.dot(query, polar_recon)
    
    Sq = S.T @ qjl_sketch.float()
    correction = torch.sqrt(torch.tensor(2.0 / math.pi)) * torch.dot(query, Sq / (torch.norm(Sq) + 1e-8))
    
    return (term1 + correction).item() * norm
