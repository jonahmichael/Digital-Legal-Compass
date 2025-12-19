from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os

def build_rag_chain(vectorstore):
    """
    Build a RAG (Retrieval-Augmented Generation) chain.
    
    Args:
        vectorstore: The vector store to use for retrieval
        
    Returns:
        Configured RAG chain
    """
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
    
    # Define prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful legal assistant. Use the following pieces of retrieved context to answer the question. If you don't know the answer based on the context, say that you don't know. Keep the answer concise and professional.\n\nContext: {context}"),
        ("human", "{input}"),
    ])
    
    # Build simple RAG chain
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # Create chain that returns both answer and context
    rag_chain = (
        {
            "context": retriever | format_docs,
            "input": RunnablePassthrough()
        }
        | RunnablePassthrough.assign(answer=(prompt | llm | StrOutputParser()))
        | RunnablePassthrough.assign(context=lambda x: retriever.invoke(x["input"]))
    )
    
    return rag_chain
