# AI Multi-Agent RAG System

A production-style AI system that combines Agents and Retrieval-Augmented Generation (RAG) to analyze documents, generate summaries, create questions, and answer user queries through a chatbot.

---

## Features

### Multi-Agent System
- Summarizer Agent  
- Question Generator Agent  

### RAG Pipeline
- Text chunking  
- Embeddings using OpenRouter  
- Vector similarity search  

### Chatbot
- Ask questions about a document  
- Retrieves the most relevant chunks using similarity  

### Observability
- Step-based tracing  
- Execution time tracking  
- Tool usage logging  

### Tool System
- `read_file` integration  

### Reliability
- Loop detection  
- Repetition prevention logic  
