# Digital Legal Compass - Backend

> FastAPI backend service for RAG-powered legal document analysis using LangChain and Google Gemini AI.

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Development](#development)
- [Testing](#testing)

## Overview

The backend service provides a RESTful API for processing legal documents and answering questions using Retrieval-Augmented Generation (RAG). It handles document ingestion, text chunking, vector embeddings, and AI-powered question answering.

### Key Features

- 📁 **Document Processing**: Support for PDF, TXT, and MD files
- 🔍 **Vector Search**: ChromaDB for semantic document retrieval
- 🤖 **AI Integration**: Google Gemini AI for embeddings and generation
- ⚡ **Fast API**: High-performance async endpoints
- 📊 **Source Attribution**: Returns relevant document sources with answers
- 🔄 **Persistent Storage**: Vector database persists across restarts

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | FastAPI | High-performance web framework |
| **LLM Orchestration** | LangChain | RAG pipeline management |
| **Language Model** | Google Gemini 1.5 Flash | Answer generation |
| **Embeddings** | Google Generative AI Embeddings | Document vectorization |
| **Vector Database** | ChromaDB | Semantic search & retrieval |
| **PDF Processing** | PyPDF/PyPDF2 | PDF text extraction |
| **Environment** | python-dotenv | Configuration management |

## Setup

### Prerequisites

- Python 3.8 or higher
- Google API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

### Installation

1. **Create a virtual environment:**
```bash
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate

# macOS/Linux
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**


Create a `.env` file in the backend directory:
```env
GOOGLE_API_KEY=your_google_api_key_here

```bash
cp .env.example .env
# Edit .env and add your Google API Key
>>>>>>> 45e798b81affe9dfb25ee9a6972ccb9e8e65ebe0
```

**Getting Your API Key:**
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Sign in with your Google account
- Click "Create API Key"
- Copy and save in `.env` file

4. **Run the server:**
```bash
# Using Python directly
python main.py

# Or using uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000**

Interactive API documentation (Swagger): **http://localhost:8000/docs**

## API Endpoints

### Root Endpoint

```http
GET /
```

**Response:**
```json
{
  "message": "Welcome to Digital Legal Compass API",
  "docs": "/docs",
  "version": "1.0.0"
}
```

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

### Upload Documents
**POST** `/api/documents/upload`

Upload legal documents (PDF, TXT, MD) for processing and embedding.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `files` (multiple file uploads)

}
```

### Upload Documents

**POST** `/api/documents/upload`

Upload legal documents (PDF, TXT, MD) for processing and embedding.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Body Parameter**: `files` (array of files)

**Supported File Types:**
- `.pdf` - PDF documents
- `.txt` - Plain text files
- `.md` - Markdown files

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "files=@contract.pdf" \
  -F "files=@agreement.txt"
```

**Example using Python:**
```python
import requests

files = [
    ('files', open('contract.pdf', 'rb')),
    ('files', open('agreement.txt', 'rb'))
]

response = requests.post(
    'http://localhost:8000/api/documents/upload',
    files=files
)

print(response.json())
```

**Success Response (200):**
```json
{
  "message": "Documents processed successfully",
  "count": 42
}
```

**Error Responses:**
- `400`: No files provided or unsupported file type
- `500`: Processing error (check logs for details)

**Processing Steps:**
1. Files saved to `temp_data/` directory
2. Text extracted from documents
3. Documents split into chunks (1000 chars, 200 overlap)
4. Chunks embedded using Google AI
5. Embeddings stored in ChromaDB

### Chat with Documents

**POST** `/api/documents/chat`

Ask questions about uploaded documents using RAG (Retrieval-Augmented Generation).

**Request:**
- **Content-Type**: `application/json`
- **Body:**
```json
{
  "query": "What are the key clauses in the contract?"
}
```

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/api/documents/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the payment terms?"}'
```

**Example using Python:**
```python
import requests

response = requests.post(
    'http://localhost:8000/api/documents/chat',
    json={"query": "What are the key terms?"}
)

print(response.json())
```

**Success Response (200):**
```json
{
  "answer": "The key clauses include confidentiality, payment terms, and termination conditions...",
  "sources": ["contract.pdf", "agreement.txt"]
}
```

**Error Responses:**
- `400`: No documents found (upload documents first)
- `500`: Processing error

**Processing Steps:**
1. Query embedded using Google AI
2. Relevant document chunks retrieved (top 4)
3. Context + query sent to Gemini AI
4. Generated answer returned with sources
**POST** `/api/documents/chat`

Ask questions about uploaded documents using RAG.

**Request:**
```json
{
  "query": "What are the key clauses in the contract?"
}
```

3. Context + query sent to Gemini AI
4. Generated answer returned with sources

## Project Structure

```
backend/
├── app/
│   ├── __init__.py                    # Package initializer
│   ├── routers/
│   │   ├── __init__.py
│   │   └── documents.py               # Document endpoints (upload, chat)
│   └── services/
│       ├── __init__.py
│       ├── document_processor.py      # Document loading & text chunking
│       ├── vector_store.py            # ChromaDB vector store operations
│       └── rag_chain.py               # RAG chain configuration
├── chroma_db/                         # ChromaDB persistent storage
│   └── chroma.sqlite3                 # Vector database file
├── temp_data/                         # Temporary uploaded files
├── main.py                            # FastAPI application entry point
├── requirements.txt                   # Python dependencies
├── .env                               # Environment variables (create this)
├── .gitignore                         # Git ignore rules
└── README.md                          # This file
```

### Module Descriptions

#### `main.py`
- FastAPI application initialization
- CORS configuration
- Router registration
- Server startup configuration

#### `app/routers/documents.py`
- **Upload endpoint**: Handles file uploads, validation, and processing
- **Chat endpoint**: Manages RAG query execution
- Request/response models
- Error handling

#### `app/services/document_processor.py`
- **File loading**: PDF, TXT, MD support
- **Text extraction**: PyPDF for PDFs, direct read for text
- **Document chunking**: Splits text into manageable pieces
- **Metadata management**: Tracks source documents

#### `app/services/vector_store.py`
- **ChromaDB initialization**: Creates/loads vector database
- **Embedding generation**: Google Generative AI Embeddings
- **Document indexing**: Stores vectorized chunks
- **Persistent storage**: Maintains database across restarts

#### `app/services/rag_chain.py`
- **Retriever configuration**: Similarity search setup
- **Prompt engineering**: System prompts for legal context
- **LLM integration**: Google Gemini AI configuration
- **Chain orchestration**: LangChain pipeline management

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Required
GOOGLE_API_KEY=your_api_key_here

# Optional (with defaults)
CHROMA_DB_PATH=./chroma_db
TEMP_DATA_PATH=./temp_data
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVER_K=4
MODEL_TEMPERATURE=0
```

### Configuration Options

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GOOGLE_API_KEY` | Google AI API key | - | Yes |
| `CHROMA_DB_PATH` | Vector database directory | `./chroma_db` | No |
| `TEMP_DATA_PATH` | Temporary file storage | `./temp_data` | No |
| `CHUNK_SIZE` | Document chunk size (chars) | `1000` | No |
| `CHUNK_OVERLAP` | Chunk overlap (chars) | `200` | No |
| `RETRIEVER_K` | Number of docs to retrieve | `4` | No |
| `MODEL_TEMPERATURE` | LLM creativity (0-1) | `0` | No |

### CORS Configuration

By default, CORS allows all origins (`allow_origins=["*"]`). For production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --log-level debug
```

Flags:
- `--reload`: Auto-reload on code changes
- `--log-level debug`: Verbose logging
- `--host 0.0.0.0`: Listen on all interfaces
- `--port 8000`: Custom port

### Adding New Endpoints

1. Create route in `app/routers/documents.py`:
```python
@router.get("/stats")
async def get_stats():
    return {"total_documents": count}
```

2. Router automatically registered in `main.py`

### Modifying Document Processing

Edit `app/services/document_processor.py`:

```python
def process_documents(file_paths: List[str]):
    # Add custom processing logic
    # Modify chunk_size, chunk_overlap
    # Add new file type support
    pass
```

### Customizing RAG Chain

Edit `app/services/rag_chain.py`:

```python
# Change retrieval strategy
retriever = vectorstore.as_retriever(
    search_type="mmr",  # Maximum Marginal Relevance
    search_kwargs={"k": 6, "fetch_k": 10}
)

# Modify prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "Your custom system prompt..."),
    ("human", "{input}")
])
```

## Testing

### Manual Testing

**Test Upload:**
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "files=@test.pdf"
```

**Test Chat:**
```bash
curl -X POST "http://localhost:8000/api/documents/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "Test question?"}'
```

**Test Health:**
```bash
curl http://localhost:8000/health
```

### Python Testing Script

```python
import requests

# Upload
files = [('files', open('test.pdf', 'rb'))]
upload_response = requests.post(
    'http://localhost:8000/api/documents/upload',
    files=files
)
print("Upload:", upload_response.json())

# Chat
chat_response = requests.post(
    'http://localhost:8000/api/documents/chat',
    json={"query": "What is this document about?"}
)
print("Chat:", chat_response.json())
```

### Common Issues

**Issue: "GOOGLE_API_KEY not found"**
- Ensure `.env` file exists in backend directory
- Check `.env` contains `GOOGLE_API_KEY=your_key`
- Restart server after creating `.env`

**Issue: "No module named 'pypdf'"**
- Run: `pip install -r requirements.txt`
- Or: `pip install pypdf` or `pip install PyPDF2`

**Issue: "ChromaDB error"**
- Delete `chroma_db/` directory and restart
- Check write permissions

**Issue: "PDF processing fails"**
- Ensure PDF is text-based, not scanned image
- Try with .txt or .md files first

## Dependencies

See `requirements.txt` for all dependencies:

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6
langchain>=0.1.0
langchain-google-genai>=0.0.6
chromadb>=0.4.0
pypdf>=3.17.0
python-dotenv>=1.0.0
```

## Production Deployment

### Security Checklist

- [ ] Change CORS settings to specific origins
- [ ] Use HTTPS
- [ ] Secure API key storage (environment variables, secrets manager)
- [ ] Implement rate limiting
- [ ] Add authentication/authorization
- [ ] Enable request validation
- [ ] Set up logging and monitoring

### Performance Optimization

- Use connection pooling for database
- Implement caching for frequent queries
- Use async operations throughout
- Scale with multiple workers: `uvicorn main:app --workers 4`

### Monitoring

- Monitor API response times
- Track ChromaDB size and performance
- Log errors and exceptions
- Monitor memory usage

---

For frontend setup and usage, see [frontend/README.md](../frontend/README.md)