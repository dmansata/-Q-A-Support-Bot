# RAG Crawler

A simple Retrieval-Augmented Generation (RAG) system that crawls a website, extracts text, stores embeddings in ChromaDB, and answers questions.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the API:
   ```bash
   python main.py
   ```
   The server will start at `http://localhost:8000`.

## API Endpoints

### 1. Crawl a Website (POST `/crawl`)
Start the background crawling process.
```json
{
  "base_url": "https://example.com",
  "max_pages": 10
}
```

### 2. Ask a Question (POST `/ask`)
Retrieve context and generate an answer (currently a placeholder generation).
```json
{
  "question": "What is the content of the example domain?"
}
```

## Documentation
Visit `http://localhost:8000/docs` for the interactive Swagger UI.
