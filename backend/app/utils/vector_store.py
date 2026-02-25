import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import pickle


class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.text_chunks = []
        self.index_path = "faiss_index.bin"
        self.chunks_path = "chunks.pkl"
        self.load_index()


    def build_index(self, chunks: list[str]):
        self.text_chunks = chunks

        embeddings = self.model.encode(
            chunks,
            batch_size=128,   # Increase batch size
            show_progress_bar=True,
            convert_to_numpy=True
            )

        embeddings = np.array(embeddings).astype("float32")

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)
        faiss.write_index(self.index, self.index_path)
        with open(self.chunks_path, "wb") as f:
            pickle.dump(self.text_chunks, f)
        
    def load_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.chunks_path):
            self.index = faiss.read_index(self.index_path)

            with open(self.chunks_path, "rb") as f:
                self.text_chunks = pickle.load(f)

            return True

        return False


    def search(self, query: str, k: int = 5) -> list[str]:
        if self.index is None:
            raise ValueError("Index not loaded or built")

        query_embedding = self.model.encode([query], convert_to_numpy=True)
        query_embedding = np.array(query_embedding).astype("float32")

        _, indices = self.index.search(query_embedding, k)

        return [self.text_chunks[i] for i in indices[0]]

