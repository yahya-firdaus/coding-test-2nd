import os
from typing import List, Dict, Any
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise

    def split_text(self, text: str) -> List[str]:
        """Split text into chunks."""
        try:
            return self.text_splitter.split_text(text)
        except Exception as e:
            logger.error(f"Error splitting text: {str(e)}")
            raise

    def process_pdf(self, pdf_path: str) -> List[Dict]:
        """Process PDF file and return chunks with metadata."""
        try:
            # Extract text from PDF
            text = self.extract_text_from_pdf(pdf_path)
            if not text:
                raise ValueError("No text could be extracted from the PDF")

            # Split text into chunks
            chunks = self.split_text(text)
            if not chunks:
                raise ValueError("No chunks could be created from the text")

            # Create documents with metadata
            documents = []
            for i, chunk in enumerate(chunks):
                doc = {
                    "content": chunk,
                    "metadata": {
                        "source": os.path.basename(pdf_path),
                        "chunk": i + 1,
                        "total_chunks": len(chunks)
                    }
                }
                documents.append(doc)

            logger.info(f"Successfully processed PDF into {len(documents)} chunks")
            return documents
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise 