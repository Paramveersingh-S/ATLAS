from datasketch import MinHash

def is_near_duplicate(new_chunk_text: str, existing_minhashes: list, threshold: float = 0.92) -> bool:
    """
    Use MinHash LSH for approximate duplicate detection.
    """
    m = MinHash(num_perm=128)
    for word in new_chunk_text.lower().split():
        m.update(word.encode('utf-8'))
        
    for ex_m in existing_minhashes:
        if m.jaccard(ex_m) >= threshold:
            return True
            
    existing_minhashes.append(m)
    return False
