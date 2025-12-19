from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List, Optional
import os

# Persistent storage path
CHROMA_DB_PATH = "./chroma_db"

def get_vectorstore(documents: Optional[List] = None):
    """
    Get or create a vector store.
    
    Args:
        documents: Optional list of documents to add to the vector store
        
    Returns:
        Chroma vector store instance
    """
    # Initialize embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # If documents provided, create new vectorstore or add to existing
    if documents:
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=CHROMA_DB_PATH
        )
        return vectorstore
    
    # Otherwise, load existing vectorstore
    if os.path.exists(CHROMA_DB_PATH):
        vectorstore = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embeddings
        )
        return vectorstore
    
    return None
