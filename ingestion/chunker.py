import numpy as np
from dataclasses import dataclass
import nltk
from sentence_transformers import SentenceTransformer
from typing import List

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    token_count: int
    start_char: int
    end_char: int
    page_number: int = 1

class SemanticChunker:
    def __init__(self, embedding_model_path: str = "all-MiniLM-L6-v2", min_tokens=200, max_tokens=800, breakpoint_threshold=0.4):
        self.model = SentenceTransformer(embedding_model_path)
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens
        self.breakpoint_threshold = breakpoint_threshold
        
    def chunk(self, text: str, doc_id: str) -> List[Chunk]:
        sentences = nltk.sent_tokenize(text)
        if not sentences: return []
        
        embeddings = self.model.encode(sentences)
        
        similarities = []
        for i in range(len(embeddings)-1):
            sim = np.dot(embeddings[i], embeddings[i+1]) / (np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[i+1]) + 1e-8)
            similarities.append(sim)
            
        chunks = []
        current_chunk_sentences = [sentences[0]]
        current_char_start = 0
        current_text_len = len(sentences[0])
        
        for i, sim in enumerate(similarities):
            current_tokens = current_text_len // 4 
            
            if sim < self.breakpoint_threshold and current_tokens >= self.min_tokens:
                chunk_text = " ".join(current_chunk_sentences)
                chunks.append(Chunk(f"{doc_id}_{len(chunks)}", doc_id, chunk_text, len(chunk_text)//4, current_char_start, current_char_start + len(chunk_text)))
                current_char_start += len(chunk_text) + 1
                current_chunk_sentences = []
                current_text_len = 0
            elif current_tokens >= self.max_tokens:
                chunk_text = " ".join(current_chunk_sentences)
                chunks.append(Chunk(f"{doc_id}_{len(chunks)}", doc_id, chunk_text, len(chunk_text)//4, current_char_start, current_char_start + len(chunk_text)))
                current_char_start += len(chunk_text) + 1
                current_chunk_sentences = []
                current_text_len = 0
                
            current_chunk_sentences.append(sentences[i+1])
            current_text_len += len(sentences[i+1]) + 1
            
        if current_chunk_sentences:
            chunk_text = " ".join(current_chunk_sentences)
            chunks.append(Chunk(f"{doc_id}_{len(chunks)}", doc_id, chunk_text, len(chunk_text)//4, current_char_start, current_char_start + len(chunk_text)))
            
        return chunks
