# Digital Legal Compass

> A powerful RAG (Retrieval-Augmented Generation) powered legal document assistant that helps you analyze and query legal documents using natural language.

## � Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[Documentation Index](DOCUMENTATION.md)** - Full documentation map
- **[Backend Docs](backend/README.md)** - Backend setup & architecture
- **[Frontend Docs](frontend/README.md)** - Frontend setup & development

## �📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

Digital Legal Compass is an AI-powered document analysis tool specifically designed for legal documents. It uses advanced RAG techniques to provide accurate, context-aware answers to questions about your uploaded legal documents.

**Key Technologies:**
- **Backend**: FastAPI, LangChain, Google Gemini AI, ChromaDB
- **Frontend**: Next.js 14, React 18, Tailwind CSS
- **AI**: Google Generative AI (Gemini 1.5 Flash & Embeddings)

## Features

✨ **Core Features:**
- 📄 **Multi-format Support**: Upload PDF, TXT, and MD files
- 🤖 **AI-Powered Chat**: Ask natural language questions about your documents
- 🔍 **Semantic Search**: Vector-based document retrieval using ChromaDB
- 📊 **Source Attribution**: Get answers with references to source documents
- 💬 **Context-Aware Responses**: Maintains conversation context
- 🎨 **Modern UI**: Responsive, intuitive interface built with Next.js
- ⚡ **Fast Processing**: Efficient document chunking and embedding
- 🔒 **Local Storage**: Documents processed and stored locally

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│             │  HTTP   │              │  API    │             │
│  Next.js    │────────▶│   FastAPI    │────────▶│  Google AI  │
│  Frontend   │  Proxy  │   Backend    │         │  (Gemini)   │
│             │◀────────│              │◀────────│             │
└─────────────┘         └──────────────┘         └─────────────┘
                              │
                              │
                              ▼
                        ┌──────────────┐
                        │   ChromaDB   │
                        │ Vector Store │
                        └──────────────┘
```

**Data Flow:**
1. User uploads documents via Next.js frontend
2. FastAPI backend processes and chunks documents
3. Documents are embedded using Google Generative AI Embeddings
4. Embeddings stored in ChromaDB vector database
5. User queries are converted to embeddings
6. Relevant document chunks retrieved via similarity search
7. Context + query sent to Gemini AI for answer generation
8. Response returned to user with source attribution

## Prerequisites

**Required:**
- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn
- Google API Key (for Gemini AI)

**Recommended:**
- 4GB RAM minimum
- Git for version control
- VS Code or similar IDE

## Quick Start

### Backend Setup

1. **Navigate to the backend directory:**
```bash
cd backend
```

2. **Create a virtual environment:**
```bash
python -m venv venv
.\venv\Scripts\Activate  # Windows PowerShell
# or
source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**

Create a `.env` file in the backend directory:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

**How to get Google API Key:**
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Sign in with your Google account
- Click "Create API Key"
- Copy and paste into `.env` file

5. **Run the backend server:**
```bash
python main.py
```

The backend API will be available at **http://localhost:8000**

### Frontend Setup

1. **Navigate to the frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Run the development server:**
```bash
npm run dev
```

The UI will be available at **http://localhost:3000**

## Configuration

### Backend Configuration

**Environment Variables (`.env`):**
```env
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional (defaults shown)
CHROMA_DB_PATH=./chroma_db
TEMP_DATA_PATH=./temp_data
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

**Configuration Options:**
- `GOOGLE_API_KEY`: Your Google API key for Gemini AI
- `CHROMA_DB_PATH`: Directory for vector database storage
- `TEMP_DATA_PATH`: Directory for temporary file storage
- `CHUNK_SIZE`: Size of document chunks (characters)
- `CHUNK_OVERLAP`: Overlap between chunks (characters)

### Frontend Configuration

**Environment Variables (`.env.local`):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Usage Guide

### Starting the Application

**Step 1: Start Backend**
```bash
cd backend
.\venv\Scripts\Activate  # Windows
python main.py
```
Backend runs on http://localhost:8000

**Step 2: Start Frontend**
```bash
cd frontend
npm run dev
```
Frontend runs on http://localhost:3000

### Using the Application

**1. Upload Documents**
- Click "Select legal documents" or drag & drop files
- Supported formats: PDF, TXT, MD
- Multiple files can be uploaded at once
- Wait for "Successfully uploaded" confirmation

**2. Ask Questions**
- Type your question in the chat input
- Press Enter or click Send
- Wait for AI-generated response
- View source documents referenced in the answer

**Example Questions:**
- "What are the key terms in the contract?"
- "Summarize the confidentiality clause"
- "What are the payment terms?"
- "Who are the parties involved in this agreement?"
- "What are the termination conditions?"

### Best Practices

**Document Preparation:**
- Ensure documents are text-based (scanned PDFs may not work well)
- Remove any confidential information before uploading
- Use clear, searchable document names
- Upload related documents together for better context

**Query Optimization:**
- Be specific in your questions
- Reference document types when relevant
- Ask follow-up questions for clarification
- Use legal terminology when appropriate

## API Documentation

Full API documentation available at: **http://localhost:8000/docs** (Swagger UI)

### Endpoints

#### Upload Documents
```http
POST /api/documents/upload
Content-Type: multipart/form-data

files: [File, File, ...]
```

**Response:**
```json
{
  "message": "Documents processed successfully",
  "count": 42
}
```

#### Chat with Documents
```http
POST /api/documents/chat
Content-Type: application/json

{
  "query": "What are the key clauses?"
}
```

**Response:**
```json
{
  "answer": "The key clauses include...",
  "sources": ["contract.pdf", "agreement.pdf"]
}
```

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

## Tech Stack

### Backend
| Technology | Purpose | Version |
|------------|---------|----------|
| FastAPI | Web framework | Latest |
| LangChain | LLM orchestration | Latest |
| Google Gemini AI | LLM & Embeddings | 1.5 Flash |
| ChromaDB | Vector database | Latest |
| PyPDF/PyPDF2 | PDF processing | Latest |
| Python-dotenv | Environment variables | Latest |

### Frontend
| Technology | Purpose | Version |
|------------|---------|----------|
| Next.js | React framework | 14.x |
| React | UI library | 18.x |
| Tailwind CSS | Styling | 3.x |
| Axios | HTTP client | Latest |

## Troubleshooting

### Common Issues

**Issue: "GOOGLE_API_KEY not found"**
- Solution: Create `.env` file in backend directory with valid API key

**Issue: "No documents found. Upload first."**
- Solution: Upload documents before attempting to chat

**Issue: "Connection refused on port 8000"**
- Solution: Ensure backend server is running

**Issue: "Module not found" errors**
- Solution: Reinstall dependencies
  ```bash
  # Backend
  pip install -r requirements.txt
  
  # Frontend
  npm install
  ```

**Issue: "PDF processing errors"**
- Solution: Ensure PDF is text-based, not scanned images

**Issue: "Frontend can't connect to backend"**
- Solution: Check CORS settings and ensure backend is running on port 8000

### Debug Mode

**Backend Debug:**
```bash
uvicorn main:app --reload --log-level debug
```

**Frontend Debug:**
```bash
npm run dev -- --debug
```

### Logs

- Backend logs: Console output
- ChromaDB: `chroma_db/` directory
- Uploaded files: `temp_data/` directory

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Create a Pull Request

### Code Style

- **Python**: Follow PEP 8
- **JavaScript**: Follow Airbnb style guide
- **Commits**: Use conventional commits

### Testing

Before submitting PR:
1. Test document upload with various formats
2. Test chat functionality
3. Verify API responses
4. Check UI responsiveness
5. Test error handling

## Usage

1. Start the backend server first (port 8000)
2. Start the frontend server (port 3000)
3. Open http://localhost:3000 in your browser
4. Upload legal documents (PDF, TXT, MD) using the upload interface
5. Ask questions about your documents in the chat interface

## Features

- **Document Upload**: Process multiple legal documents (PDF, TXT, MD)
- **RAG-Powered Chat**: Ask questions and get answers based on your documents
- **Vector Search**: ChromaDB for efficient semantic search
- **Modern UI**: Responsive Next.js interface with Tailwind CSS

## Project Structure

```
digitallegalcompass/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── documents.py          # API endpoints for upload & chat
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── document_processor.py # Document loading & chunking
│   │       ├── vector_store.py       # ChromaDB operations
│   │       └── rag_chain.py          # RAG chain with LangChain
│   ├── chroma_db/                    # Vector database storage
│   ├── temp_data/                    # Temporary file storage
│   ├── main.py                       # FastAPI application entry
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # Environment variables (create this)
│   └── README.md                     # Backend documentation
└── frontend/
    ├── app/
    │   ├── components/
    │   │   ├── DocumentUpload.js     # Upload component
    │   │   └── Chat.js               # Chat interface component
    │   ├── layout.js                 # Root layout
    │   ├── page.js                   # Home page
    │   └── globals.css               # Global styles
    ├── public/                       # Static assets
    ├── package.json                  # Node dependencies
    ├── next.config.js                # Next.js configuration
    ├── tailwind.config.js            # Tailwind CSS configuration
    ├── .env.local                    # Environment variables
    └── README.md                     # Frontend documentation
```

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## Acknowledgments

- Google Gemini AI for powerful language models
- LangChain for RAG implementation
- FastAPI for backend framework
- Next.js for frontend framework
- ChromaDB for vector storage

---

Made with ❤️ for legal professionals
