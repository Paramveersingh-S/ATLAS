import torch
import numpy as np

def find_nearest_centroid(value, centroids):
    idx = np.argmin(np.abs(centroids - value))
    return int(idx)

def cartesian_to_recursive_polar(v: torch.Tensor) -> tuple:
    """
    Recursively convert Cartesian coordinates to polar angles.
    At each step, peel off the last coordinate as a polar angle.
    """
    angles = []
    current = v.clone()
    
    while current.shape[0] > 1:
        r = torch.norm(current)
        if r < 1e-10:
            angles.append(0.0)
        else:
            angle = torch.arcsin(current[-1] / r)
            angle_normalized = (angle.item() + np.pi/2) / np.pi  # map to [0,1]
            angles.append(angle_normalized)
        
        # Reduce dimension: project onto (d-1)-sphere
        current = current[:-1] / (torch.norm(current[:-1]) + 1e-10)
    
    r_final = current[0].item()
    return angles[::-1], r_final

def polar_to_cartesian(angles_normalized: list, r_final: float) -> torch.Tensor:
    current = torch.tensor([r_final], dtype=torch.float32)
    
    for angle_norm in angles_normalized:
        angle = angle_norm * np.pi - np.pi/2
        new_val = torch.tensor([np.sin(angle)], dtype=torch.float32)
        current = current * np.cos(angle)
        current = torch.cat([current, new_val])
        
    return current

def polarquant_compress(x: torch.Tensor, precomputed, bits: int = 3) -> dict:
    d = x.shape[0]
    R = precomputed.R
    x_rot = R @ x
    
    norm = torch.norm(x)
    x_normalized = x_rot / (norm + 1e-8)
    
    angles, r_final = cartesian_to_recursive_polar(x_normalized)
    
    quantized_angles = []
    for level, angle in enumerate(angles):
        centroids = precomputed.centroids[level]
        idx = find_nearest_centroid(angle, centroids)
        quantized_angles.append(idx)
        
    return {
        'norm': norm.item(),
        'angle_indices': quantized_angles,
        'r_final': r_final,
        'd': d,
        'bits': bits
    }

def polarquant_decompress(compressed: dict, precomputed, return_normalized=False) -> torch.Tensor:
    angle_indices = compressed['angle_indices']
    
    angles_normalized = []
    for level, idx in enumerate(angle_indices):
        centroids = precomputed.centroids[level]
        angles_normalized.append(centroids[idx])
        
    x_rot_recon_normalized = polar_to_cartesian(angles_normalized, compressed['r_final'])
    
    R_t = precomputed.R.T
    x_recon_normalized = R_t @ x_rot_recon_normalized
    
    if return_normalized:
        return x_recon_normalized
    return x_recon_normalized * compressed['norm']
