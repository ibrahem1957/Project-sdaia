from src.llm.openrouter import OpenRouterLLM
from src.agent.base import BaseAgent
from src.agent.prompts import SUMMARIZER_PROMPT, QUESTION_GENERATOR_PROMPT
from src.tools.registry import TOOLS
from src.rag.rag_pipeline import RAGPipeline
from dotenv import load_dotenv
from src.chatbot.chat import ChatBot

load_dotenv()

llm = OpenRouterLLM()


def run(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    rag = RAGPipeline()
    rag.build_index(text)

    retrieved_chunks = rag.retrieve(text[:200])
    context = "\n\n".join(retrieved_chunks)

    # ================= SUMMARY =================
    summarizer = BaseAgent(
        llm=llm,
        tools=TOOLS,
        prompt=SUMMARIZER_PROMPT
    )

    summary = summarizer.run(f"""
Use the following context to summarize:

{context}
""")

    clean_summary = summary["final"].replace("FINAL:", "").strip()

    print("\n===== SUMMARY =====\n")
    print(clean_summary)

    # ================= QUESTIONS =================
    question_agent = BaseAgent(
        llm=llm,
        tools=TOOLS,
        prompt=QUESTION_GENERATOR_PROMPT
    )

    questions = question_agent.run(f"""
Generate questions from this text:

{clean_summary}
""")

    print("\n===== QUESTIONS =====\n")
    print(questions["final"])

    # ================= CHATBOT =================
    bot = ChatBot()
    bot.load_file(file_path)

    print("\n===== CHATBOT READY =====\n")

    while True:
        q = input("\nAsk a question: ")

        if q.lower() in ["exit", "quit"]:
            break

        answer = bot.ask(q)
        print("\n Answer:\n", answer)


if __name__ == "__main__":
    run("src/data.txt")