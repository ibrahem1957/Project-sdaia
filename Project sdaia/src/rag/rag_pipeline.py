from src.rag.chunker import chunk_text
from src.rag.embeddings import OpenRouterEmbeddings
from src.rag.vector_store import VectorStore


class RAGPipeline:
    def __init__(self):
        self.embedder = OpenRouterEmbeddings()
        self.store = VectorStore()

    def build_index(self, text: str):
        chunks = chunk_text(text)

        for chunk in chunks:
            vector = self.embedder.embed(chunk)
            self.store.add(vector, chunk)

    def retrieve(self, query: str):
        query_vector = self.embedder.embed(query)
        return self.store.search(query_vector)
        