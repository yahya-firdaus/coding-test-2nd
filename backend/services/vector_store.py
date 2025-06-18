from typing import List, Dict
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import os
from config import settings
import logging

logger = logging.getLogger(__name__)

class VectorStoreService:
    def __init__(self, persist_directory: str = None):
        self.persist_directory = persist_directory or settings.vector_db_path
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None
        self._initialize_vector_store()

    def _initialize_vector_store(self):
        """Initialize or load existing vector store."""
        try:
            if os.path.exists(self.persist_directory):
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
            else:
                os.makedirs(self.persist_directory, exist_ok=True)
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
        except Exception as e:
            logger.error(f"Error initializing vector store: {str(e)}")
            raise

    def add_documents(self, documents: List[Dict]):
        """Add documents to vector store."""
        try:
            if not documents:
                raise ValueError("No documents provided")
            
            # Validate document format
            for doc in documents:
                if not isinstance(doc, dict):
                    raise ValueError(f"Document must be a dictionary, got {type(doc)}")
                if "content" not in doc:
                    raise ValueError("Document must have 'content' field")
                if "metadata" not in doc:
                    raise ValueError("Document must have 'metadata' field")
            
            texts = [doc["content"] for doc in documents]
            metadatas = [doc["metadata"] for doc in documents]
            
            if not texts:
                raise ValueError("No text content found in documents")
            
            self.vector_store.add_texts(
                texts=texts,
                metadatas=metadatas
            )
            self.vector_store.persist()
            logger.info(f"Successfully added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise

    def similarity_search(self, query: str, k: int = None) -> List[Dict]:
        """Search for similar documents."""
        try:
            k = k or settings.retrieval_k
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k
            )
            
            return [{
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            } for doc, score in results]
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            raise

    def get_all_documents(self) -> List[Dict]:
        """Retrieve all documents from vector store."""
        try:
            return self.vector_store.get()
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise 