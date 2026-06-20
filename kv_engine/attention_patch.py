import torch.nn as nn
from .kv_cache import TurboQuantKVCache

def make_tq_forward(module, original_forward):
    def tq_forward(hidden_states, *args, **kwargs):
        # Placeholder for deep integration into model forward pass
        # This intercepts the forward call to inject our compressed KV logic.
        return original_forward(hidden_states, *args, **kwargs)
    return tq_forward

def patch_model_attention(model: nn.Module, bits_k: int = 3, bits_v: int = 3):
    """
    Walk the model's module tree, find all self-attention layers,
    and replace their KV cache with TurboQuantKVCache.
    """
    for name, module in model.named_modules():
        if hasattr(module, 'k_proj') and hasattr(module, 'v_proj'):
            module._tq_kv_cache = TurboQuantKVCache(
                d_head=module.head_dim if hasattr(module, 'head_dim') else 128,
                num_heads=module.num_heads if hasattr(module, 'num_heads') else 32,
                bits_k=bits_k,
                bits_v=bits_v
            )
            original_forward = module.forward
            module.forward = make_tq_forward(module, original_forward)
            
    return model
