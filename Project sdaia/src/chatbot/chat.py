from src.rag.rag_pipeline import RAGPipeline
from src.llm.openrouter import OpenRouterLLM


class ChatBot:
    def __init__(self):
        self.llm = OpenRouterLLM()
        self.rag = RAGPipeline()

    def load_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        self.rag.build_index(text)
        print(" File loaded into knowledge base")

    def ask(self, question: str):
        # 1) retrieve relevant chunks
        context_chunks = self.rag.retrieve(question)
        context = "\n\n".join(context_chunks)

        # 2) build prompt
        prompt = f"""
You are a precise AI assistant designed for Retrieval-Augmented Generation (RAG).

STRICT RULES:
1. Answer ONLY using the provided context.
2. If the answer is NOT in the context, say: "I don't know based on the provided context."
3. DO NOT use prior knowledge.
4. DO NOT guess or hallucinate.

CONTEXT:
{context}

QUESTION:
{question}

INSTRUCTIONS:
- Provide a clear and concise answer.
- Then provide the exact supporting evidence from the context.
- Cite sources using (Chunk X).

FORMAT:

Answer:
<your answer>

Sources:
- (Chunk X): "<exact sentence>"
- (Chunk Y): "<exact sentence>"
"""

        # 3) call LLM
        response = self.llm.invoke(prompt)

        return response