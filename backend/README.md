# Digital Legal Compass - Backend

RAG-powered legal document assistant built with FastAPI and LangChain.

## Setup

1. **Create a virtual environment:**
```bash
python -m venv venv
.\venv\Scripts\Activate  # Windows PowerShell
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

4. **Run the server:**
```bash
python main.py
# Or use uvicorn directly:
# uvicorn main:app --reload
```

## API Endpoints

### Upload Documents
**POST** `/api/documents/upload`

Upload legal documents (PDF, TXT, MD) for processing and embedding.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `files` (multiple file uploads)

**Response:**
```json
{
  "message": "Documents processed successfully",
  "count": 42
}
```

### Chat with Documents
**POST** `/api/documents/chat`

Ask questions about uploaded documents using RAG.

**Request:**
```json
{
  "query": "What are the key clauses in the contract?"
}
```

**Response:**
```json
{
  "answer": "The key clauses include...",
  "sources": ["contract.pdf", "agreement.pdf"]
}
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── documents.py      # API endpoints
│   └── services/
│       ├── __init__.py
│       ├── document_processor.py  # Document loading & splitting
│       ├── vector_store.py        # ChromaDB vector store
│       └── rag_chain.py           # RAG chain with LangChain
├── main.py                   # FastAPI application
├── requirements.txt
├── .env.example
└── .gitignore
```

## Tech Stack

- **FastAPI** - Modern web framework
- **LangChain** - LLM orchestration
- **OpenAI** - Embeddings & LLM
- **ChromaDB** - Vector database
- **PyPDF** - PDF processing
