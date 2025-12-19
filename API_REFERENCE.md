# Digital Legal Compass - API Reference

Complete API documentation for the Digital Legal Compass backend service.

## Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

## Table of Contents

- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [Root](#root)
  - [Health Check](#health-check)
  - [Upload Documents](#upload-documents)
  - [Chat with Documents](#chat-with-documents)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

## Authentication

Currently, the API does not require authentication. For production deployment, implement authentication using:
- API Keys
- JWT Tokens
- OAuth 2.0

## Endpoints

### Root

Get API information and links to documentation.

**Endpoint:** `GET /`

**Request:**
```http
GET / HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "message": "Welcome to Digital Legal Compass API",
  "docs": "/docs",
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK`: Success

---

### Health Check

Check if the API is operational.

**Endpoint:** `GET /health`

**Request:**
```http
GET /health HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Codes:**
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is down

**Use Cases:**
- Load balancer health checks
- Monitoring and alerting
- Service availability verification

---

### Upload Documents

Upload and process legal documents for embedding and retrieval.

**Endpoint:** `POST /api/documents/upload`

**Request:**
```http
POST /api/documents/upload HTTP/1.1
Host: localhost:8000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="files"; filename="contract.pdf"
Content-Type: application/pdf

[Binary PDF Content]
------WebKitFormBoundary
Content-Disposition: form-data; name="files"; filename="terms.txt"
Content-Type: text/plain

[Text Content]
------WebKitFormBoundary--
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| files | File[] | Yes | Array of files to upload |

**Supported File Types:**
- `.pdf` - PDF documents
- `.txt` - Plain text files
- `.md` - Markdown files

**File Size Limits:**
- Maximum per file: 10MB (configurable)
- Maximum total: 50MB (configurable)

**Response (Success):**
```json
{
  "message": "Documents processed successfully",
  "count": 42
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| message | string | Success message |
| count | integer | Number of document chunks created |

**Status Codes:**
- `200 OK`: Upload successful
- `400 Bad Request`: No files or invalid file type
- `413 Payload Too Large`: File size exceeded
- `500 Internal Server Error`: Processing error

**Processing Steps:**
1. Validate file types
2. Save files to temporary storage
3. Extract text from documents
4. Split text into chunks (1000 chars, 200 overlap)
5. Generate embeddings using Google AI
6. Store in ChromaDB vector database

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@/path/to/contract.pdf" \
  -F "files=@/path/to/terms.txt"
```

**Example (Python):**
```python
import requests

files = [
    ('files', ('contract.pdf', open('contract.pdf', 'rb'), 'application/pdf')),
    ('files', ('terms.txt', open('terms.txt', 'rb'), 'text/plain'))
]

response = requests.post(
    'http://localhost:8000/api/documents/upload',
    files=files
)

print(response.json())
```

**Example (JavaScript/Axios):**
```javascript
const formData = new FormData();
formData.append('files', fileInput.files[0]);
formData.append('files', fileInput.files[1]);

const response = await axios.post(
  'http://localhost:8000/api/documents/upload',
  formData,
  {
    headers: { 'Content-Type': 'multipart/form-data' }
  }
);
```

---

### Chat with Documents

Ask questions about uploaded documents using RAG.

**Endpoint:** `POST /api/documents/chat`

**Request:**
```http
POST /api/documents/chat HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "query": "What are the key terms in the contract?"
}
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| query | string | Yes | Question to ask about documents |

**Query Guidelines:**
- Be specific and clear
- Use complete sentences
- Reference document types when relevant
- Keep queries under 500 characters

**Response (Success):**
```json
{
  "answer": "The key terms in the contract include: 1) Payment of $1000 per month, 2) Contract duration of 12 months, 3) Termination with 30 days notice, and 4) Confidentiality obligations for both parties.",
  "sources": [
    "contract.pdf",
    "terms.txt"
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| answer | string | AI-generated answer based on documents |
| sources | string[] | Source documents used for answer |

**Status Codes:**
- `200 OK`: Query successful
- `400 Bad Request`: Invalid query or no documents found
- `500 Internal Server Error`: Processing error

**Processing Steps:**
1. Validate query
2. Generate query embedding
3. Search vector database (retrieves top 4 chunks)
4. Construct prompt with context
5. Send to Google Gemini AI
6. Parse and return response with sources

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/api/documents/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the payment terms?"}'
```

**Example (Python):**
```python
import requests

response = requests.post(
    'http://localhost:8000/api/documents/chat',
    json={'query': 'What are the payment terms?'}
)

data = response.json()
print(f"Answer: {data['answer']}")
print(f"Sources: {', '.join(data['sources'])}")
```

**Example (JavaScript/Axios):**
```javascript
const response = await axios.post(
  'http://localhost:8000/api/documents/chat',
  { query: 'What are the payment terms?' }
);

console.log('Answer:', response.data.answer);
console.log('Sources:', response.data.sources);
```

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error description message"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid input or missing parameters |
| 404 | Not Found | Endpoint doesn't exist |
| 413 | Payload Too Large | File size exceeded |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | Service is down |

### Common Errors

**No Documents Found:**
```json
{
  "detail": "No documents found. Upload first."
}
```
**Solution:** Upload documents before attempting to chat.

**Unsupported File Type:**
```json
{
  "detail": "Unsupported file type: .docx. Only PDF, TXT, and MD files are allowed."
}
```
**Solution:** Convert document to supported format.

**Processing Error:**
```json
{
  "detail": "Error processing PDF: encrypted file"
}
```
**Solution:** Remove encryption or use different file.

---

## Rate Limiting

**Not Currently Implemented**

For production, implement rate limiting:
- 100 requests per minute per IP
- 1000 requests per hour per IP
- Burst allowance of 20 requests

**Example Response (Rate Limited):**
```json
{
  "detail": "Rate limit exceeded. Please try again later.",
  "retry_after": 60
}
```

---

## Examples

### Complete Upload and Query Workflow (Python)

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Step 1: Health Check
health = requests.get(f"{BASE_URL}/health")
print("Health:", health.json())

# Step 2: Upload Documents
files = [
    ('files', ('contract.pdf', open('contract.pdf', 'rb'), 'application/pdf')),
    ('files', ('terms.txt', open('terms.txt', 'rb'), 'text/plain'))
]

upload_response = requests.post(
    f"{BASE_URL}/api/documents/upload",
    files=files
)

print("Upload:", upload_response.json())
# Output: {"message": "Documents processed successfully", "count": 42}

# Step 3: Query Documents
queries = [
    "What are the payment terms?",
    "Who are the parties involved?",
    "What is the contract duration?"
]

for query in queries:
    chat_response = requests.post(
        f"{BASE_URL}/api/documents/chat",
        json={"query": query}
    )
    
    data = chat_response.json()
    print(f"\nQ: {query}")
    print(f"A: {data['answer']}")
    print(f"Sources: {', '.join(data['sources'])}")
```

### Complete Workflow (JavaScript)

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const BASE_URL = 'http://localhost:8000';

async function main() {
  // Step 1: Health Check
  const health = await axios.get(`${BASE_URL}/health`);
  console.log('Health:', health.data);

  // Step 2: Upload Documents
  const formData = new FormData();
  formData.append('files', fs.createReadStream('contract.pdf'));
  formData.append('files', fs.createReadStream('terms.txt'));

  const uploadResponse = await axios.post(
    `${BASE_URL}/api/documents/upload`,
    formData,
    { headers: formData.getHeaders() }
  );

  console.log('Upload:', uploadResponse.data);

  // Step 3: Query Documents
  const queries = [
    'What are the payment terms?',
    'Who are the parties involved?',
    'What is the contract duration?'
  ];

  for (const query of queries) {
    const chatResponse = await axios.post(
      `${BASE_URL}/api/documents/chat`,
      { query }
    );

    console.log(`\nQ: ${query}`);
    console.log(`A: ${chatResponse.data.answer}`);
    console.log(`Sources: ${chatResponse.data.sources.join(', ')}`);
  }
}

main().catch(console.error);
```

---

## Interactive Documentation

For interactive API testing, visit:

**Swagger UI:** http://localhost:8000/docs

**ReDoc:** http://localhost:8000/redoc

Both provide:
- Interactive request forms
- Request/response examples
- Schema definitions
- Try-it-out functionality

---

## Websocket Support (Future)

Planned for real-time streaming responses:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');

ws.send(JSON.stringify({ query: 'What are the payment terms?' }));

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Chunk:', data.text);
};
```

---

## SDK Examples (Future)

**Python SDK:**
```python
from digital_legal_compass import Client

client = Client(base_url="http://localhost:8000")
client.upload_documents(['contract.pdf', 'terms.txt'])
answer = client.chat("What are the payment terms?")
```

**JavaScript SDK:**
```javascript
import { DigitalLegalCompass } from 'digital-legal-compass-sdk';

const client = new DigitalLegalCompass('http://localhost:8000');
await client.uploadDocuments(['contract.pdf', 'terms.txt']);
const answer = await client.chat('What are the payment terms?');
```

---

**For more information, see:**
- [Main README](README.md)
- [Backend Documentation](backend/README.md)
- [Frontend Documentation](frontend/README.md)
- [Quick Start Guide](QUICKSTART.md)
