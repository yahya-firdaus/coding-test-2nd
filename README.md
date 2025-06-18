# RAG-based Financial Statement Q&A System Coding Challenge

## Overview
Build a full-stack application using **RAG (Retrieval Augmented Generation)** technology:
1. **Next.js** as the frontend framework
2. **FastAPI** as the backend API layer
3. **PDF financial statement document** based intelligent Q&A system
4. **Vector database** for document search and generative AI

Parse and embed the provided **`FinancialStatement_2025_I_AADIpdf.pdf`** file, then build a system where users can ask questions about the financial statement and AI generates answers by retrieving relevant information.

---

## How to Complete This Assignment

### 📋 **Assignment Process**
1. **Fork this repository** to your own GitHub account
2. **Clone your forked repository** to your local machine
3. **Complete the coding challenge** following the requirements below
4. **Push your completed solution** to your forked repository
5. **Send your repository URL via email** when completed

### 🚀 **Getting Started**
```bash
# Fork this repository on GitHub (click "Fork" button)
# Then clone your forked repository
git clone https://github.com/YOUR_USERNAME/coding-test-2nd.git
cd coding-test-2nd

# Start development...
```

### ✉️ **Submission**
When you complete the assignment:
- Ensure your code is pushed to your forked repository
- Test that your application runs correctly
- **Send your GitHub repository URL via email**
- Include any additional setup instructions if needed

---

## Requirements

### 1. **PDF Document Processing & RAG Pipeline (Required)**
   - Parse PDF file to text and split into chunks
   - Convert each chunk to vector embeddings and store in vector database
   - Implement retrieval system that embeds user questions and searches for relevant document chunks
   - Implement generation system that combines retrieved context with questions and sends to LLM

### 2. **Backend API (Required)**
   - Implement the following endpoints using **FastAPI**:
     - `POST /api/upload`: PDF file upload and vectorization processing
     - `GET /api/documents`: Retrieve processed document information
     - `POST /api/chat`: Generate RAG-based answers to questions
     - `GET /api/chunks`: Retrieve document chunks and metadata (optional)
   - Configure CORS to allow API calls from Next.js app
   - Integrate with vector database (e.g., Chroma, FAISS, Pinecone, etc.)

### 3. **Frontend UI/UX (Required)**
   - Implement user-friendly chat interface using **Next.js**
   - Real-time Q&A functionality (chat format)
   - Document upload status display and processing progress
   - Display referenced document chunk sources with answers
   - Loading states and error handling

### 4. **Recommended Tech Stack**
   - **Document Processing**: PyPDF2, pdfplumber, or langchain Document Loaders
   - **Embedding Models**: OpenAI embeddings, Sentence Transformers, or HuggingFace embeddings
   - **Vector Database**: ChromaDB (local), FAISS, or Pinecone
   - **LLM**: OpenAI GPT, Google Gemini, Anthropic Claude, or open-source models
   - **Frameworks**: LangChain or LlamaIndex (for RAG pipeline construction)

### 5. **Bonus Features (Optional)**
   - Multi-PDF file support
   - Conversation history maintenance and context continuity
   - Answer quality evaluation and feedback system
   - Visual highlighting of document chunks
   - Financial metrics calculator integration
   - Chart and graph generation functionality

---

## Free LLM APIs and Embedding Services

### LLM Services
- **OpenAI API**: GPT-3.5/4 (free credits provided)
- **Google Gemini API**: Free tier available
- **Anthropic Claude**: Free credits provided
- **Cohere**: Free API available
- **Hugging Face**: Free open-source models

### Embedding Services
- **OpenAI Embeddings**: text-embedding-ada-002
- **Cohere Embeddings**: Free tier available
- **Sentence Transformers**: Open-source models for local execution
- **Hugging Face Embeddings**: Various free models available

### Vector Databases
- **ChromaDB**: Free local and cloud usage
- **FAISS**: Free open-source by Meta
- **Weaviate**: Free cloud tier available
- **Pinecone**: Free starter plan available

---

## Project Structure

```
coding-test-2nd/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models/              # Data models
│   │   └── schemas.py       # Pydantic schemas
│   ├── services/            # RAG service logic
│   │   ├── pdf_processor.py # PDF processing and chunking
│   │   ├── vector_store.py  # Vector database integration
│   │   └── rag_pipeline.py  # RAG pipeline
│   ├── requirements.txt     # Python dependencies
│   └── config.py           # Configuration file
├── frontend/
│   ├── pages/              # Next.js pages
│   │   ├── index.tsx       # Main page
│   │   └── _app.tsx        # App component
│   ├── components/         # React components
│   │   ├── ChatInterface.tsx
│   │   └── FileUpload.tsx
│   ├── styles/             # CSS files
│   │   └── globals.css     # Global styles
│   ├── package.json        # Node.js dependencies
│   ├── tsconfig.json       # TypeScript configuration
│   ├── next.config.js      # Next.js configuration
│   ├── next-env.d.ts       # Next.js type definitions
│   └── .eslintrc.json      # ESLint configuration
├── data/
│   └── FinancialStatement_2025_I_AADIpdf.pdf
└── README.md
```

---

## Getting Started

### 1. **Environment Setup**
```bash
# Clone repository
git clone <your-repository-url>
cd coding-test-2nd

# Set up Python virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. **Backend Setup**
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (create .env file)
OPENAI_API_KEY=your_openai_api_key
VECTOR_DB_PATH=./vector_store
PDF_UPLOAD_PATH=../data

# Run server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. **Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

**Note**: If you encounter TypeScript/linting errors:
- Make sure `npm install` completed successfully
- The project includes all necessary configuration files (`tsconfig.json`, `.eslintrc.json`, `next-env.d.ts`)
- Check that all dependencies are properly installed in `node_modules`

### 4. **Initial Data Processing**
```bash
# Process and vectorize PDF file via API
curl -X POST "http://localhost:8000/api/upload" \
     -F "file=@../data/FinancialStatement_2025_I_AADIpdf.pdf"
```

---

## API Endpoints

### **POST /api/upload**
Upload PDF file and store in vector database
```json
{
  "file": "multipart/form-data"
}
```

### **POST /api/chat**
Generate RAG-based answer to question
```json
{
  "question": "What is the total revenue for 2025?",
  "chat_history": [] // optional
}
```

Response:
```json
{
  "answer": "The total revenue for 2025 is 123.4 billion won...",
  "sources": [
    {
      "content": "Related document chunk content",
      "page": 1,
      "score": 0.85
    }
  ],
  "processing_time": 2.3
}
```

### **GET /api/documents**
Retrieve processed document information
```json
{
  "documents": [
    {
      "filename": "FinancialStatement_2025_I_AADIpdf.pdf",
      "upload_date": "2024-01-15T10:30:00Z",
      "chunks_count": 125,
      "status": "processed"
    }
  ]
}
```

---

## Evaluation Criteria

### 1. **RAG System Implementation (30%)**
   - PDF processing and chunking quality
   - Embedding and vector search accuracy
   - LLM integration and answer quality

### 2. **Code Quality & Structure (30%)**
   - Code readability and maintainability
   - Modularization and separation of concerns
   - Error handling and logging

### 3. **User Experience (20%)**
   - Intuitive chat interface
   - Real-time feedback and loading states
   - Answer source display and reliability

### 4. **Technical Implementation (20%)**
   - API design and documentation
   - Performance optimization
   - Scalable architecture

---

## Submission

### 📦 **What to Submit**
1. **Your forked GitHub repository** with complete implementation
2. **All source code** (frontend, backend, configurations)
3. **Updated documentation** with any additional setup instructions
4. **Runnable demo** that works locally

### 📧 **How to Submit**
1. **Complete your implementation** in your forked repository
2. **Test thoroughly** to ensure everything works
3. **Push all changes** to your GitHub repository
4. **Send an email** with your repository URL to the designated contact

### 📝 **Repository Should Include**
- Complete frontend and backend implementation
- All necessary configuration files
- Clear installation and execution instructions
- Any additional documentation or notes

### 🎥 **Optional Extras**
- **Demo video** showing your system in action
- **Performance analysis** or optimization notes
- **Future improvement suggestions**

---

## Sample Questions

Your system should be able to handle questions like these about the financial statement PDF:

- "What is the total revenue for 2025?"
- "What is the year-over-year operating profit growth rate?"
- "What are the main cost items?"
- "How is the cash flow situation?"
- "What is the debt ratio?"

---

## Troubleshooting

### Common Issues

**Frontend TypeScript Errors**:
- Ensure `npm install` was completed successfully
- Check that `node_modules` directory exists and is populated
- Verify all configuration files are present

**Backend Import Errors**:
- Activate Python virtual environment
- Install all requirements: `pip install -r requirements.txt`
- Check Python path and module imports

**CORS Issues**:
- Ensure backend CORS settings allow frontend origin
- Check that API endpoints are accessible from frontend

---

**Build a smarter document Q&A system with RAG technology!** 

---

## Screenshot Results

Berikut adalah penjelasan hasil running project berdasarkan screenshot yang tersedia:

### Screenshot 1: `Screenshot 2025-06-18 181021 001.png`
- **Deskripsi**: Menampilkan halaman utama aplikasi RAG-based Financial Statement Q&A System
- **Fitur yang terlihat**: Interface chat yang user-friendly dengan area untuk mengajukan pertanyaan tentang dokumen laporan keuangan
- **Status**: Aplikasi berhasil berjalan dan siap menerima pertanyaan dari pengguna

### Screenshot 2: `Screenshot 2025-06-18 181134 002.png`
- **Deskripsi**: Menampilkan proses upload dan processing dokumen PDF
- **Fitur yang terlihat**: Sistem berhasil memproses file `FinancialStatement_2025_I_AADIpdf.pdf` dan melakukan vectorization
- **Status**: Dokumen berhasil di-upload dan diproses untuk RAG pipeline

### Screenshot 3: `Screenshot 2025-06-18 181208 003.png`
- **Deskripsi**: Menampilkan hasil Q&A dengan pertanyaan tentang laporan keuangan
- **Fitur yang terlihat**: Sistem memberikan jawaban berdasarkan dokumen yang diproses dengan menampilkan sumber referensi
- **Status**: RAG pipeline berfungsi dengan baik dalam memberikan jawaban yang akurat

### Screenshot 4: `Screenshot 2025-06-18 181254 004.png`
- **Deskripsi**: Menampilkan interface chat yang lengkap dengan riwayat percakapan
- **Fitur yang terlihat**: Multiple Q&A interactions dengan source citations dan loading states
- **Status**: Sistem chat berjalan lancar dengan fitur real-time Q&A dan source tracking

### Kesimpulan Running Project
✅ **Backend FastAPI**: Berhasil berjalan di port 8000 dengan semua endpoint berfungsi  
✅ **Frontend Next.js**: Interface responsive dan user-friendly  
✅ **RAG Pipeline**: PDF processing, vectorization, dan Q&A generation berjalan optimal  
✅ **Vector Database**: Penyimpanan dan retrieval dokumen berfungsi dengan baik  
✅ **Real-time Chat**: Sistem chat dengan source citations berjalan lancar  

Project ini telah berhasil mengimplementasikan sistem RAG-based Q&A untuk dokumen laporan keuangan dengan teknologi modern dan user experience yang baik. 