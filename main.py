from fastapi import FastAPI, HTTPException, BackgroundTasks
from models import CrawlRequest, CrawlResponse, AskRequest, AskResponse
from crawler import Crawler
from chunker import process_page
from storage import add_documents
from rag import rag_pipeline
import uvicorn

app = FastAPI(title="RAG Crawler API")

def crawl_task(base_url, max_pages, max_depth):
    crawler = Crawler()
    pages = crawler.crawl(base_url, max_pages, max_depth)
    
    total_chunks = 0
    for page in pages:
        chunks = process_page(page)
        add_documents(chunks)
        total_chunks += len(chunks)
        
    print(f"Crawl finished. Processed {len(pages)} pages and {total_chunks} chunks.")

@app.post("/crawl", response_model=CrawlResponse)
async def crawl_endpoint(request: CrawlRequest, background_tasks: BackgroundTasks):
    # Run crawling in background to not block the request
    background_tasks.add_task(crawl_task, request.base_url, request.max_pages, request.max_depth)
    return CrawlResponse(
        message=f"Started crawling {request.base_url}. This happens in the background.",
        pages_crawled=0, # Placeholder as it's async
        chunks_generated=0
    )

@app.post("/ask", response_model=AskResponse)
async def ask_endpoint(request: AskRequest):
    answer, sources = rag_pipeline(request.question)
    return AskResponse(answer=answer, sources=sources)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
