from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.services.document_processor import process_documents
from app.services.vector_store import get_vectorstore
from app.services.rag_chain import build_rag_chain
import shutil
import os

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(..., description="Upload PDF, TXT, or MD files")):
    """Upload legal documents for processing and embedding."""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    # 1. Save files locally
    os.makedirs("temp_data", exist_ok=True)
    saved_paths = []
    
    for file in files:
        # Validate file type
        if not file.filename:
            continue
        
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.pdf', '.txt', '.md']:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file_ext}. Only PDF, TXT, and MD files are allowed."
            )
        
        file_path = f"temp_data/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_paths.append(file_path)
    
    # 2. Process and Embed
    try:
        splits = process_documents(saved_paths)
        get_vectorstore(documents=splits) # Index them
        return {"message": "Documents processed successfully", "count": len(splits)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def chat(request: ChatRequest):
    """Ask questions about uploaded documents using RAG."""
    # 1. Load DB
    vectorstore = get_vectorstore()
    if not vectorstore:
        raise HTTPException(status_code=400, detail="No documents found. Upload first.")
    
    # 2. Run Chain
    chain = build_rag_chain(vectorstore)
    response = chain.invoke({"input": request.query})
    
    # 3. Format Output
    return {
        "answer": response["answer"],
        "sources": [doc.metadata.get("source", "Unknown") for doc in response["context"]]
    }
