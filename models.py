from pydantic import BaseModel
from typing import List, Optional

class CrawlRequest(BaseModel):
    base_url: str
    max_pages: int = 10
    max_depth: int = 2

class CrawlResponse(BaseModel):
    message: str
    pages_crawled: int
    chunks_generated: int

class AskRequest(BaseModel):
    question: str

class Source(BaseModel):
    url: str
    title: str

class AskResponse(BaseModel):
    answer: str
    sources: List[Source]
