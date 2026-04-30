import numpy as np

class VectorStore:
    def __init__(self):
        self.vectors = []
        self.texts = []

    def add(self, vector, text):
        self.vectors.append(vector)
        self.texts.append(text)

    def similarity(self, v1, v2):
        v1 = np.array(v1)
        v2 = np.array(v2)
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def search(self, query_vector, top_k=5):
        scores = []

        print("\n[INFO] Calculating similarity...\n")

        for i, vec in enumerate(self.vectors):
            score = self.similarity(query_vector, vec)

            print(f"[SIMILARITY] chunk {i}: {score:.4f}")

            scores.append((score, self.texts[i]))

        scores.sort(reverse=True, key=lambda x: x[0])

        print("\n[TOP RESULTS]\n")

        for rank, (score, text) in enumerate(scores[:top_k]):
            print(f"Rank {rank + 1} | Score: {score:.4f}")
            print(f"{text[:80]}...\n")

        return [text for _, text in scores[:top_k]]