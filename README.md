# DocuMind AI

An AI-powered Retrieval-Augmented Generation (RAG) platform that allows users to upload PDF documents, chat with them using natural language, and generate intelligent summaries.

## Features

- JWT-based Authentication
- PDF Upload & Management
- PDF Text Extraction
- Smart Chunking
- Gemini Embeddings
- ChromaDB Vector Storage
- Hybrid Search (BM25 + Vector Search)
- Reciprocal Rank Fusion (RRF)
- Multi-PDF Chat
- Conversation Memory
- AI-Powered Question Answering
- Page-Level Citations
- Chat History
- PDF Summarization

---

## Tech Stack

### Backend
- FastAPI
- Python

### AI
- Gemini API
- Retrieval-Augmented Generation (RAG)
- BM25
- Reciprocal Rank Fusion (RRF)

### Databases
- MongoDB
- ChromaDB

### Authentication
- JWT

---

## Project Architecture

See the architecture diagram below.

---

## API Endpoints

### Authentication

- POST /auth/signup
- POST /auth/login

### PDF Management

- POST /pdf/upload
- GET /pdf/list
- DELETE /pdf/{pdf_id}
- GET /pdf/{pdf_id}/summary

### Chat

- POST /chat/
- GET /chat/history

---

## RAG Pipeline

PDF Upload
→ Text Extraction
→ Chunking
→ Embedding Generation
→ ChromaDB Storage

User Query
→ Hybrid Retrieval (BM25 + Vector Search + RRF)
→ Conversation Memory
→ Gemini
→ Answer + Citations

---

## Future Improvements

- Document Classification
- MCQ Generation
- Streaming Responses
- Role-Based Access Control
- Deployment with Docker
- Reranking Models

---

## Author

Aryan Dev

