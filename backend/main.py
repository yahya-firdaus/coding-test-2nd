from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.schemas import ChatRequest, ChatResponse, DocumentsResponse, UploadResponse
from services.pdf_processor import PDFProcessor
from services.vector_store import VectorStoreService
from services.rag_pipeline import RAGPipeline
from config import settings
import logging
import time
import os
import shutil
from typing import List, Dict
from datetime import datetime

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG-based Financial Statement Q&A System",
    description="AI-powered Q&A system for financial documents using RAG",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
pdf_processor = PDFProcessor()
vector_store = VectorStoreService()
rag_pipeline = RAGPipeline()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        logger.info("Starting RAG Q&A System...")
        # Create necessary directories
        os.makedirs("data", exist_ok=True)
        os.makedirs(settings.vector_db_path, exist_ok=True)
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "RAG-based Financial Statement Q&A System is running"}


@app.post("/api/upload")
async def upload_pdf(files: List[UploadFile] = File(...)):
    """Upload and process PDF file(s)."""
    processed_files_info = []
    for file in files:
        try:
            start_time = time.time()
            
            # Save uploaded file
            file_path = f"data/{file.filename}"
            os.makedirs("data", exist_ok=True)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Process PDF
            chunks = pdf_processor.process_pdf(file_path)
            
            # Store in vector database
            vector_store.add_documents(chunks)
            
            processing_time = time.time() - start_time
            
            processed_files_info.append({
                "filename": file.filename,
                "chunks_count": len(chunks),
                "processing_time": processing_time
            })
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            # Continue processing other files even if one fails
            processed_files_info.append({
                "filename": file.filename,
                "status": "failed",
                "error": str(e)
            })
    
    if not processed_files_info:
        raise HTTPException(status_code=400, detail="No files were processed.")
    
    return JSONResponse(content=processed_files_info)


@app.get("/api/documents")
async def get_documents():
    """Get information about processed documents."""
    try:
        # TODO: Refactor to retrieve detailed document metadata from ChromaDB
        documents = vector_store.get_all_documents()
        
        # Group chunks by source (filename) and count them
        files_info = {}
        for doc_id, metadata in documents["metadatas"].items():
            source = metadata.get("source", "unknown")
            if source not in files_info:
                files_info[source] = {
                    "filename": source,
                    "upload_date": datetime.now().isoformat(),  # Placeholder for actual upload date
                    "chunks_count": 0,
                    "status": "processed"
                }
            files_info[source]["chunks_count"] += 1
            
        return DocumentsResponse(
            documents=list(files_info.values())
        )
    except Exception as e:
        logger.error(f"Error retrieving documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Generate answer for user question."""
    try:
        start_time = time.time()
        
        # Retrieve relevant documents
        context = vector_store.similarity_search(request.question)
        
        # Generate answer
        result = rag_pipeline.generate_answer(request.question, context)
        
        processing_time = time.time() - start_time
        
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            processing_time=processing_time
        )
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chunks")
async def get_chunks():
    """Get all document chunks."""
    try:
        documents = vector_store.get_all_documents()
        
        # Format chunks for display
        formatted_chunks = []
        for i, (content_id, content) in enumerate(documents["documents"].items()):
            metadata = documents["metadatas"].get(content_id, {})
            formatted_chunks.append({
                "id": content_id,
                "content": content,
                "metadata": metadata
            })
        
        return {"chunks": formatted_chunks}
    except Exception as e:
        logger.error(f"Error retrieving chunks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port, reload=settings.debug) 