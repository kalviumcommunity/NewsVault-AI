# NewsVault AI

## AI-Powered Journalism Research Assistant

NewsVault AI is an AI-powered journalism research assistant that helps users search, retrieve, and understand information from a structured archive of documents.

The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from archived documents and generate grounded answers using an AI model. Every answer is connected to its retrieved sources so that users can verify the information through evidence.

---

## Features

### 🔎 Intelligent Archive Search
- Search the archive using natural-language questions.
- Retrieve relevant document chunks using semantic similarity.
- Return the most relevant sources for each query.

### 🤖 AI-Powered Answers
- Generate concise answers using retrieved archive evidence.
- Answers are grounded only in retrieved content.
- Reduces unsupported or hallucinated information.
- Prevents unnecessary repetition in generated responses.

### 📚 Evidence-Based Research
- Display the primary sources used to generate an answer.
- View the actual retrieved evidence from the archive.
- Show source filename, chunk information, and relevance score.

### 🎯 Metadata Filtering
Users can refine searches using:
- Date range
- Content type
- Author
- Topic
- Keywords

### 📄 Document Upload
Supports archive documents such as:
- PDF
- DOCX
- TXT

### 🧠 Retrieval-Augmented Generation
The system follows the complete RAG pipeline:

```text
User Question
      ↓
Query Embedding
      ↓
Vector Similarity Search
      ↓
Relevant Document Chunks
      ↓
Context Construction
      ↓
Grounded Prompt
      ↓
Gemini AI
      ↓
Answer + Sources
````

### ⚠️ Insufficient Information Handling

If the archive does not contain enough relevant information, the system avoids generating unsupported answers and returns an insufficient-information response.

---

# Technology Stack

## Frontend

* Streamlit
* HTML
* CSS

## Backend

* Python
* FastAPI-compatible backend architecture
* LangChain components where applicable

## AI / Machine Learning

* Google Gemini API
* Gemini 3.6 Flash for answer generation
* Gemini Embedding 2 for vector embeddings

## Database

* PostgreSQL
* pgvector

## Document Processing

* PyMuPDF (`fitz`) for PDF extraction
* python-docx for DOCX extraction
* Python file handling for TXT documents

## Development Tools

* Git
* GitHub
* VS Code
* Postman / Bruno
* Python virtual environment

---

# System Architecture

```text
                         ┌─────────────────────┐
                         │      User           │
                         │ Natural Language    │
                         │      Question       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Streamlit Frontend  │
                         │ Search + Filters    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   RAG Service       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Query Embedding     │
                         │ Gemini Embedding 2  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ PostgreSQL +        │
                         │ pgvector            │
                         │ Vector Search       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Relevant Chunks     │
                         │ + Metadata          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Context Builder     │
                         │ + RAG Prompt        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Gemini 3.6 Flash    │
                         │ Answer Generation  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                  ┌─────────────────┴─────────────────┐
                  │                                   │
                  ▼                                   ▼
          ┌───────────────┐                   ┌───────────────┐
          │ AI Answer     │                   │ Source /      │
          │               │                   │ Evidence      │
          └───────────────┘                   └───────────────┘
```

---

# RAG Pipeline

NewsVault AI uses Retrieval-Augmented Generation to ensure that generated answers are based on the archive.

## 1. Document Ingestion

Documents are uploaded and processed by the document extraction layer.

Supported formats:

```text
PDF
DOCX
TXT
```

Text is extracted from the uploaded document.

---

## 2. Text Chunking

Large documents are divided into smaller chunks.

Each chunk contains:

* Document ID
* Chunk index
* Text content
* Embedding

Chunking allows the system to retrieve only the relevant portions of a document instead of passing the complete document to the AI model.

---

## 3. Embedding Generation

Each document chunk is converted into a numerical vector representation using:

```text
Gemini Embedding 2
```

The project uses:

```text
Embedding dimension = 768
```

These vectors represent the semantic meaning of the text.

---

## 4. Vector Storage

Embeddings are stored in PostgreSQL using the `pgvector` extension.

The database stores both document metadata and vector embeddings.

Example:

```text
documents
    │
    ├── filename
    ├── document_date
    ├── content_type
    ├── author
    └── topic

chunks
    │
    ├── document_id
    ├── chunk_index
    ├── content
    └── embedding
```

---

## 5. Query Embedding

When a user enters a question, the question is converted into an embedding using the same embedding model.

```text
User Question
      ↓
Gemini Embedding 2
      ↓
768-dimensional vector
```

---

## 6. Similarity Search

The query vector is compared against stored document vectors using cosine similarity.

The most relevant chunks are retrieved based on similarity.

The current retrieval configuration uses:

```text
Top K = 5
Similarity Threshold = 0.70
```

---

## 7. Context Construction

The retrieved chunks are combined into a structured context.

Example:

```text
[Source 1]
Filename: gdp_2025_26.txt
Chunk: 2
Content:
...

[Source 2]
Filename: gdp_2025_26.txt
Chunk: 4
Content:
...
```

The context is limited to avoid unnecessarily large prompts.

Current maximum context size:

```text
12,000 characters
```

---

## 8. Grounded Answer Generation

The retrieved context is provided to Gemini along with strict evidence rules.

The AI is instructed to:

* Use only retrieved archive evidence.
* Avoid outside knowledge.
* Avoid assumptions.
* Avoid unsupported conclusions.
* Cite factual claims using source references.
* Keep answers concise.
* Avoid repeating information.
* Clearly indicate when information is missing.

---

# Database

NewsVault AI uses PostgreSQL with the `pgvector` extension.

## Database

```text
newsvaultai
```

## Main Tables

### documents

Stores document-level information.

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    document_date DATE,
    content_type TEXT,
    author TEXT,
    topic TEXT
);
```

### chunks

Stores document chunks and their embeddings.

```sql
CREATE TABLE chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id)
        ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(768) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

# Project Structure

```text
NewsVault-AI/
│
├── backend/
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── repositories/
│   │   └── document_repository.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── rag_service.py
│   │   ├── pdf_extractor.py
│   │   └── docx_extractor.py
│   │
│   └── ...
│
├── frontend/
│   │
│   ├── components/
│   │   ├── search_bar.py
│   │   └── evidence_card.py
│   │
│   ├── pages/
│   │   ├── research_home.py
│   │   └── research_results.py
│   │
│   └── ...
│
├── data/
│   └── documents/
│       ├── economic_survey_agriculture_2025_26.txt
│       ├── economic_survey_education_2025_26.txt
│       ├── economic_survey_environment_2025_26.txt
│       ├── economic_survey_health_2025_26.txt
│       ├── economic_survey_industry_2025_26.txt
│       ├── economic_survey_infrastructure_2025_26.txt
│       ├── economic_survey_services_2025_26.txt
│       ├── envistats_india_2025.txt
│       ├── gdp_2025_26.txt
│       └── plfs_annual_report_2025.txt
│
├── tests/
│   ├── test_ai_stabilization.py
│   └── ...
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

# Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd NewsVault-AI
```

---

## 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key

GEMINI_MODEL=gemini-3.6-flash

DB_HOST=localhost
DB_PORT=5432
DB_NAME=newsvaultai
DB_USER=postgres
DB_PASSWORD=your_database_password
```

### Important

Never commit `.env` or API keys to GitHub.

Add:

```text
.env
```

to `.gitignore`.

---

# PostgreSQL Setup

Make sure PostgreSQL is installed and running.

Create the database:

```sql
CREATE DATABASE newsvaultai;
```

Connect to the database and enable pgvector:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Create the required tables using the database schema described above.

---

# Running the Application

From the project root:

```powershell
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# Example Query

A user can ask:

```text
What was the estimated Real GVA growth rate in FY 2025-26?
```

The system:

```text
Question
   ↓
Generate Query Embedding
   ↓
Search PostgreSQL + pgvector
   ↓
Retrieve Relevant GDP/Economic Survey Chunks
   ↓
Build Evidence Context
   ↓
Send Grounded Prompt to Gemini
   ↓
Generate Answer
   ↓
Display Answer + Sources
```

---

# Source Attribution

NewsVault AI provides source references alongside generated answers.

Example:

```text
In FY 2025-26, the estimated Real GVA growth rate was
7.6% [Source 1].
```

The user can then select:

```text
View Evidence
```

to inspect the retrieved archive content.

This improves transparency and allows users to verify the generated answer.

---

# Error Handling

The application handles several failure cases.

## Empty Question

If the user submits an empty question:

```text
Please enter a question to search the archive.
```

---

## No Relevant Evidence

If no retrieved chunk meets the similarity threshold:

```text
The archive does not contain sufficient information to answer
this question using the retrieved evidence.
```

---

## AI Generation Failure

If the AI service cannot generate a response:

```text
AI service could not generate an answer. Please try again later.
```

The retrieved sources remain available for inspection.

---

## Empty AI Response

If the AI model returns an empty response:

```text
AI service returned an empty response. Please try again.
```

---

# RAG Optimization

The RAG pipeline has been optimized to improve answer quality.

### Retrieval Optimization

* Similarity threshold filtering
* Top-K retrieval
* Metadata-aware filtering
* Keyword filtering
* Relevant chunk selection

### Context Optimization

* Maximum context size
* Avoid unnecessarily large prompts
* Remove irrelevant retrieved information
* Reduce duplicated information

### Prompt Optimization

The RAG prompt instructs the model to:

* Stay grounded in retrieved evidence.
* Avoid hallucinations.
* Avoid unsupported assumptions.
* Cite sources.
* Avoid repetitive answers.
* Answer only what the evidence supports.

---

# Testing

The project contains automated tests for important RAG and AI-service behavior.

Run the complete test suite:

```powershell
pytest
```

The test suite verifies areas such as:

* Empty questions
* Prompt construction
* AI generation failures
* Empty AI responses
* Context-size limits
* Insufficient retrieval handling
* RAG workflow behavior

Example successful result:

```text
12 passed
```

---

# Current Dataset

The project currently contains official Indian economic and statistical documents covering areas such as:

* GDP
* Agriculture
* Education
* Environment
* Health
* Industry
* Infrastructure
* Services
* Employment
* Labour statistics

The archive contains:

```text
10 documents
181 chunks
```

---

# Security

The project follows basic security practices:

* API keys are stored in environment variables.
* Database credentials are stored in `.env`.
* Secrets should never be committed to Git.
* Database queries use parameterized values.
* Retrieved evidence is separated from application instructions.
* AI answers are restricted to retrieved archive evidence.

---

# Future Improvements

Possible future enhancements include:

* Advanced hybrid search
* BM25 + vector search
* Reranking models
* Improved document parsing
* OCR for scanned documents
* More metadata filters
* User authentication and roles
* Search history
* Saved research
* Export answers as PDF
* Improved evidence highlighting
* Multi-document comparison
* Streaming AI responses
* Better citation verification
* Production deployment
* Automated document ingestion

---

# Project Goals

NewsVault AI aims to make journalism research:

* **Faster** — quickly find relevant archive information.
* **More accurate** — ground answers in retrieved evidence.
* **Transparent** — show the sources behind answers.
* **Efficient** — retrieve only relevant document sections.
* **Accessible** — allow users to ask questions naturally.

---

# Key RAG Design Principles

NewsVault AI follows these principles:

```text
Retrieve before generating
        ↓
Ground answers in evidence
        ↓
Limit irrelevant context
        ↓
Cite supporting sources
        ↓
Avoid unsupported claims
        ↓
Show evidence to the user
```

---

# Conclusion

NewsVault AI combines **semantic search, vector databases, document processing, and generative AI** to create an evidence-grounded journalism research assistant.

By using a Retrieval-Augmented Generation architecture, the system can retrieve relevant information from an archive and generate concise answers while maintaining a clear connection between the answer and its underlying evidence.

The project demonstrates the practical use of:

```text
Python
+
Streamlit
+
Gemini
+
Embeddings
+
PostgreSQL
+
pgvector
+
RAG
=
NewsVault AI
```

---
