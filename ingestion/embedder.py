from sentence_transformers import SentenceTransformer

class LocalEmbedder:
    def __init__(self, model_path: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_path)
        
    def encode(self, texts):
        return self.model.encode(texts)
