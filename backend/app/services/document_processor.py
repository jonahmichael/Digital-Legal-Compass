from typing import List
import os

try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

from langchain_core.documents import Document

def process_documents(file_paths: List[str]):
    """
    Load and split documents into chunks for embedding.
    
    Args:
        file_paths: List of file paths to process
        
    Returns:
        List of document splits ready for embedding
    """
    documents = []
    
    for file_path in file_paths:
        try:
            _, ext = os.path.splitext(file_path)
            
            if ext.lower() == '.pdf':
                # Load PDF
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                
                documents.append(Document(
                    page_content=text,
                    metadata={"source": file_path}
                ))
                
            elif ext.lower() in ['.txt', '.md']:
                # Load text file
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                documents.append(Document(
                    page_content=text,
                    metadata={"source": file_path}
                ))
            else:
                print(f"Unsupported file type: {ext}")
                continue
                
        except Exception as e:
            print(f"Error loading {file_path}: {str(e)}")
            continue
    
    # Split documents into chunks
    splits = []
    chunk_size = 1000
    chunk_overlap = 200
    
    for doc in documents:
        text = doc.page_content
        metadata = doc.metadata
        
        # Simple character-based splitting
        for i in range(0, len(text), chunk_size - chunk_overlap):
            chunk_text = text[i:i + chunk_size]
            if chunk_text.strip():
                splits.append(Document(
                    page_content=chunk_text,
                    metadata=metadata
                ))
    
    return splits
