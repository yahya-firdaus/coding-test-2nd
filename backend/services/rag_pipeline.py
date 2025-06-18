from typing import List, Dict, Any
from langchain.schema import Document
from services.vector_store import VectorStoreService
from config import settings
import logging
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(self):
        try:
            self.llm = ChatOpenAI(
                model_name=settings.llm_model,
                temperature=settings.llm_temperature,
                max_tokens=settings.max_tokens
            )
            self._setup_chain()
        except Exception as e:
            logger.error(f"Error initializing RAG pipeline: {str(e)}")
            raise

    def _setup_chain(self):
        """Setup the RAG chain with prompt template including chat history."""
        qa_template = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template(
                    """Answer the question based on the following context. If you cannot find the answer in the context, say "I cannot find the answer in the provided context."\n\nContext:\n{context}\n\nQuestion: {question}"""
                ),
            ]
        )

        self.chain = (
            {
                "context": RunnablePassthrough(),
                "question": RunnablePassthrough(),
                "chat_history": RunnablePassthrough(),
            }
            | qa_template
            | self.llm
            | StrOutputParser()
        )

    def generate_answer(self, question: str, context: List[Dict], chat_history: List[Dict[str, str]] = None) -> Dict:
        """Generate answer using RAG pipeline, considering chat history."""
        try:
            combined_context = "\n\n".join([doc["content"] for doc in context])

            # Convert chat_history (List[Dict]) to LangChain BaseMessage format
            formatted_chat_history = []
            if chat_history:
                for msg in chat_history:
                    if msg["role"] == "user":
                        formatted_chat_history.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        formatted_chat_history.append(AIMessage(content=msg["content"]))
            
            inputs = {
                "context": combined_context,
                "question": question,
                "chat_history": formatted_chat_history
            }

            answer = self.chain.invoke(inputs)
            
            return {
                "answer": answer,
                "sources": context
            }
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise
    
    def _retrieve_documents(self, query: str) -> List[Document]:
        """Retrieve relevant documents for the query"""
        try:
            # Search vector store for similar documents
            results = self.vector_store.similarity_search(
                query=query,
                k=settings.retrieval_k
            )
            
            # Filter by similarity threshold
            filtered_results = [
                doc for doc in results 
                if doc["score"] >= settings.similarity_threshold
            ]
            
            return filtered_results
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise
    
    def _generate_context(self, documents: List[Document]) -> str:
        """Generate context from retrieved documents"""
        try:
            # Combine document contents with metadata
            context_parts = []
            for doc in documents:
                context_parts.append(
                    f"Source: {doc.metadata.get('source', 'unknown')}\n"
                    f"Page: {doc.metadata.get('page', 'unknown')}\n"
                    f"Content: {doc.page_content}\n"
                )
            
            return "\n---\n".join(context_parts)
        except Exception as e:
            logger.error(f"Error generating context: {str(e)}")
            raise
    
    def _generate_llm_response(self, question: str, context: str, chat_history: List[Dict[str, str]] = None) -> str:
        """Generate response using LLM"""
        try:
            # Create prompt with question and context
            prompt = f"""Based on the following context and chat history, answer the question:

            Context:
            {context}

            Chat History:
            {self._format_chat_history(chat_history) if chat_history else 'No previous conversation.'}

            Question: {question}

            Answer:"""
            
            # Call LLM API
            response = self.llm.predict(prompt)
            
            return response
        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            raise
    
    def _format_chat_history(self, chat_history: List[Dict[str, str]]) -> str:
        """Format chat history for prompt"""
        formatted_history = []
        for msg in chat_history:
            formatted_history.append(
                f"{msg['role']}: {msg['content']}"
            )
        return "\n".join(formatted_history) 