import numpy as np

def pack_indices(indices: list, bits_per_index: int) -> np.ndarray:
    """Pack variable-bit-width integers into a compact byte array."""
    total_bits = len(indices) * bits_per_index
    total_bytes = int(np.ceil(total_bits / 8))
    packed = np.zeros(total_bytes, dtype=np.uint8)
    
    bit_pos = 0
    for idx in indices:
        byte_pos = bit_pos // 8
        bit_offset = bit_pos % 8
        # Write idx into packed at position bit_pos
        packed[byte_pos] |= (idx << bit_offset) & 0xFF
        if bit_offset + bits_per_index > 8:
            packed[byte_pos + 1] |= (idx >> (8 - bit_offset)) & 0xFF
        bit_pos += bits_per_index
    
    return packed

def unpack_indices(packed: np.ndarray, count: int, bits_per_index: int) -> list:
    """Reverse of pack_indices."""
    indices = []
    mask = (1 << bits_per_index) - 1
    bit_pos = 0
    for _ in range(count):
        byte_pos = bit_pos // 8
        bit_offset = bit_pos % 8
        val = (int(packed[byte_pos]) >> bit_offset)
        if bit_offset + bits_per_index > 8 and byte_pos + 1 < len(packed):
            val |= (int(packed[byte_pos + 1]) << (8 - bit_offset))
        indices.append(val & mask)
        bit_pos += bits_per_index
    return indices
