import os
import torch
import numpy as np
from scipy.stats import beta as beta_dist
from sklearn.cluster import KMeans

def build_rotation_matrix(d: int, seed: int = 42) -> torch.Tensor:
    """
    Generate a fixed random orthogonal matrix via QR decomposition.
    MUST use the same seed everywhere — stored to disk on first run.
    """
    torch.manual_seed(seed)
    G = torch.randn(d, d)
    Q, _ = torch.linalg.qr(G)
    return Q  # orthogonal: Q^T @ Q = I

def build_sign_matrix(m: int, d: int, seed: int = 123) -> torch.Tensor:
    """
    Generate the QJL random sign matrix S ∈ {-1, +1}^(m×d).
    m = d // 4 is the recommended sketch dimension.
    """
    torch.manual_seed(seed)
    return (2 * torch.bernoulli(torch.full((m, d), 0.5)) - 1)

def compute_beta_centroids(level: int, bits: int) -> np.ndarray:
    """
    Lloyd-Max quantizer centroids for Beta(k/2, 1/2) distribution.
    k = d - level (dimension at each recursion level).
    Precompute for all (level, bits) pairs and cache to disk.
    """
    k = max(1, level)
    a, b = k / 2, 0.5
    num_centroids = 2 ** bits
    # Use k-means on Beta distribution samples
    samples = beta_dist.rvs(a, b, size=100_000)
    km = KMeans(n_clusters=num_centroids, n_init=10, random_state=42)
    km.fit(samples.reshape(-1, 1))
    return np.sort(km.cluster_centers_.flatten())

class TurboQuantPrecomputed:
    """Singleton — load once at startup."""
    def __init__(self, d: int, bits: int = 3, cache_dir: str = "./data/cache/"):
        os.makedirs(cache_dir, exist_ok=True)
        cache_path = os.path.join(cache_dir, f"tq_precomputed_d{d}_b{bits}.pt")
        
        if os.path.exists(cache_path):
            print(f"Loading precomputed TurboQuant tables for d={d}, bits={bits} from {cache_path}")
            data = torch.load(cache_path)
        else:
            print(f"Building TurboQuant precomputed tables for d={d}, bits={bits}...")
            data = {
                'R': build_rotation_matrix(d),
                'S': build_sign_matrix(d // 4, d),
                'centroids': {lv: compute_beta_centroids(lv, bits-1) for lv in range(d)},
            }
            torch.save(data, cache_path)
            print(f"Saved precomputed tables to {cache_path}")
            
        self.R = data['R']
        self.S = data['S']
        self.centroids = data['centroids']
        self.d = d
        self.bits = bits
